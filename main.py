import os  # to access environment variables

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_ollama import OllamaLLM  # instead of ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()  # take environment variables from .env.


def main():
    print("Hello from langchain-course!")
    # print(os.environ.get("OPENAI_API_KEY" ))
    information = """
        Elon Musk
        Musk in 2022 Senior Advisor to the Presidentarture from the Department of Government Efficiency
        Recorded May 30, 2025. This article is part of a series about June 28, 1971) is an international businessman and entrepreneur known for his leadership of Tesla, SpaceX, X (formerly Twitter), and the Department of Government Efficiency (DOGE). Musk has been the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion.
        Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada; he had obtained Canadian citizenship at birth through his Canadian-born mother. He received bachelor's degrees in 1997 from the University of Pennsylvania in Philadelphia, United States, before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became an American citizen.
    """
    summary_template = """ 
    Given the following information {information} about a person, I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOllama(
        temperature=0, model="gemma3:270m"
    )  # using Ollama instead of ChatOpenAI
    chain = (
        summary_prompt_template | llm
    )  # creating a chain with the prompt and the LLM
    response = chain.invoke(
        input={"information": information}
    )  # invoking the chain with the information

    print(response.content)  # printing the response


if __name__ == "__main__":
    main()
