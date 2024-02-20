from langchain.chat_models import ChatOpenAI
from langchain.tools import format_tool_to_openai_function
from langchain.agents import initialize_agent, AgentType
from tools import InvestingAdvisorTool
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()


@cl.langchain_factory(use_async=False)
def agent():
    tools = [InvestingAdvisorTool()]
    functions = [format_tool_to_openai_function(t) for t in tools]
    llm = ChatOpenAI(temperature=0, model="gpt-4")

    open_ai_agent = initialize_agent(
        tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
    )

    return open_ai_agent
