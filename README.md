# Twenty_AI_Materials
Deliverables and Scripts Demonstrating Agentic Capabilities

Crew AI Heirarchy Demo:
Contains a crew made of three agents. The Cheif agent is responsible for delegating to two other agents, an offensive security specialist and 
a risk analyst. This structure is meant to mimic a design paradigm where there is one agent that provides attack vectors and another agent that assesses them, 
meanwhile a primary control agent makes the final decision based on the risks and rewards involved. 

This system could be expanded with tool usage, the attack vectors could be ingested as graphs from an nmap tool scan. The assessment of the viability of the attack vectors could be done by an RL model trained on hundreds of thousands of hypothetical nodes.

Crew AI Sequential demo serializes the process, demonstrating how simpler control paths with discrete logic execution flow can improve outcome stability and execution times.
