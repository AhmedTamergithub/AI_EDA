#!/usr/bin/env python3
"""
Script to configure which agent is set as the root agent in Task 1 and Task 2.
Run the script and choose from the available agents interactively.
"""

import sys
import os
import re

# Define the agents and their corresponding files and root agent lines
agents = {
    'api_fetching': {
        'file': 'task1/api_fetching_agent/agent.py',
        'commented': '##root_agent = api_fetching_agent',
        'uncommented': 'root_agent = api_fetching_agent'
    },
    'summarization': {
        'file': 'task1/summarization_agent/agent.py',
        'commented': '##root_agent = summarization_agent',
        'uncommented': 'root_agent = summarization_agent'
    },
    'orchestrator': {
        'file': 'task1/Orchestrator/agent.py',
        'commented': '##root_agent = root_orchestrator',
        'uncommented': 'root_agent = root_orchestrator'
    },
    'evaluation': {
        'file': 'task1/evaluation_agent/agent.py',
        'commented': '##root_agent = evaluation_agent',
        'uncommented': 'root_agent = evaluation_agent'
    },
    'mcp_client': {
        'file': 'task2/agent.py',
        'commented': '##root_agent = mcp_agent',
        'uncommented': 'root_agent = mcp_agent'
    }
}

def configure_root_agent(agent_name):
    if agent_name not in agents:
        print(f"Error: Invalid agent name '{agent_name}'. Valid options: {', '.join(agents.keys())}")
        return

    # First, remove all root_agent lines from all files
    for name, config in agents.items():
        file_path = os.path.join(os.path.dirname(__file__), config['file'])
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            # Remove any lines containing root_agent
            content = re.sub(r'^.*root_agent.*$\n?', '', content, flags=re.MULTILINE)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Removed any root_agent lines from {config['file']}")

    # Then, add the root_agent line to the specified agent file
    config = agents[agent_name]
    file_path = os.path.join(os.path.dirname(__file__), config['file'])
    if os.path.exists(file_path):
        with open(file_path, 'a') as f:
            f.write('\n' + config['uncommented'] + '\n')
        print(f"Set {agent_name} as root agent in {config['file']}")
    else:
        print(f"Error: File {config['file']} not found")

if __name__ == "__main__":
    print("Available agents to set as root:")
    print("\nTask 1:")
    print("- api_fetching")
    print("- summarization")
    print("- orchestrator")
    print("- evaluation")
    print("\nTask 2:")
    print("- mcp_client")
    print()
    
    agent_name = input("Enter the agent name to set as root: ").strip().lower()
    if agent_name not in agents:
        print(f"Error: Invalid agent name '{agent_name}'. Valid options: {', '.join(agents.keys())}")
        sys.exit(1)
    
    configure_root_agent(agent_name)