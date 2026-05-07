from backend.tools.gmail_tool import GmailTool


def test_send_email():
    gmail = GmailTool()

    result = gmail.send_email(
        to="dhe2raj05@gmail.com",   # Replace with your Gmail
        subject="Personal Agent Test Email",
        body="This is a successful test email sent from your personal agent backend."
    )

    print(result)


if __name__ == "__main__":
    test_send_email()