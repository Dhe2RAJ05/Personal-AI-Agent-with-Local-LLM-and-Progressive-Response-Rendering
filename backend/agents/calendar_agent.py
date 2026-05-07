from backend.tools.calendar_tool import CalendarTool
from backend.db.database import SessionLocal
from backend.db.models import Task


class CalendarAgent:
    def __init__(self):
        self.calendar_tool = CalendarTool()

    def log_task(self, task_name, status, result):
        db = SessionLocal()

        try:
            new_task = Task(
                agent_name="calendar_agent",
                task=task_name,
                status=status,
                result=str(result)
            )

            db.add(new_task)
            db.commit()

        finally:
            db.close()

    def process_command(self, command, **kwargs):
        command = command.lower()

        if command == "create event":
            result = self.calendar_tool.create_event(
                summary=kwargs.get("summary"),
                start_time=kwargs.get("start_time"),
                end_time=kwargs.get("end_time")
            )

            self.log_task(
                task_name=f"Create event: {kwargs.get('summary')}",
                status=result["status"],
                result=result
            )

            return result

        elif command == "list events":
            result = self.calendar_tool.list_upcoming_events(
                max_results=kwargs.get("max_results", 10)
            )

            self.log_task(
                task_name="List upcoming events",
                status="success",
                result=result
            )

            return result

        elif command == "search date":
            result = self.calendar_tool.search_events_by_date(
                target_date=kwargs.get("target_date")
            )

            self.log_task(
                task_name=f"Search calendar events on {kwargs.get('target_date')}",
                status="success",
                result=result
            )

            return result

        elif command == "delete event":
            result = self.calendar_tool.delete_event(
                event_id=kwargs.get("event_id")
            )

            self.log_task(
                task_name=f"Delete event {kwargs.get('event_id')}",
                status=result["status"],
                result=result
            )

            return result
        
        else:
            error_result = {
                "status": "failed",
                "error": f"Unknown command: {command}"
            }

            self.log_task(
                task_name=command,
                status="failed",
                result=error_result
            )

            return error_result