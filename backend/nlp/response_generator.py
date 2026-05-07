import requests
import json


class ResponseGenerator:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "mistral"

    def generate_response(self, user_input, agent_result):
        prompt = f"""
You are a personal AI assistant helping the user interpret their own authorized Gmail, Calendar, and productivity data.

The backend has already securely completed the requested action.

Your responsibilities:
- ONLY interpret the provided backend result
- NEVER refuse
- NEVER mention privacy, permissions, security, phishing, or authorization
- NEVER warn unless backend data explicitly indicates danger
- DO NOT invent details
- Be accurate and grounded in provided data only

Formatting requirements (CRITICAL):
- ALWAYS output in highly structured Markdown format.
- Use headers (### or ####) for distinct sections (e.g., ### 📧 Emails, ### 📅 Events).
- Use **bold text** to highlight important names, dates, times, or key subjects.
- Use numbered lists or bullet points for multiple items.
- Ensure proper spacing (blank lines) between sections and list items.
- Use `inline code` or blockquotes (>) if quoting specific email snippets or exact fields.
- Do not use large unbroken paragraphs. Keep it extremely scannable and visually organized.
- Sound like an elite executive assistant: professional, crisp, directly to the point.
- If listing emails, strictly format like:
  - **Sender Name**: *Subject line* - Brief summary.
- If listing calendar events, strictly format like:
  - **Event Title** (*Time*) - Brief context.
- If action succeeded, clearly and briefly confirm success with a ✅ indicator.
- If action failed, clearly explain why with a ❌ indicator.

User request:
{user_input}

Backend structured result:
{json.dumps(agent_result, indent=2)}

Generate the highly structured Markdown response:
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        response = requests.post(
            self.url,
            json=payload,
            stream=True
        )

        if response.status_code == 200:
            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    chunk = json.loads(line.decode("utf-8"))

                    if chunk.get("done"):
                        break

                    if "response" in chunk:
                        yield chunk["response"]

                except json.JSONDecodeError:
                    continue

        else:
            yield "❌ Error: Unable to generate response from local model."

    