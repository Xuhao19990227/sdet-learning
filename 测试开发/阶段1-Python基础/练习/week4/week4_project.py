class Student:
    """学生类"""
    SUBJECTS = ("语文", "数学", "英语")

    def __init__(self, name, age):
        """初始化方法"""
        self.name = name
        self.age = age
        self.__scores = {subject: 0.0 for subject in self.SUBJECTS}

    @classmethod
    def from_dict(cls, data):
        """学生类工厂"""
        student = cls(data["name"], data["age"])
        for subject, score in data["scores"].items():
            student.set_score(subject, score)
        return student

    @staticmethod
    def is_valid_score(value):
        """判断分数是否合法"""
        return 0 <= value <= 100

    def set_score(self, subject, score):
        """设置学科分数"""
        if subject not in Student.SUBJECTS:
            raise ValueError(f"科目不存在：{subject}")
        if not Student.is_valid_score(score):
            raise ValueError(f"成绩必须在0-100之间：{score}")
        self.__scores[subject] = score

    def get_score(self, subject):
        """获取科目分数"""
        if subject not in Student.SUBJECTS:
            raise ValueError(f"科目不存在：{subject}")
        return self.__scores[subject]

    def average(self):
        """获取平均分"""
        average_score = sum(self.__scores.values()) / len(Student.SUBJECTS)

        return round(average_score, 1)

    def __str__(self):
        """魔法方法str"""
        return f"{self.name}({self.age}岁) 语文 {self.__scores['语文']} 数学 {self.__scores['数学']} 英语 {self.__scores['英语']} 平均 {self.average()}"

    def __repr__(self):
        """魔法方法repr"""
        class_name = self.__class__.__name__
        return f"{class_name}({self.name!r}, {self.age!r}, {self.__scores!r})"

    def __eq__(self, other):
        """魔法方法eq"""
        if not isinstance(other, Student):
            return False
        return self.name == other.name


class ArtStudent(Student):
    """艺术生类"""
    WEIGHTS = {"语文": 0.5, "数学": 0.2, "英语": 0.3}

    def average(self):
        """返回加权平均分"""
        weighted_chinese = ArtStudent.WEIGHTS["语文"] * self.get_score("语文")
        weighted_math = ArtStudent.WEIGHTS["数学"] * self.get_score("数学")
        weighted_english = ArtStudent.WEIGHTS["英语"] * self.get_score("英语")
        weighted_average_score = weighted_chinese + weighted_math + weighted_english

        return round(weighted_average_score, 1)

    def __str__(self):
        """魔法方法str"""
        return "[艺术]" + super().__str__()


class GradeSystem:
    """学生管理系统类"""

    def __init__(self):
        self.__students = []

    def add_student(self, student):
        """添加学生"""
        if student in self.__students:
            return False
        self.__students.append(student)
        return True

    def remove_student(self, name):
        """删除学生"""
        for student in self.__students:
            if student.name == name:
                self.__students.remove(student)
                return True
        return False

    def find_student(self, name):
        """查找学生"""
        for student in self.__students:
            if student.name == name:
                return student

    def rank(self):
        """返回按平均分排序的学生"""
        return sorted(self.__students, key=lambda s: s.average(), reverse=True)

    def __len__(self):
        """魔法方法，返回学生数量"""
        return len(self.__students)

    def __str__(self):
        """魔法方法str"""
        return f"共有 {len(self)} 名学生\n" + '\n'.join(str(student) for student in self.__students)


if __name__ == '__main__':
    # 1.排序会按照Student的普通平均数排序；一个是Student类，一个是ArtStudent实例
    # 2.因为有名称修饰机制，我是用的get_score()，跟着定义属性的类走的
    # 3.因为Student类中定义了__eq__这个魔法方法，名字相等就相等
    # 4.不需要改，同一套 Student 类，既可以用于命令行工具，也可以用于 Web 后端，还可以用于数据分析脚本（Jupyter Notebook），甚至用于移动端 App 的后端逻辑

    def handle_find(system):
        name = input("输入姓名：")
        student = system.find_student(name)
        if student is None:
            print("未找到该学生")
        else:
            print(student)


    def handle_add(system):
        name = input("输入姓名：")
        if system.find_student(name) is not None:
            print("该学生已存在")
        else:
            try:
                age = int(input("输入年龄："))
            except ValueError:
                print("输入不合法")
                return
            try:
                chinese_score = float(input("输入语文成绩："))
                math_score = float(input("输入数学成绩："))
                english_score = float(input("输入英语成绩："))
            except ValueError:
                print("输入不合法")
                return
            student = Student(name, age)
            try:
                student.set_score("语文", chinese_score)
                student.set_score("数学", math_score)
                student.set_score("英语", english_score)
            except ValueError as e:
                print(e)
            else:
                system.add_student(student)
                print(f"添加成功：{name}")


    def handle_remove(system):
        name = input("输入姓名：")
        if system.remove_student(name):
            print(f"已删除：{name}")
        else:
            print("未找到该学生")


    def handle_show_all(system):
        if len(system) == 0:
            print("暂无学生")
        else:
            print(system)


    def handle_update(system):
        name = input("输入姓名：")
        student = system.find_student(name)
        if student is None:
            print("未找到该学生")
        else:
            try:
                subject = input("输入科目：")
                score = float(input(f"输入{subject}成绩："))
            except ValueError:
                print("输入不合法")
            else:
                try:
                    student.set_score(subject, score)
                except ValueError as e:
                    print(e)
                else:
                    print("修改成功")


    def handle_rank(system):
        if len(system) == 0:
            print("暂无学生")
        else:
            for i, student in enumerate(system.rank(), start=1):
                print(f"第{i}名：{student.name} 平均分 {student.average()}")


    def main():
        students_data = [
            (Student, {"name": "张三", "age": 20,
                       "scores": {"语文": 85.0, "数学": 92.0, "英语": 78.0}}),
            (Student, {"name": "李四", "age": 21,
                       "scores": {"语文": 90.0, "数学": 88.0, "英语": 95.0}}),
            (ArtStudent, {"name": "王五", "age": 22,
                          "scores": {"语文": 99.0, "数学": 70.0, "英语": 80.0}}),
        ]
        system = GradeSystem()
        for student_cls, data in students_data:
            system.add_student(student_cls.from_dict(data))
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
        while True:
            print(begin_text)
            try:
                choice = int(input("请输入功能编号："))
            except ValueError:
                print("输入不合法")
                continue
            if choice == 0:
                print("再见")
                break
            elif choice == 1:
                handle_add(system)
            elif choice == 2:
                handle_remove(system)
            elif choice == 3:
                handle_update(system)
            elif choice == 4:
                handle_find(system)
            elif choice == 5:
                handle_show_all(system)
            elif choice == 7:
                handle_rank(system)
            else:
                print("系统无此功能选项")


    main()
