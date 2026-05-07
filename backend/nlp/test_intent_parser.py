from backend.nlp.intent_parser import IntentParser


def test_intents():
    parser = IntentParser()

    test_commands = [
        "show my emails",
        "show my events",
        "schedule DSA practice session tomorrow at 5 pm",
        "schedule project meeting tomorrow at 11 am",
        "send email to example@gmail.com about internship update",
        "draft email to example@gmail.com about internship followup"

    ]
    for command in test_commands:
        result = parser.parse(command)

        print(f"Input: {command}")
        print("Parsed Output:")
        print(result)

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    test_intents()