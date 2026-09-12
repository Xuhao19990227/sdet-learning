students = [
    {"name": "张三", "age": 20, "scores": {"语文": 85.0, "数学": 92.0, "英语": 78.0}},
    {"name": "李四", "age": 21, "scores": {"语文": 90.0, "数学": 88.0, "英语": 95.0}},
]

while True:
    begin_text = '''====== 学生成绩管理系统 ======
  1. 添加学生
  2. 删除学生
  3. 修改成绩
  4. 查询学生
  5. 显示所有学生
  6. 统计分析
  7. 排行榜
  0. 退出系统
  =============================='''
    print(begin_text)
    students_name = [student["name"] for student in students]
    function_code = int(input("请输入功能编号："))
    if not function_code:
        print("再见")
        break
    elif function_code == 1:
        new_student = {}
        name = input("输入姓名：")
        if name in students_name:
            print("该学生已存在")
        else:
            new_student["name"] = name
            try:
                age = int(input("输入年龄："))
                new_student["age"] = age
                try:
                    chinese_score = float(input("输入语文成绩："))
                    new_student["scores"] = {}
                    new_student["scores"]["语文"] = chinese_score
                    try:
                        math_score = float(input("输入数学成绩："))
                        new_student["scores"]["数学"] = math_score
                        try:
                            english_score = float(input("输入英语成绩："))
                            new_student["scores"]["英语"] = english_score
                            # 所有信息输入都合法才会新增数据
                            students.append(new_student)
                            print(f"添加成功：{name}")
                        except ValueError:
                            print("英语输入不合法")
                    except ValueError:
                        print("数学成绩输入不合法")
                except ValueError:
                    print("语文成绩输入不合法")
            except ValueError:
                print("年龄输入不合法")
    elif function_code == 2:
        name = input("输入姓名：")
        if name not in students_name:
            print("未找到该学生")
        else:
            for student in students:
                if student["name"] == name:
                    students.remove(student)
                    print(f"已删除：{name}")
                    break
    elif function_code == 3:
        name = input("输入姓名：")
        if name not in students_name:
            print("未找到该学生")
        else:
            subject = input("输入科目：")
            if subject in ["语文", "数学", "英语"]:
                try:
                    subject_score = float(input(f"输入{subject}成绩："))
                    for student in students:
                        if student["name"] == name:
                            student["scores"][subject] = subject_score
                            print("修改成功")
                            break
                except ValueError:
                    print("成绩输入不合法")
            else:
                print("科目不存在")
    elif function_code == 4:
        name = input("输入姓名：")
        if name in students_name:
            for student in students:
                if student["name"] == name:
                    print(f"姓名：{name} | 年龄：{student['age']}")
                    print(
                        f"语文：{student['scores']['语文']}  数学：{student['scores']['数学']}  英语：{student['scores']['英语']}")
                    print(f'平均分：{sum([score for score in student["scores"].values()]) / 3:.1f}')
                    break

        else:
            print("未找到该学生")
    elif function_code == 5:
        if not students:
            print("暂无学生数据")
        else:
            print(f"{'姓名':<6}{'年龄':<6}{'语文':<6}{'数学':<6}{'英语':<6}{'平均':<6}")
            for student in students:
                avg_score = round(sum([score for score in student['scores'].values()]) / 3, 1)
                print(
                    f"{student['name']:<6}{student['age']:<7}{student['scores']['语文']:<7}{student['scores']['数学']:<7}{student['scores']['英语']:<7}{avg_score:<8}")

    elif function_code == 6:
        if not students:
            print("暂无学生数据")
        else:
            max_chinese = max([student["scores"]["语文"] for student in students])
            max_math = max([student["scores"]["数学"] for student in students])
            max_english = max([student["scores"]["英语"] for student in students])
            min_chinese = min([student["scores"]["语文"] for student in students])
            min_math = min([student["scores"]["数学"] for student in students])
            min_english = min([student["scores"]["英语"] for student in students])
            avg_chinese = round(sum([student["scores"]["语文"] for student in students]) / len(students), 1)
            avg_math = round(sum([student["scores"]["数学"] for student in students]) / len(students), 1)
            avg_english = round(sum([student["scores"]["英语"] for student in students]) / len(students), 1)
            avg_total = round((avg_chinese + avg_math + avg_english) / 3, 1)
            print("===== 统计分析 =====")
            print(f"语文  最高：{max_chinese}  最低：{min_chinese}  平均：{avg_chinese}")
            print(f"数学  最高：{max_math}  最低：{min_math}  平均：{avg_math}")
            print(f"英语  最高：{max_english}  最低：{min_english}  平均：{avg_english}")
            print(f"全班平均分：{avg_total}")

    elif function_code == 7:
        if not students:
            print("暂无学生数据")
        else:
            sorted_students = sorted(students, key=lambda x: sum(x["scores"].values()) / 3, reverse=True)
            print("===== 排行榜 =====")
            for i in range(len(sorted_students)):
                print(
                    f"第{i + 1}名：{sorted_students[i]['name']}（平均分 {sum(sorted_students[i]['scores'].values()) / 3:.1f}）")

    else:
        print('系统无此功能选项')
