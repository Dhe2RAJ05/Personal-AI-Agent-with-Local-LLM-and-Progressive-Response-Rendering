from backend.tools.gmail_tool import GmailTool
from backend.db.database import SessionLocal
from backend.db.models import Task


class GmailAgent:
    def __init__(self):
        self.gmail_tool = GmailTool()

    def log_task(self, task_name, status, result):
        db = SessionLocal()

        try:
            new_task = Task(
                agent_name="gmail_agent",
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

        if command == "send email":
            result = self.gmail_tool.send_email(
                to=kwargs.get("to"),
                subject=kwargs.get("subject"),
                body=kwargs.get("body")
            )

            self.log_task(
                task_name=f"Send email to {kwargs.get('to')}",
                status=result["status"],
                result=result
            )

            return result

        elif command == "read emails":
            result = self.gmail_tool.get_recent_emails(
                max_results=kwargs.get("max_results", 5)
            )

            self.log_task(
                task_name="Read recent emails",
                status="success",
                result=result
            )

            return result
        
        elif command == "search sender":
            result = self.gmail_tool.search_emails_by_sender(
                sender_email=kwargs.get("sender_email"),
                max_results=kwargs.get("max_results", 5)
            )

            self.log_task(
                task_name=f"Search emails from {kwargs.get('sender_email')}",
                status="success",
                result=result
            )

            return result

        elif command == "search subject":
            result = self.gmail_tool.search_emails_by_subject(
                subject_keyword=kwargs.get("subject_keyword"),
                max_results=kwargs.get("max_results", 5)
            )

            self.log_task(
                task_name=f"Search emails with subject '{kwargs.get('subject_keyword')}'",
                status="success",
                result=result
            )

            return result
        
        elif command == "draft email":
            result = self.gmail_tool.create_draft_email(
                to=kwargs.get("to"),
                subject=kwargs.get("subject"),
                body=kwargs.get("body")
            )

            self.log_task(
                task_name=f"Draft email to {kwargs.get('to')}",
                status=result["status"],
                result=result
            )

            return result

        elif command == "list drafts":
            result = self.gmail_tool.list_drafts(
                max_results=kwargs.get("max_results", 10)
            )

            self.log_task(
                task_name="List Gmail drafts",
                status="success",
                result=result
            )

            return result

        elif command == "send draft":
            result = self.gmail_tool.send_draft(
                draft_id=kwargs.get("draft_id")
            )

            self.log_task(
                task_name=f"Send draft {kwargs.get('draft_id')}",
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
        
    