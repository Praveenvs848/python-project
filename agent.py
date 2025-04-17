from typing import Annotated

from typing_extensions import TypedDict
from langchain_core.messages import AIMessageChunk, HumanMessage,SystemMessage
import os
from dotenv import load_dotenv
from langgraph.graph.message import add_messages

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")




class State(TypedDict):
    messages: Annotated[list, add_messages]


from langchain_core.tools import tool


@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    return ["Cloudy with a chance of hail."]


tools = [search]
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo" , api_key=openai_api_key)

# model = model.bind_tools(tools)


from typing import Literal

from langchain_core.runnables import RunnableConfig

from langgraph.graph import END, START, StateGraph



# Define the function that calls the model
async def answer(state: State, config: RunnableConfig):
    messages = state["messages"]
    

    response = await model.ainvoke(messages, config)
    return {"messages": response}

async def usermessage(state: State, config: RunnableConfig):
    messages = state["messages"]
    prompt=[SystemMessage(content="""
    provide a short messeage to user about the response like a chatbot. The output should be in Markdown format.
    Don't include ``` markdown ``` into the response

""")]
    

    response = await model.ainvoke(messages+prompt, config)
    return {"messages": response}

# Define a new graph
workflow = StateGraph(State)

workflow.add_node("answer_agent", answer)
workflow.add_node("usermessage_agent", usermessage)


workflow.add_edge(START, "answer_agent")
workflow.add_edge("answer_agent","usermessage_agent")



# workflow.add_edge("tools", "agent")
workflow.add_edge("usermessage_agent", END)

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()


# from langchain_core.messages import AIMessageChunk, HumanMessage
# import asyncio

# async def gettt():
#     inputs = [HumanMessage(content="what is the weather in sf")]
#     first = True
#     gathered = None  # Initialize a variable to accumulate chunks of AI message

#     # Start streaming the responses
#     async for event in graph.astream_events({"messages": inputs}, version="v1"):
#         kind = event["event"]
#         print(f"{kind}: {event['name']}")
#         return event

# Run the asynchronous function
# asyncio.run(get())