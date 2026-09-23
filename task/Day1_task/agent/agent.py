from tools import get_subject_mark, get_pending_tasks


def run_agent():

    print("\n--- AI Agent ---")

    user_request = input("Enter your request: ")

    print("\nUser:", user_request)

    # Step 1: Agent understands the task
    print("\nAgent: I need to check the student's Maths performance.")

    # Step 2: Use tool
    maths_mark = get_subject_mark("Maths")

    print("Tool: get_subject_mark('Maths')")
    print("Tool Result:", maths_mark)

    # Step 3: Observe result
    print("\nAgent: Maths mark is low, so I should check pending tasks.")

    # Step 4: Use another tool
    tasks = get_pending_tasks()

    print("Tool: get_pending_tasks()")
    print("Tool Result:", tasks)

    # Step 5: Make decision
    print("\nAgent: Creating a study plan based on the available information.")

    print("\nFinal Answer:")
    print("You should prioritize Maths because your mark is", maths_mark)
    print("Your pending tasks are:")

    for task in tasks:
        print("-", task)

    print("\nSuggested 3-hour plan:")
    print("1 hour - Maths concepts")
    print("1 hour - Maths problem practice")
    print("30 minutes - Revision")
    print("30 minutes - Mock questions")


run_agent()