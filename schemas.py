from typing import List # this module provides support for type hints.
from pydantic import BaseModel, Field # those models are used for data validation and settings management using Python type annotations.


# this will help us get structured output from the agent 
class Source(BaseModel):
    """ Schema for a source used by the agent"""
    url: str = Field(description='The URL of the source')  # field is used to add a description to the url attribute

class AgentResponse(BaseModel):
    """ Schema for the agent response"""
    answer: str = Field(description="The agent's answer to the query")  
    sources: List[Source] = Field(default_factory=List, description="List of sources used to generate the answer")