# 导师演示 1.1：本地最小「被测接口」——用 curl -v 当显微镜观察 HTTP 原始报文
# 只用 Python 标准库（http.server + json），任何 Python 3 可跑，不需要装任何包
#
# 运行方式（两个终端）：
#   终端A：python demo_http_server.py   → 打印「监听」后一直卡着 = 服务器起来了；Ctrl+C 停
#   终端B：curl -v http://127.0.0.1:8000/cases   → -v 显示原始报文（> 是请求，< 是响应）
#
# 端点菜单（本课全部状态码都能现场打出来）：
#   GET    /cases            → 200 用例列表        GET /cases/TC001 → 200 单条
#   GET    /cases/TC999      → 404 资源不存在      GET /nope        → 404 端点不存在
#   POST   /cases            → 201 创建成功        坏 body/缺字段    → 400
#   PUT    /cases/TC001      → 200 更新成功        DELETE /cases/TC001 → 204 删除成功
#   GET    /report           → 不带凭证 401 / 凭证错 403 / 带 Authorization: Bearer secret → 200
#
# 注意：数据在内存（CASES 字典）里，POST/PUT/DELETE 是真改，重启服务器就恢复原样；
#       服务器终端每个请求会打一行访问日志——那就是 3.4 要正式接的 logging 的最原始形态
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST, PORT = "127.0.0.1", 8000  # 只监听回环地址：仅本机可访问，安全；端口被占就改 8001

CASES = {
    "TC001": {"case_id": "TC001", "title": "登录接口验证", "level": "P0"},
    "TC002": {"case_id": "TC002", "title": "下单接口验证", "level": "P1"},
}
TOKEN = "Bearer secret"  # 假装这是登录后的有效凭证（真实项目里由登录接口发放，3.7 讲）


class ApiHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # 声明用 HTTP/1.1 应答（配合 Content-Length 支持长连接）

    def _send_json(self, status, payload=None):
        """响应的统一出口：状态行 → 响应头 → 空行 → 响应体，正是报文三段式"""
        self.send_response(status)  # 状态行：HTTP/1.1 <状态码> <原因短语>（Server/Date 头自动附带）
        if payload is None:  # 204 No Content：不许带 body（RFC 也禁止带 Content-Length）
            self.end_headers()
            return
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_header("Content-Type", "application/json; charset=utf-8")  # 告诉客户端 body 是什么格式
        self.send_header("Content-Length", str(len(body)))  # 告诉客户端 body 有多少字节
        self.end_headers()  # 空行：头与体的分界线
        self.wfile.write(body)  # 响应体

    def do_GET(self):  # 方法名 do_XXX 就是「这个服务器支持哪些方法」——没定义的方法会得到 501
        if self.path == "/cases":
            self._send_json(200, list(CASES.values()))  # 读集合成功 → 200
        elif self.path.startswith("/cases/"):
            case = CASES.get(self.path.removeprefix("/cases/"))
            if case is None:
                self._send_json(404, {"error": "用例不存在"})  # 资源不存在 → 404
            else:
                self._send_json(200, case)
        elif self.path == "/report":
            auth = self.headers.get("Authorization", "")  # 从请求头里取凭证
            if not auth:
                self._send_json(401, {"error": "未携带凭证"})  # 没带凭证 = 未认证 → 401
            elif auth != TOKEN:
                self._send_json(403, {"error": "无权限"})  # 带了但不对/权限不够 → 403
            else:
                self._send_json(200, {"report": "本轮全部通过"})
        else:
            self._send_json(404, {"error": "端点不存在"})

    def _read_body(self):
        """读请求体：按 Content-Length 声明的字节数读——头与体配合的典型例子"""
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def do_POST(self):
        raw = self._read_body()  # 先把体读干净再处置：keep-alive 下没读完的体会被当下一条请求，污染解析
        if self.path != "/cases":
            self._send_json(404, {"error": "端点不存在"})
            return
        try:
            data = json.loads(raw or b"{}")
        except ValueError:  # 语法坏→JSONDecodeError、编码坏→UnicodeDecodeError，都是 ValueError 子类（5.2：精确捕获≠只捕最窄的那个）
            self._send_json(400, {"error": "请求体不是合法 JSON（语法或编码错）"})  # 客户端发坏的 → 400，不许崩连接
            return
        if "case_id" not in data:
            self._send_json(400, {"error": "缺少 case_id 字段"})  # 参数不齐 → 也是 400
            return
        CASES[data["case_id"]] = data  # 真「创建」：写进内存字典
        self._send_json(201, {"created": data["case_id"]})  # 创建成功 → 201

    def do_PUT(self):
        raw = self._read_body()  # 同 do_POST：先读干净体——404 提前返回的路径也不能把半截 body 留在连接里
        if not self.path.startswith("/cases/"):
            self._send_json(404, {"error": "端点不存在"})
            return
        case_id = self.path.removeprefix("/cases/")
        if case_id not in CASES:
            self._send_json(404, {"error": "用例不存在"})  # 改一个不存在的资源 → 404
            return
        try:
            data = json.loads(raw or b"{}")
        except ValueError:  # 同 do_POST：JSONDecodeError / UnicodeDecodeError 都在 ValueError 家族
            self._send_json(400, {"error": "请求体不是合法 JSON（语法或编码错）"})
            return
        CASES[case_id].update(data)  # 更新字段
        self._send_json(200, {"updated": case_id})  # 更新成功 → 200

    def do_DELETE(self):
        if not self.path.startswith("/cases/"):
            self._send_json(404, {"error": "端点不存在"})
            return
        case_id = self.path.removeprefix("/cases/")
        if case_id not in CASES:
            self._send_json(404, {"error": "用例不存在"})  # 删一个不存在的资源 → 404（幂等：状态上「它没了」成立）
            return
        del CASES[case_id]
        self._send_json(204)  # 删除成功、无内容可回 → 204


if __name__ == "__main__":  # 老规矩：import 无副作用
    server = ThreadingHTTPServer((HOST, PORT), ApiHandler)
    print(f"被测接口服务已监听 http://{HOST}:{PORT}（Ctrl+C 停止）", flush=True)  # flush=True：输出被重定向到文件时也不憋在缓冲区
    print("端点: GET /cases | GET /cases/<id> | POST /cases | PUT /cases/<id> | DELETE /cases/<id> | GET /report", flush=True)
    try:
        server.serve_forever()  # 阻塞循环：来一个请求分发到对应的 do_XXX
    except KeyboardInterrupt:
        print("\n收到 Ctrl+C，服务器关闭")
        server.shutdown()
