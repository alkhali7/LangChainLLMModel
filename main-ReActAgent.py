# this is the main file to run the ReAct agent example

# note for self: uv add python-dotenv in terminal to load environment variables from .env files
import os  # to access environment variables

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from langchain import hub     # where prompt templates are stored in langchain-hub
from langchain.agents import AgentExecutor # to execute the agent (the runtime method for agents)
from langchain.agents.react.agent import create_react_agent # the ReAct agent (llm + tools)
from langchain_ollama import OllamaLLM  # using gemma2 model since its free
from langchain_tavily import TavilySearch  # to access tavily search tool

tools = [
    TavilySearch()  # using tavily search tool
    ]
# configure an llm
llm = OllamaLLM(model='gemma2:2b', temperature=0)  # using gemma2 model since its free; need to Ollama pull gemma-2-2b first in terminal
# pulling the ReAct prompt template
react_prompt = hub.pull('hwchase17/react') #  (basis for all model technology)

agent = create_react_agent(llm,tools, react_prompt)   # creating the ReAct agent (returns a LLMChain)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # to execute the agent (verbose=True to see the thought process)
chain = agent_executor  # alias

def main():
    print("Hello from langchain-course! Creating a ReAct agent...")

    result = chain.invoke( 
        input = {'input': "search for 3 job postings for data scientist in Lansing area on LinkedIn and list their details"}
    )
    print(result)

if __name__ == "__main__":
    main()