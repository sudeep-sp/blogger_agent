#!/usr/bin/env python
from langtrace_python_sdk import langtrace
import sys
import warnings
import os
from crew import BloggerAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

langtrace.init(
    api_key=os.getenv("LANGTRACE_API_KEY"),
)


def run():
    """
    Run the crew.
    """
    input_topic = input("Enter the topic you want to write blog: ")
    inputs = {
        'topic': input_topic,
    }
    BloggerAgent().crew().kickoff(inputs=inputs)


run()
