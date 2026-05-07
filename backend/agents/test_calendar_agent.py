from backend.agents.calendar_agent import CalendarAgent
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def test_calendar_agent():
    agent = CalendarAgent()

    # Create test event
    start_time = datetime.now(ZoneInfo("Asia/Kolkata")) + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    create_result = agent.process_command(
        command="create event",
        summary="Calendar Agent Test Event",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat()
    )

    print("Create Event Result:")
    print(create_result)

    print("\n" + "=" * 50 + "\n")

    # List events
    list_result = agent.process_command(
        command="list events",
        max_results=5
    )

    print("Upcoming Events:")

    for event in list_result:
        print(f"Event: {event['summary']}")
        print(f"Start: {event['start']}")
        print("-" * 40)


if __name__ == "__main__":
    test_calendar_agent()