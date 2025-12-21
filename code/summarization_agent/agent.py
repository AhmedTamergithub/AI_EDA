import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from prompt import system_prompt

root_agent = Agent(
    name="summarization_agent",
    model="gemini-1.5-flash",
    description=(
        "Agent that recieves a PDF as an input and extract text from it , then perform chunking and summarization for each chunk, and provide a combined summary for the pdf , also it detects the language of the PDF."
    ),
    instruction=system_prompt,
    tools=[]
)  