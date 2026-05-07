import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class IntentParser:
    def parse(self, user_input: str):
        text = user_input.lower()

        # Gmail intents
        if "show my emails" in text or "read emails" in text:
            return {
                "agent_type": "gmail",
                "command": "read emails",
                "parameters": {
                    "max_results": 5
                }
            }

        elif "search emails from" in text:
            match = re.search(r"search emails from (.+)", text)

            if match:
                sender_email = match.group(1).strip()

                return {
                    "agent_type": "gmail",
                    "command": "search sender",
                    "parameters": {
                        "sender_email": sender_email,
                        "max_results": 5
                    }
                }
        
        elif "draft email to" in text:
            match = re.search(
                r"draft email to\s+([^\s]+)\s+about\s+(.+)",
                text
            )

            if match:
                recipient = match.group(1).strip()
                subject = match.group(2).strip()

                return {
                    "agent_type": "gmail",
                    "command": "draft email",
                    "parameters": {
                        "to": recipient,
                        "subject": subject,
                        "body": f"Regarding: {subject}"
                    }
                }
                
        elif "send email to" in text:
            match = re.search(
                r"send email to\s+([^\s]+)\s+about\s+(.+)",
                text
            )

            if match:
                recipient = match.group(1).strip()
                subject = match.group(2).strip()

                return {
                    "agent_type": "gmail",
                    "command": "send email",
                    "parameters": {
                        "to": recipient,
                        "subject": subject,
                        "body": f"Regarding: {subject}"
                    }
                }
        
        # Calendar intents
        elif "schedule" in text:
            summary = text.replace("schedule", "").strip()

            # Default: tomorrow
            target_date = datetime.now(
                ZoneInfo("Asia/Kolkata")
            ) + timedelta(days=1)

            # Default time
            hour = 9
            minute = 0

            # Detect "tomorrow"
            if "tomorrow" in text:
                summary = summary.replace("tomorrow", "").strip()

            # Detect time like "5 pm" or "11 am"
            time_match = re.search(r"(\d{1,2})\s*(am|pm)", text)

            if time_match:
                hour = int(time_match.group(1))
                am_pm = time_match.group(2)

                if am_pm == "pm" and hour != 12:
                    hour += 12
                elif am_pm == "am" and hour == 12:
                    hour = 0

                summary = re.sub(r"\d{1,2}\s*(am|pm)", "", summary).strip()

            start_time = target_date.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            end_time = start_time + timedelta(hours=1)

            return {
                "agent_type": "calendar",
                "command": "create event",
                "parameters": {
                    "summary": summary,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat()
                }
            }

        elif "show my events" in text or "list events" in text:
            return {
                "agent_type": "calendar",
                "command": "list events",
                "parameters": {
                    "max_results": 10
                }
            }

        return {
            "status": "failed",
            "error": "Could not determine user intent"
        }