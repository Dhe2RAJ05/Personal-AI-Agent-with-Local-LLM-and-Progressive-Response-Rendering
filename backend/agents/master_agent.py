from backend.agents.gmail_agent import GmailAgent
from backend.agents.calendar_agent import CalendarAgent


class MasterAgent:
    def __init__(self):
        self.gmail_agent = GmailAgent()
        self.calendar_agent = CalendarAgent()

    def process_request(self, agent_type, command, **kwargs):
        agent_type = agent_type.lower()

        if agent_type == "gmail":
            return self.gmail_agent.process_command(
                command=command,
                **kwargs
            )

        elif agent_type == "calendar":
            return self.calendar_agent.process_command(
                command=command,
                **kwargs
            )

        else:
            return {
                "status": "failed",
                "error": f"Unknown agent type: {agent_type}"
            }