"""4.3 继承练习：用继承组织测试用例类

BaseCase 抽出所有用例的共性（编号、标题、计数、报告格式），
ApiCase / UICase 各自只写"不一样的部分"（判定通过的逻辑）。
好处：公共代码只写一遍，新增用例类型（如性能用例）只需再继承一次。
"""


class BaseCase:
    """所有测试用例的基类（父类）：定义共性属性和通用方法"""

    # 类属性：挂在类身上，所有实例共享，用来统计创建过的用例总数
    # （对比实例属性 self.xxx：每个实例各存一份）
    total_count = 0

    def __init__(self, case_id, title):
        # 用"类名.属性"修改类属性：每创建一个实例，总数 +1
        BaseCase.total_count += 1
        self.case_id = case_id  # 实例属性：用例编号，如 "API-001"
        self.title = title  # 实例属性：用例标题

    def run(self):
        # 基类只给默认实现（占位）："具体怎么算通过"留给子类重写
        return "NOT_RUN"

    def describe(self):
        # 通用的报告格式。关键在 self.run()：
        # 运行时 self 是哪个子类的实例，就执行哪个子类重写后的 run()
        # —— 基类方法调用子类实现，这就是多态（4.4 正式讲）
        return f"[{self.case_id}] {self.title} -> {self.run()}"


class ApiCase(BaseCase):
    """接口用例：类名后括号里写父类名，即单继承

    自动拥有 BaseCase 的 total_count / describe()，只补接口特有的部分。
    """

    def __init__(self, case_id, title, url, status_code):
        # super() 代表父类：公共属性（case_id/title）的初始化交给父类做，
        # 子类不抄一遍代码，只处理自己新增的两个参数
        super().__init__(case_id, title)
        self.url = url  # 实例属性：接口地址
        self.status_code = status_code  # 实例属性：接口实际返回的状态码

    def run(self):
        # 重写（override）：同名方法覆盖父类的 "NOT_RUN" 默认实现
        # 接口用例的判定规则：状态码等于 200 才算通过
        return "PASS" if self.status_code == 200 else "FAIL"


class UICase(BaseCase):
    """UI 用例：与 ApiCase 平级，同样继承 BaseCase"""

    def __init__(self, case_id, title, element_found):
        super().__init__(case_id, title)  # 公共部分仍委托父类初始化
        self.element_found = element_found  # 实例属性：页面元素是否找到

    def run(self):
        # 重写：UI 用例的判定规则——元素找到即通过
        return "PASS" if self.element_found else "FAIL"


if __name__ == '__main__':  # 只有直接运行才执行；被 import 时不执行（3.6 学过）
    # 构造 4 个用例：2 个接口 + 2 个 UI
    # 每次实例化都会走各自的 __init__ -> super().__init__() -> total_count +1
    api1 = ApiCase("API-001", "登录接口返回200", "https://ex.com/login", 200)
    api2 = ApiCase("API-002", "查询接口返回500", "https://ex.com/query", 500)
    ui1 = UICase("UI-001", "登录按钮存在", True)
    ui2 = UICase("UI-002", "退出按钮存在", False)

    # 不同类型的对象放进同一个列表，用统一的 describe() 处理：
    # 调用方不需要关心是 API 还是 UI，每个对象各自的 run() 自动生效
    cases = [api1, api2, ui1, ui2]
    for case in cases:
        print(case.describe())

    # 用类名直接读类属性：4 个实例（含子类实例）共计数 4
    print("total_count =", BaseCase.total_count)
    # isinstance 判断"is-a"关系：子类实例同时也是父类的实例 -> True
    print("isinstance(api1, BaseCase) =", isinstance(api1, BaseCase))
    # 反过来不成立：api1 是接口用例，不是 UI 用例 -> False
    print("isinstance(api1, UICase) =", isinstance(api1, UICase))

    # ===== 思考题答案（学生作答，勿改） =====
    # 1.一个是类属性一个是实例属性；BaseCase.total_count的值是0，实例身上的total_count是1
    # 2.因为子类重写的run()这个方法
    # 3.会报AttributeError，报错信息里缺少的属性是case_id
    # 4.SpecialResult,因为调的是子类