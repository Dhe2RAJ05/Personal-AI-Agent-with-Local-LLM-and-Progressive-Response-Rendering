from backend.agents.master_agent import MasterAgent
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def test_master_agent():
    master = MasterAgent()

    # Gmail test
    gmail_result = master.process_request(
        agent_type="gmail",
        command="read emails",
        max_results=3
    )

    print("Gmail Agent Result:")
    for email in gmail_result:
        print(email)

    print("\n" + "=" * 50 + "\n")

    # Calendar test
    start_time = datetime.now(ZoneInfo("Asia/Kolkata")) + timedelta(hours=2)
    end_time = start_time + timedelta(hours=1)

    calendar_result = master.process_request(
        agent_type="calendar",
        command="create event",
        summary="Master Agent Test Event",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat()
    )

    print("Calendar Agent Result:")
    print(calendar_result)


if __name__ == "__main__":
    test_master_agent()