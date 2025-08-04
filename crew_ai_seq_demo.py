from crewai import Agent, Crew, Task, Process, LLM

model_selected = "ollama/qwen3:14b"
#model_selected = "ollama/deepseek-r1:8b"
#model_selected = "ollama/llama3:8b"
#initialize the ollama qwen3 model locally

llm = LLM(model=model_selected,
          base_url="http://localhost:11434",
          api_key="ollama",
          temperature=0.1)

NetworkPenTester = Agent(
    role      = "Researcher",
    goal      = "Offensive Cyber Security",
    backstory = "Recommends offensive security attack vectors.",
    llm       = llm,
    verbose   = True,
)

OffensiveOptions = Task(
    description     = "Recommend 5 different attack options, assign random risk and reward scores between 0 and 1 to each.",
    expected_output = "5 options, Bulleted list with associated risk and reward score for each.",
    agent           = NetworkPenTester,
)

RiskAnalyst = Agent(
    role      = "Risk Analyst",
    goal      = "Assess attack proposals and select best options.",
    backstory = "Background in inteligence and offensive security as well as expertise in risk analysis.",
    llm       = llm,
    verbose   = True,
)

AttackSelection = Task(
    description     ="Assess the 5 attacks provided and select the best. Provide justification.",
    expected_output ="The name of the best attack, and a confidence score in the decision (from 0 to 1) with justification.",
    agent           =RiskAnalyst,
)

crew = Crew(
    agents  = [NetworkPenTester, RiskAnalyst],
    tasks   = [OffensiveOptions, AttackSelection],
    process = Process.sequential,
    verbose = True,
)

if __name__ == "__main__":
    print(crew.kickoff())
