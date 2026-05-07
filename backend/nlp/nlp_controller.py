from backend.nlp.intent_parser import IntentParser
from backend.agents.master_agent import MasterAgent
from backend.nlp.response_generator import ResponseGenerator

class NLPController:
    def __init__(self):
        self.parser = IntentParser()
        self.master_agent = MasterAgent()
        self.response_generator = ResponseGenerator()

    def process_user_input(self, user_input: str):
        parsed_intent = self.parser.parse(user_input)

        # If parsing failed, yield a user-friendly error instead of returning a raw dict
        if parsed_intent.get("status") == "failed":
            error_msg = parsed_intent.get("message", "I couldn't understand your request.")
            def error_stream():
                yield f"❌ **Request Failed**\n\n{error_msg}\n\nPlease try rephrasing your request."
            return error_stream()

        try:
            result = self.master_agent.process_request(
                agent_type=parsed_intent["agent_type"],
                command=parsed_intent["command"],
                **parsed_intent["parameters"]
            )
        except Exception as e:
            def exception_stream():
                yield f"❌ **Error Processing Request**\n\n{str(e)}\n\nPlease try again."
            return exception_stream()

        return self.response_generator.generate_response(
            user_input=user_input,
            agent_result=result
        )