import json


def read_student_data():
    with open("data/student_data.json", "r") as file:
        return json.load(file)


def get_subject_mark(subject):
    data = read_student_data()

    mark = data["subjects"].get(subject)

    if mark is None:
        return f"No marks found for {subject}"

    return mark


def get_pending_tasks():
    data = read_student_data()
    return data["tasks"]
    