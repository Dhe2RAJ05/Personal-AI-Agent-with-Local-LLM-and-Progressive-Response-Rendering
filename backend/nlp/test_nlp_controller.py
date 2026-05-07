from backend.nlp.nlp_controller import NLPController


def test_nlp_controller():
    controller = NLPController()

    test_commands = [
        "show my emails",
        "show my events",
        "schedule DSA practice session",
        "send email to dhe2raj05@gmail.com about NLP system test",
        "draft email to dhe2raj05@gmail.com about NLP draft test",
        "schedule DSA practice session",
        "schedule project meeting"
    ]

    for command in test_commands:
        print(f"User Input: {command}")

        result = controller.process_user_input(command)

        print("System Output:")
        print(result)

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    test_nlp_controller()