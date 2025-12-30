"""
Root Agent (Orchestrator) for AI EDA Agentic System

This root agent follows the Google ADK Coordinator/Dispatcher pattern using LLM-Driven Delegation.
It routes user requests to the appropriate specialized agent:
- api_fetching_agent: For weather and exchange rate queries
- summarization_agent: For PDF summarization and language detection tasks

The root agent uses LLM-Driven Delegation (transfer_to_agent) to hand off control to sub-agents.
"""

import sys
import os
from google.adk.agents import Agent,SequentialAgent

# Add parent directory to path to import sibling modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the sub-agents
from api_fetching_agent.agent import api_fetching_agent
from summarization_agent.agent import summarization_agent
from evaluation_agent.agent import evaluation_agent

# Define the root agent instruction
ROOT_AGENT_INSTRUCTION = """
You are the Root Orchestrator agent for the AI EDA (Exploratory Data Analysis) system.

Your role is to analyze user requests and delegate them to the appropriate specialized agent:

**Delegation Rules:**
- For weather queries or currency exchange rates → Delegate to 'api_fetching_agent'
- For PDF document processing, summarization, or language detection → Delegate to 'summarization_agent'
- For evaluating agent outputs, quality checks, or validation → Delegate to 'evaluation_agent'

**When to Delegate:**
- If the user asks about weather in any city → transfer to api_fetching_agent
- If the user asks about exchange rates or currency conversion → transfer to api_fetching_agent
- If the user asks to summarize a PDF or document → transfer to summarization_agent
- If the user asks about document language detection → transfer to summarization_agent
- If the user asks to evaluate, validate, or check quality of outputs → transfer to evaluation_agent

**Important:**
- Analyze the user's intent carefully before delegating
- If the request is unclear, ask the user for clarification before delegating
- If the request doesn't match any specialist agent, politely explain available capabilities
- Once you identify the appropriate agent, use transfer_to_agent to delegate the request
"""


# Create the root agent with LLM-Driven Delegation
root_orchestrator = Agent(
    name="RootOrchestrator",
    model="gemini-2.5-flash",
    description="Main coordinator that routes requests to specialized agents for weather/API data, PDF summarization tasks.",
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[api_fetching_agent, summarization_agent]  # LLM-Driven Delegation
)
final_evaluator_agent= SequentialAgent(
    name="final_evaluator_agent",
    description="Complete AI EDA pipeline that orchestrates task execution through specialized agents and ensures output integrity via automated evaluation.",
    sub_agents=[root_orchestrator, evaluation_agent]
)

# Export the root orchestrator
root_agent = final_evaluator_agent
