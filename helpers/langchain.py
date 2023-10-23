from langchain.chat_models import ChatOpenAI
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain
from langchain.utilities.serpapi import SerpAPIWrapper

def do_search(input, language="english"):
    model ='gpt-4'
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events",
        )
    ]

    prefix = """Answer the following questions as best you can. You have access to the following tools:"""
    suffix = """When answering, you MUST speak in the following language: {language}.

    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "language", "agent_scratchpad"],
    )

    llm_chain = LLMChain(llm=ChatOpenAI(model=model), prompt=prompt)

    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )

    return agent_executor.run(input=input, language=language)