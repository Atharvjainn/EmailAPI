from pydantic import BaseModel,Field
from datetime import date
from typing import List,Literal

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
  reason: str = Field(description="Short explanation")

class DeadlineList(BaseModel):
  deadlines : list[Deadline]
