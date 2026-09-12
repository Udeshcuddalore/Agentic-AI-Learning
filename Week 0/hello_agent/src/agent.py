"""
agent.py
--------
Wraps LangChain's pandas dataframe agent creation and the "ask a question"
call. This is the only module that talks to LangChain/OpenAI directly.
"""

from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_classic.agents.agent_types import AgentType

from config import settings
from src.prompts import build_full_prompt


def build_agent(dataframes: dict, api_key: str):
    """
    Builds a single LangChain agent that can reason over one or many
    DataFrames at once. LangChain's dataframe agent accepts either a single
    df or a list of dfs, so we just pass the values from our dict.
    """
    llm = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        api_key=api_key,
    )

    df_list = list(dataframes.values())
    print(df_list)
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df_list if len(df_list) > 1 else df_list[0],
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
        allow_dangerous_code=True,  # required by langchain_experimental to execute pandas code
        handle_parsing_errors=True,
    )
    return agent


def ask_question(agent, question: str) -> str:
    """
    Sends the constrained prompt to the agent and returns a plain-text answer.
    Any execution errors are caught and turned into a user-friendly message
    rather than a stack trace in the UI.
    """
    full_prompt = build_full_prompt(question)
    try:
        result = agent.invoke({"input": full_prompt})
        return result.get("output", str(result)).strip()
    except Exception as e:
        return f"Something went wrong while reading the data: {e}"