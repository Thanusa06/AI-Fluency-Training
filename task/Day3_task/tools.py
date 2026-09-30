import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "student_data.json"


def get_subject_mark(subject: str) -> str:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        mark = data["subjects"].get(subject)

        if mark is None:
            return f"Error: No mark found for subject '{subject}'."

        return f"{data['student']}'s {subject} mark is {mark}."

    except Exception as exc:
        return f"Error reading student data: {exc}"
