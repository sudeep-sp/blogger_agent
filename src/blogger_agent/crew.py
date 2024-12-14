from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

load_dotenv()


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@CrewBase
class BloggerAgent():
    """BloggerAgent crew"""

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

    openai_llm = LLM(
        model="gpt-4o-mini",
        temperature=0.7,
    )
    openai_4o = LLM(
        model="gpt-4o",
        temperature=0.7,
    )

    @agent
    def AI_Blog_Researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['AI_Blog_Researcher'],
            tool=[search_tool],
            llm=self.openai_llm
        )

    @agent
    def Content_Strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['Content_Strategist'],
            llm=self.openai_llm
        )

    @agent
    def Creative_Blogger(self) -> Agent:
        return Agent(
            config=self.agents_config['Creative_Blogger'],
            llm=self.openai_llm
        )

    @agent
    def SEO_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['SEO_Analyst'],
            llm=self.openai_llm
        )

    @task
    def blog_researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_researcher_task'],
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'],
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            return_output=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BloggerAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
