# AI EDA Project

## Tasks Block Diagrams

### Task 1: Multi-Agent Orchestration
![Task 1 System Diagram](images/task1_system_diagram.png)

For Task 1, we developed a modular multi-agent system where each specific responsibility is handled by a dedicated agent. This architecture ensures clear separation of concerns:
- **Modular Design**: Each agent (API Fetching, Summarization, and Evaluation) is equipped with its own set of specialized **tools** and a dedicated **prompt file** for precise behavioral control.
- **Framework**: The system is built using the **Google-adk** framework, leveraging its capabilities for robust agent management and tool integration.

---

### Task 2: MCP-Based Architecture
![Task 2 System Diagram](images/task2_system_diagram.png)

Task 2 transitions the system to a Model Context Protocol (MCP) architecture, enhancing scalability and interoperability:
- **MCP Client**: A single agent acts as the MCP client, orchestrating requests across the environment.
- **MCP Servers**: Three distinct servers provide specialized services:
    1. **API Fetching Server**
    2. **Summarization Server**
    3. **Evaluation Server**

> **Note on Evaluation Logic**: The Evaluation Server is exclusively responsible for assessing the **summarization output**. We have omitted automated evaluation for the API fetching stage because the fetching server interacts directly with the ground truth (real API data). Evaluating the raw fetching output against itself would be redundant, as the server's primary role is to provide the factual data used in subsequent steps.
