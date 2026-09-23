def chatbot(user_input):
    print("\n--- Plain Chatbot ---")
    print("User:", user_input)

    response = (
        "You should focus on subjects where you need more practice. "
        "Try creating a study schedule based on your weak subjects."
    )

    print("Chatbot:", response)


user_input = input("Ask your question: ")
chatbot(user_input)
