from utils import *

if __name__ == "__main__":
    contest_type = input('Enter type(0-8 or 9-11): ')

    with open('data/' + contest_type + '.html') as f:
        data = f.read()

    students = []
    tasks = []

    process_tasks(data, tasks)
    set_task_scores(tasks)

    num_ids = process_students(data, students)
    fill_results(data, students, tasks)
    set_student_scores(students, tasks)

    set_student_correction_for_contest(students, contest_type)

    for task in tasks:
        print(task)
    print()

    for student in students:
        print(student)
    print()

    print_table_result(students, num_ids)

