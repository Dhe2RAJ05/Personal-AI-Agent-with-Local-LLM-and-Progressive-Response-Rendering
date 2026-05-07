from google_auth import authenticate_gmail


def test_gmail_auth():
    creds = authenticate_gmail()

    if creds:
        print("Gmail authentication successful.")
    else:
        print("Authentication failed.")


if __name__ == "__main__":
    test_gmail_auth()