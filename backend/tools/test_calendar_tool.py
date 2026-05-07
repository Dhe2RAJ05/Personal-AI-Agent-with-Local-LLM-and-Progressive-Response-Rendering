from backend.tools.calendar_tool import CalendarTool
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def test_calendar():
    calendar = CalendarTool()
    
    # India timezone-aware current time
    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))

    print("Time of execution:", now_ist)

    # Event starts 1 hour later
    start_time = now_ist + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    print("Start Time ISO:", start_time.isoformat())
    print("End Time ISO:", end_time.isoformat())
    
    result = calendar.create_event(
        summary="Personal Agent Test Event",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat()
    )

    print("Calendar Event Creation Result:\n")
    print(result)


if __name__ == "__main__":
    test_calendar()