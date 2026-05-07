from googleapiclient.discovery import build
from backend.auth.google_auth import authenticate_gmail
from datetime import datetime, timezone


class CalendarTool:
    def __init__(self):
        creds = authenticate_gmail()
        self.service = build("calendar", "v3", credentials=creds)

    def list_upcoming_events(self, max_results=10):
        now = datetime.now(timezone.utc).isoformat()

        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return []

        event_data = []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            event_data.append({
                "event_id": event["id"],
                "summary": event.get("summary", "No Title"),
                "start": start,
                "end": end
            })

        return event_data
    
    def create_event(self, summary, start_time, end_time):
        duplicate_check = self.check_existing_event(
            summary=summary,
            start_time=start_time,
            end_time=end_time
        )

        if duplicate_check["exists"]:
            return {
                "status": "failed",
                "message": f"Duplicate event already exists: {summary}",
                "existing_event_id": duplicate_check["event_id"]
            }

        conflict_check = self.check_time_conflict(
            start_time=start_time,
            end_time=end_time
        )

        if conflict_check["conflict"]:
            return {
                "status": "failed",
                "message": f"Time conflict with existing event: {conflict_check['summary']}",
                "conflicting_event_id": conflict_check["event_id"],
                "conflict_start": conflict_check["conflict_start"],
                "conflict_end": conflict_check["conflict_end"]
            }

        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time
            },
            "end": {
                "dateTime": end_time
            }
        }

        created_event = self.service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return {
            "status": "success",
            "event_id": created_event["id"],
            "event_link": created_event.get("htmlLink")
        }
    
    def search_events_by_date(self, target_date):
        start_of_day = f"{target_date}T00:00:00+05:30"
        end_of_day = f"{target_date}T23:59:59+05:30"

        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return []

        event_data = []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            event_data.append({
                "event_id": event["id"],
                "summary": event.get("summary", "No Title"),
                "start": start,
                "end": end
            })

        return event_data
    
    def delete_event(self, event_id):
        try:
            self.service.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()

            return {
                "status": "success",
                "message": f"Event {event_id} deleted successfully"
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def check_existing_event(self, summary, start_time, end_time):
        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        for event in events:
            existing_summary = event.get("summary", "").lower().strip()

            if existing_summary == summary.lower().strip():
                return {
                    "exists": True,
                    "event_id": event["id"],
                    "summary": event.get("summary")
                }

        return {
            "exists": False
        }

    def check_time_conflict(self, start_time, end_time):
        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if events:
            first_conflict = events[0]

            conflict_start = first_conflict["start"].get(
                "dateTime",
                first_conflict["start"].get("date")
            )

            conflict_end = first_conflict["end"].get(
                "dateTime",
                first_conflict["end"].get("date")
            )

            return {
                "conflict": True,
                "event_id": first_conflict["id"],
                "summary": first_conflict.get("summary", "Untitled Event"),
                "conflict_start": conflict_start,
                "conflict_end": conflict_end
            }

        return {
            "conflict": False
        }