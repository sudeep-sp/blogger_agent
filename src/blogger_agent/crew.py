from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llama_llm = LLM(
#     model="ollama/llama3.2",
#     base_url="http://localhost:11434"
# )
# groq_llm = LLM(
#     model=os.getenv("MODEL_G"),
#     temperature=0.7,
#     api_key=GROQ_API_KEY
# )


@CrewBase
class BloggerAgent():
    """BloggerAgent crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    llama_llm = LLM(
        model="ollama/llama3.2",
        base_url="http://localhost:11434"
    )

    groq_llm = LLM(
        model=os.getenv("MODEL_G"),
        temperature=0.7,
        api_key=GROQ_API_KEY
    )

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def Content_Strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['Content_Strategist'],
            verbose=True,
            tool=search_tool,
            llm=self.llama_llm
        )

    @agent
    def Creative_Blogger(self) -> Agent:
        return Agent(
            config=self.agents_config['Creative_Blogger'],
            verbose=True,
            llm=self.groq_llm
        )

    @agent
    def SEO_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['SEO_Analyst'],
            verbose=True,
            llm=self.llama_llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BloggerAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
