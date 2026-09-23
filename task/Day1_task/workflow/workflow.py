import json

# Load private student data
with open("data/student_data.json", "r") as file:
    data = json.load(file)

print("\n--- Rule-Based Workflow ---")
print("Student:", data["student"])

print("\nSubject Analysis:")

for subject, mark in data["subjects"].items():

    if mark < 40:
        status = "High Priority"

    elif mark < 60:
        status = "Needs Practice"

    else:
        status = "Good"

    print(f"{subject}: {mark} -> {status}")
    