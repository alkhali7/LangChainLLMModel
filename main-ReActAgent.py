# this is the main file to create and run a ReAct agent using an llm model and tools returning a string response
# since gemm2 model is limited it cannot access real-time information like job postings, however if we used a more capable model like gpt-4-turbo it would work
# but gpt-4-turbo is not free, so we will use gemma2
import os  # to access env variables
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from langchain import hub                                   # where prompt templates are stored in langchain-hub
from langchain.agents import AgentExecutor                              # to execute the agent
from langchain.agents.react.agent import create_react_agent             # the ReAct agent (llm + tools)
from langchain_ollama import OllamaLLM                                  # using gemma2 model since its free
from langchain_tavily import TavilySearch                               # to access tavily search tool

from langchain_core.output_parsers.pydantic import PydanticOutputParser  # to parse the output of the agent
from langchain_core.prompts import PromptTemplate                       # to create a prompt template
from langchain_core.runnables import RunnableLambda

from prompt import REACT_PROMPT_FOR_GEMMA                # custom ReAct prompt template
from schemas import AgentResponse                                    # custom pydantic schema for the agent response

tools = [TavilySearch(name="tavily_search")]
llm = OllamaLLM(model="gemma2:2b", temperature=0)           # using gemma2 model; free; need to Ollama pull gemma-2-2b first in terminal

react_prompt = hub.pull("hwchase17/react")                  # pulling the ReAct prompt template

# output_parser = PydanticOutputParser(pydantic_object=AgentResponse)         # to parse the output of the agent according to the AgentResponse schema
from langchain.output_parsers import OutputFixingParser

output_parser = OutputFixingParser.from_llm(
    llm=llm,
    parser=PydanticOutputParser(pydantic_object=AgentResponse)
)
# creating a prompt template with custom ReAct prompt for --gpt-4-turbo--
# react_prompt_with_format_instructions = PromptTemplate(
#             template=REACT_PROMPT_FOR_GEMMA,
#             input_variables=['input','agent_scratchpad','tool_names']).
#             partia(format_instructions= output_parser.get_format_instructions())

from prompt import REACT_PROMPT_FOR_GEMMA

react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_FOR_GEMMA,
    input_variables=["input", "agent_scratchpad"],
    partial_variables={
        "tools": "\n".join([tool.name for tool in tools]),
        "tool_names": ", ".join([tool.name for tool in tools]),
        "format_instructions": output_parser.get_format_instructions(),
    },
)

agent = create_react_agent(llm = llm, tools=tools, prompt=react_prompt_with_format_instructions)  # creating the ReAct agent (returns a LLMChain)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)  # to execute the agent (verbose=True to see the thought process)
chain = agent_executor  # alias

def main():
    print("Hello from langchain-course! Creating a ReAct agent...")

    result = chain.invoke(
        input={
            "input": "search for 3 job postings for data scientist in Lansing area on LinkedIn and list their details"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
