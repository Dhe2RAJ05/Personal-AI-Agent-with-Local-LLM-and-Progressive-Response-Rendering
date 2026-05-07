from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.gmail_agent import GmailAgent
from backend.agents.calendar_agent import CalendarAgent
from backend.agents.master_agent import MasterAgent
from backend.nlp.nlp_controller import NLPController
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="Personal Agent Backend",
    description="Local Agentic System Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gmail_agent = GmailAgent()
calendar_agent = CalendarAgent()
master_agent = MasterAgent()
nlp_controller = NLPController()

# Request model for sending email
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

class DraftSendRequest(BaseModel):
    draft_id: str

class CalendarEventRequest(BaseModel):
    summary: str
    start_time: str
    end_time: str

class CalendarDeleteRequest(BaseModel):
    event_id: str

class MasterRequest(BaseModel):
    agent_type: str
    command: str
    parameters: dict = {}

class NLPRequest(BaseModel):
    user_input: str

@app.get("/")
def root():
    return {
        "message": "Personal Agent Backend is running successfully"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "active"
    }


@app.post("/gmail/send")
def send_email(request: EmailRequest):
    return gmail_agent.process_command(
        command="send email",
        to=request.to,
        subject=request.subject,
        body=request.body
    )

@app.get("/gmail/read")
def read_emails(max_results: int = 5):
    return gmail_agent.process_command(
        command="read emails",
        max_results=max_results
    )

@app.get("/gmail/search")
def search_emails(sender_email: str, max_results: int = 5):
    return gmail_agent.process_command(
        command="search sender",
        sender_email=sender_email,
        max_results=max_results
    )

@app.get("/gmail/search-subject")
def search_emails_by_subject(subject_keyword: str, max_results: int = 5):
    return gmail_agent.process_command(
        command="search subject",
        subject_keyword=subject_keyword,
        max_results=max_results
    )

@app.post("/gmail/draft")
def draft_email(request: EmailRequest):
    return gmail_agent.process_command(
        command="draft email",
        to=request.to,
        subject=request.subject,
        body=request.body
    )

@app.get("/gmail/drafts")
def list_drafts(max_results: int = 10):
    return gmail_agent.process_command(
        command="list drafts",
        max_results=max_results
    )

@app.post("/gmail/send-draft")
def send_draft(request: DraftSendRequest):
    return gmail_agent.process_command(
        command="send draft",
        draft_id=request.draft_id
    )

@app.post("/calendar/create")
def create_calendar_event(request: CalendarEventRequest):
    return calendar_agent.process_command(
        command="create event",
        summary=request.summary,
        start_time=request.start_time,
        end_time=request.end_time
    )


@app.get("/calendar/events")
def list_calendar_events(max_results: int = 10):
    return calendar_agent.process_command(
        command="list events",
        max_results=max_results
    )

@app.get("/calendar/search-date")
def search_calendar_by_date(target_date: str):
    return calendar_agent.process_command(
        command="search date",
        target_date=target_date
    )

@app.post("/calendar/delete")
def delete_calendar_event(request: CalendarDeleteRequest):
    return calendar_agent.process_command(
        command="delete event",
        event_id=request.event_id
    )

@app.post("/master/process")
def process_master_request(request: MasterRequest):
    return master_agent.process_request(
        agent_type=request.agent_type,
        command=request.command,
        **request.parameters
    )

@app.post("/nlp/process")
def process_nlp(request: NLPRequest):
    response_stream = nlp_controller.process_user_input(request.user_input)

    return StreamingResponse(
        response_stream,
        media_type="text/plain"
    )