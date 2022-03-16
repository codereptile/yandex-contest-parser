import re


class Student:
    def __init__(self):
        self.name = ""
        self.results = []
        self.scores = []
        self.grade = -1
        self.id = -1

        self.final_score = 0

    def __str__(self):
        return 'Student \'' + self.name + '\'(' + str(self.id) + ') in grade ' + str(self.grade) + \
               ' got score: ' + str(sum(self.scores)) + ' with final score: ' + str(self.final_score)


class Task:
    def __init__(self):
        self.name = ""
        self.score = 1

    def __str__(self):
        return 'Task: \'' + self.name + '\' with score: ' + str(self.score)


def process_students(data, students):
    pattern_students = re.compile('class=\"user__first-letter\">\w</span>[a-zA-Z0-9\s@.-]*</span>')
    # cut my name and two last commits:
    for i in pattern_students.findall(data)[3:]:
        clear_student = re.compile('>[a-zA-Z0-9\s@.-]*<')
        parts_of_student_name = clear_student.findall(i)
        students.append(Student())
        students[-1].name = parts_of_student_name[0][1:-1] + parts_of_student_name[1][1:-1]

    grade_dic = {}
    id_dic = {}
    with open('data/class_data.txt') as f:
        id = 0
        for i in f.readlines():
            name_grade = i.split()
            grade_dic[name_grade[0]] = int(name_grade[1])
            id_dic[name_grade[0]] = id
            id += 1
        num_ids = id

    for student in students:
        if student.name in grade_dic:
            student.grade = grade_dic[student.name]
            student.id = id_dic[student.name]

    return num_ids


def process_tasks(data, tasks):
    pattern_tasks = re.compile('<a class=\"link\" href=\"/contest/\d*/problems/\w*/\">\w*</a>')
    # cut my name and two last commits:
    for i in pattern_tasks.findall(data):
        clear_task = re.compile('>\w*<')
        tasks.append(Task())
        tasks[-1].name = clear_task.findall(i)[0][1:-1]


def fill_results(data, students, tasks):
    pattern_results = re.compile('<div class=\"table__data *\w*\">[—+-][0-9]*<\/div>')

    clear_results = []

    for i in pattern_results.findall(data):
        clear_result = re.compile('>[—+-][0-9]*<')
        clear_results.append(clear_result.findall(i)[0][1:-1])

    for i in range(len(students)):
        students[i].results = clear_results[i * len(tasks):(i + 1) * len(tasks)]


def set_task_scores(tasks):
    pattern_hard = re.compile('Гроб\d?')
    pattern_super_hard = re.compile('Гробище\d?')

    for task in tasks:
        if pattern_hard.match(task.name):
            task.score = 2
        if pattern_super_hard.match(task.name):
            task.score = 3


def set_student_scores(students, tasks):
    pattern_solved = re.compile('\+[0-9]*')
    for student in students:
        for i in range(len(tasks)):
            if pattern_solved.match(student.results[i]):
                student.scores.append(tasks[i].score)
            else:
                student.scores.append(0)


def set_student_correction_for_contest(students, contest_type):
    for student in students:
        if (contest_type == '0-8' and 0 <= student.grade <= 8) or (contest_type == '9-11' and 9 <= student.grade <= 11):
            student.final_score = sum(student.scores)
        else:
            student.final_score = sum(student.scores) / 4


def print_table_result(students, num_ids):
    student_dic = {}

    for student in students:
        student_dic[student.id] = student

    print("Data from students with id's:")

    for i in range(num_ids):
        if i in student_dic:
            print(student_dic[i].final_score)
        else:
            print(0)
