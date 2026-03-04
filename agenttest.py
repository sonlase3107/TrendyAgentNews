# ===============================
# 1️⃣ IMPORTS
# ===============================

from email import feedparser
from typing import Optional
from dataclasses import Field, dataclass

# LangChain OpenAI-compatible wrapper
from langchain_openai import ChatOpenAI

# LangChain message types
from langchain_core.messages import HumanMessage, SystemMessage

# LangChain tools
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool


# ===============================
# 2️⃣ CONFIGURATION
# ===============================
@dataclass
class LLMConfig:
    base_url: str
    model_name: str
    api_key: str = "not-needed"  # LMStudio does not require real API key

@tool("special_math_tool", return_direct=True)
def special_math_tool(a: float, b: float) -> float:
    """
    Compute special formula: (a + b)^2 - (a - b)
    """
    result = (a + b)**2 - (a - b)
    return result

class LLMAdapter:
    def __init__(self, config: LLMConfig):
        self.config = config

    # Using OpenAI-compatible wrapper
        self.llm = ChatOpenAI(
            base_url=self.config.base_url,
            model=self.config.model_name,
            api_key=self.config.api_key,
            temperature=0.2,
        )

        self.llm_with_tools = self.llm.bind_tools([special_math_tool])

    def handleUsersInput(self, input: str) -> str:
        response = self.llm_with_tools.invoke([HumanMessage(content=input)])
        return response
    
    def generate(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        # Send prompt to LLMs

        message = []
        if system_prompt:
            message.append(SystemMessage(system_prompt))

        message.append(HumanMessage(content=user_input))

        response = self.llm.invoke(message)
        
        return response.content

    

class AgentService:
    """
    High-level service layer.
    In future:
    - Add Intent Classifier
    - Add Planner
    - Add Tool Executor
    - Add Memory Orchestrator
    """
    def __init__(self, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter

    def handle_request(self, user_input:str) -> str:
        #Entrypoint of Users

        system_prompt = """
        You are an AI Agent Service with specific binding tools.
        Answer concisely and clearly.
        Understand the user query and use the special_math_tool when needed.
        """

        res = self.llm_adapter.handleUsersInput(user_input)
    
        if res.tool_calls:
            print(res)
            print(res.tool_calls)
            return f"Calling tools OK"

        return self.llm_adapter.generate(
            user_input=user_input,
            system_prompt=system_prompt
        )
    




def main():
    """
    Entry point for running the agent service locally.
    """

    # 1️⃣ Configure LMStudio connection
    lmStudioConfig = LLMConfig(
        base_url="http://localhost:1234/v1",
        model_name="deepseek/deepseek-r1-0528-qwen3-8b"
    )

    # 2️⃣ Initialize LLM Adapter
    adapter = LLMAdapter(config=lmStudioConfig)

    # 3️⃣ Initialize Agent Service
    agent = AgentService(adapter)

    # 4️⃣ Simple test
    print("=== AI Agent Service ===")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = agent.handle_request(user_input)

        print("\nAgent:", response)
        print()

if __name__ == "__main__":
    main()