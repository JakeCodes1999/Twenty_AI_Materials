# Import necessary classes from CrewAI framework
from crewai import Agent, Crew, Task, Process, LLM

# -----------------------------------
# MODEL SETUP
# -----------------------------------

# Select the local Ollama model to use for all agents
model_selected = "ollama/qwen3:14b"  # Other options are commented out

# Initialize the LLM using Ollama with local endpoint
llm = LLM(
    model=model_selected,             # LLM model to be used
    base_url="http://localhost:11434",  # Local Ollama server
    api_key="ollama",                 # Dummy API key for local usage
    temperature=0.1                   # Low temperature for deterministic output
)

# -----------------------------------
# AGENT DEFINITIONS
# -----------------------------------

# Agent 1: Offensive cybersecurity specialist
NetworkPenTester = Agent(
    role="Offensive CyberSecurity Specialist",
    goal="To provide relevant high-quality attacks for target systems.",
    backstory="Years of industry red teaming experience, decorated and seasoned pen tester.",
    llm=llm,
    verbose=True,
    allow_delegation=True            # Allows this agent to delegate sub-tasks
)

# Agent 2: Risk analyst who evaluates attack options
RiskAnalyst = Agent(
    role="Risk Analyst",
    goal="Assess attack proposals and select best options.",
    backstory="Background in intelligence and offensive security as well as expertise in risk analysis.",
    llm=llm,
    verbose=True,
    allow_delegation=True
)

# Agent 3: Chief of Offensive Operations—oversees and delegates tasks
OffenseLead = Agent(
    role="Chief of Offensive Operations",
    goal="Examine tasking, select agent most appropriate for target, dispatch agent accordingly.",
    backstory="The Chief of Offensive Operations has rich background in cybersecurity with years of red teaming experience. However, as a chief they need to delegate to their security specialist.",
    llm=llm,
    verbose=True,
    allow_delegation=True
)

# -----------------------------------
# TASK DEFINITIONS
# -----------------------------------

# Task 1: Initial task to analyze input problem and assign the right agent
AnalyzeInputProblem = Task(
    description=(
        "Theres is a system with hostname fin-db.corp.local with ip 10.0.10.21 "
        "with role of hosting PostgreSQL for Finance data on OS: Ubuntu 24.04 LTS. "
        "Deligate an appropriate agent to attack this system."
    ),
    expected_output="Delegation of appropriate agent with justification for delegation decision. Information on target system to be included.",
    agent=OffenseLead,
    human_input=True                 # Indicates human-triggered input for this task
)

# Task 2: Penetration tester suggests 5 attack options with risk/reward scores
OffensiveOptions = Task(
    description="Recommend 5 different attack options, assign random risk and reward scores between 0 and 1 to each.",
    expected_output="5 options, Bulleted list with associated risk and reward score for each.",
    agent=NetworkPenTester
)

# Task 3: Risk analyst selects the best attack and justifies the decision
AttackSelection = Task(
    description="Assess the 5 attacks provided and select the best. Provide justification.",
    expected_output="The name of the best attack, and a confidence score in the decision (from 0 to 1) with justification.",
    agent=RiskAnalyst
)

# -----------------------------------
# CREW DEFINITION
# -----------------------------------

# Define the overall crew (process pipeline)
crew = Crew(
    agents=[NetworkPenTester, RiskAnalyst],       # Operational agents
    tasks=[AnalyzeInputProblem, OffensiveOptions, AttackSelection],  # Ordered tasks
    process=Process.hierarchical,                 # Tasks are handled in a hierarchy
    verbose=True,
    manager_agent=OffenseLead                     # Top-level decision-making agent
)

# -----------------------------------
# EXECUTION
# -----------------------------------

# Run the process if the script is executed directly
if __name__ == "__main__":
    print(crew.kickoff())  # Starts the hierarchical task execution