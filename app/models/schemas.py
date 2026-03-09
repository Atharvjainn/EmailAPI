from pydantic import BaseModel,Field
from datetime import date
from typing import List,Literal
from app.lib.utils import today

class Email(BaseModel):
    id : str
    subject : str
    body : str

class EmailRequest(BaseModel):
    userId : str
    emails : List[Email]

class Deadline(BaseModel):
  subject: str = Field(description="Email subject")
  deadline: date = Field(description="ISO date of deadline or event")
  types: Literal["Deadline","Event"] = Field(description="Specify whether it is an event or deadline")
  urgency: int = Field(description="Urgency from 1 to 10")

class DeadlineList(BaseModel):
  deadlines : list[Deadline]


def prompt_template(context):
    prompt = f"""
    Today's date is {today}.

    You are an AI assistant that analyzes emails to detect time-sensitive information.

    Your task is to extract either:

    1) DEADLINES
    2) EVENTS

    Definitions:

    A DEADLINE means the recipient must COMPLETE, SUBMIT, PAY, RENEW,
    RESPOND, or FINISH something BEFORE that date.

    An EVENT is something that happens on a specific future date
    (meeting, interview, exam, appointment, celebration, lunch, call, etc.)
    but does NOT require completing something beforehand.

    Rules:
    - If an event is recurring (e.g., every Monday), include only the NEXT upcoming occurrence based on today's date.
    - Convert relative expressions like "next Friday", "tomorrow",
      "in 3 days", "next week" into ISO format (YYYY-MM-DD)
      based on today's date.
    - Ignore emails with no future time reference.
    - Only include future dates.
    - Be conservative. Do not guess.
    - When interpreting relative dates, calculate them strictly based on today's date.
    - Do not guess vague phrases like "sometime next month". Ignore them.
    - Return structured output only.

    Urgency Guidelines (1–10 scale):
    - 9–10 → Critical (within 1–2 days or severe consequence)
    - 7–8 → High (within a week or important obligation)
    - 4–6 → Medium (normal scheduled event or moderate importance)
    - 1–3 → Low (casual meeting, social event)

    For each item return:
    - subject
    - deadline (ISO format)
    - urgency
    - types (Event or Deadline)

    Emails:
    {context}
    """
    return prompt

