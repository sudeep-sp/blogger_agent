#!/usr/bin/env python
from langtrace_python_sdk import langtrace
import sys
import warnings
import os
from blogger_agent.crew import BloggerAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

langtrace.init(
    api_key=os.getenv("LANGTRACE_API_KEY"),
)


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI vs ML vs DL vs Data Science',
    }
    BloggerAgent().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI vs ML vs DL vs Data Science"
    }
    try:
        BloggerAgent().crew().train(n_iterations=int(
            sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        BloggerAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI vs ML vs DL vs Data Science"
    }
    try:
        BloggerAgent().crew().test(n_iterations=int(
            sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
