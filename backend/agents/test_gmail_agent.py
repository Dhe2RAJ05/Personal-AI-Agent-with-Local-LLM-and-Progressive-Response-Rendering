from backend.agents.gmail_agent import GmailAgent


def test_gmail_agent():
    agent = GmailAgent()

    # Test sending email
    result = agent.process_command(
        command="send email",
        to="your_email@gmail.com",   # Replace this
        subject="Agent Command Test",
        body="This email was sent through GmailAgent command processing."
    )

    print("Send Email Result:")
    print(result)

    print("\n" + "=" * 50 + "\n")

    # Test reading emails
    emails = agent.process_command(
        command="read emails",
        max_results=3
    )

    print("Recent Emails:")

    for email in emails:
        print(f"From:    {email['sender']}")
        print(f"To:      {email['recipient']}")
        print(f"Subject: {email['subject']}")
        print("-" * 40)


if __name__ == "__main__":
    test_gmail_agent()