# # # # # # import os
# # # # # # from dotenv import load_dotenv
# # # # # # from langchain_openai import ChatOpenAI
# # # # # # from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# # # # # # from weather_tool import weather_tool

# # # # # # load_dotenv()

# # # # # # # ── 1. LLM ───────────────────────────────────────────────────────────
# # # # # # llm = ChatOpenAI(
# # # # # #     model="gpt-3.5-turbo",
# # # # # #     temperature=0.7
# # # # # # ).bind_tools([weather_tool])

# # # # # # # ── 2. Memory (simple list) ──────────────────────────────────────────
# # # # # # chat_history = []

# # # # # # # ── 3. System prompt ─────────────────────────────────────────────────
# # # # # # system_prompt = SystemMessage(content="""
# # # # # # You are a helpful weather assistant.
# # # # # # When user asks about weather, use the weather_tool to get real data.
# # # # # # Always mention temperature, humidity, wind speed and forecast clearly.
# # # # # # """)


# # # # # # # ── 4. Run agent ─────────────────────────────────────────────────────
# # # # # # def run_agent(user_input: str) -> str:

# # # # # #     # Add user message to history
# # # # # #     chat_history.append(HumanMessage(content=user_input))

# # # # # #     # Build messages list
# # # # # #     messages = [system_prompt] + chat_history

# # # # # #     # Call LLM
# # # # # #     response = llm.invoke(messages)

# # # # # #     # Check if LLM wants to call a tool
# # # # # #     if response.tool_calls:
# # # # # #         for tool_call in response.tool_calls:
# # # # # #             if tool_call["name"] == "weather_tool":

# # # # # #                 # Call the actual weather tool
# # # # # #                 tool_result = weather_tool.invoke(tool_call["args"])

# # # # # #                 # Add tool result back to messages
# # # # # #                 from langchain_core.messages import ToolMessage
# # # # # #                 messages.append(response)
# # # # # #                 messages.append(ToolMessage(
# # # # # #                     content=tool_result,
# # # # # #                     tool_call_id=tool_call["id"]
# # # # # #                 ))

# # # # # #                 # Get final response from LLM with tool data
# # # # # #                 final_response = llm.invoke(messages)
# # # # # #                 reply = final_response.content

# # # # # #     else:
# # # # # #         reply = response.content

# # # # # #     # Save assistant reply to memory
# # # # # #     chat_history.append(AIMessage(content=reply))

# # # # # #     return reply


# # # # # # # ── 5. Test ──────────────────────────────────────────────────────────
# # # # # # if __name__ == "__main__":

# # # # # #     print("=== Test 1 — Current weather ===")
# # # # # #     reply = run_agent("What is the weather in Chennai right now?")
# # # # # #     print("Agent:", reply)

# # # # # #     print("\n=== Test 2 — Memory test ===")
# # # # # #     reply = run_agent("What about the 5 day forecast for that city?")
# # # # # #     print("Agent:", reply)

# # # # # #     print("\n=== Test 3 — Different city ===")
# # # # # #     reply = run_agent("How is the weather in Mumbai?")
# # # # # #     print("Agent:", reply)


# # # # # import os
# # # # # import ssl
# # # # # from dotenv import load_dotenv
# # # # # from langchain_openai import ChatOpenAI
# # # # # from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# # # # # from weather_tool import weather_tool

# # # # # load_dotenv()

# # # # # # Disable LangSmith SSL issues
# # # # # os.environ["LANGCHAIN_TRACING_V2"] = "false"

# # # # # # ── 1. LLM ───────────────────────────────────────────────────────────
# # # # # llm = ChatOpenAI(
# # # # #     model="gpt-3.5-turbo",
# # # # #     temperature=0.7
# # # # # ).bind_tools([weather_tool])

# # # # # # ── 2. Memory ────────────────────────────────────────────────────────
# # # # # chat_history = []

# # # # # # ── 3. System prompt ─────────────────────────────────────────────────
# # # # # system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# # # # # # ── 4. Run agent ─────────────────────────────────────────────────────
# # # # # def run_agent(user_input: str) -> str:

# # # # #     chat_history.append(HumanMessage(content=user_input))
# # # # #     messages = [system_prompt] + chat_history
# # # # #     response = llm.invoke(messages)

# # # # #     if response.tool_calls:
# # # # #         for tool_call in response.tool_calls:
# # # # #             if tool_call["name"] == "weather_tool":
# # # # #                 tool_result = weather_tool.invoke(tool_call["args"])
# # # # #                 messages.append(response)
# # # # #                 messages.append(ToolMessage(
# # # # #                     content=tool_result,
# # # # #                     tool_call_id=tool_call["id"]
# # # # #                 ))
# # # # #                 final_response = llm.invoke(messages)
# # # # #                 reply = final_response.content
# # # # #     else:
# # # # #         reply = response.content

# # # # #     chat_history.append(AIMessage(content=reply))
# # # # #     return reply


# # # # # # ── 5. Test ──────────────────────────────────────────────────────────
# # # # # if __name__ == "__main__":
# # # # #     print("=== Test 1 ===")
# # # # #     reply = run_agent("What is the weather in Chennai right now?")
# # # # #     print("Agent:", reply)

# # # # #     print("\n=== Test 2 - Memory test ===")
# # # # #     reply = run_agent("What about the 5 day forecast for that city?")
# # # # #     print("Agent:", reply)


# # # # import os
# # # # from dotenv import load_dotenv
# # # # from langchain_groq import ChatGroq
# # # # from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# # # # from weather_tool import weather_tool

# # # # load_dotenv()

# # # # import httpx
# # # # import ssl

# # # # # Disable LangSmith tracing
# # # # # os.environ["LANGCHAIN_TRACING_V2"] = "false"

# # # # os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
# # # # os.environ["CURL_CA_BUNDLE"] = ""
# # # # os.environ["REQUESTS_CA_BUNDLE"] = ""
# # # # os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "")
# # # # os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
# # # # os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "weather-llm-app")
# # # # # ── 1. LLM ───────────────────────────────────────────────────────────
# # # # llm = ChatGroq(
# # # #     model="llama-3.3-70b-versatile",
# # # #     temperature=0.7,
# # # #     groq_api_key=os.getenv("GROQ_API_KEY")
# # # # ).bind_tools([weather_tool])

# # # # # ── 2. Memory ────────────────────────────────────────────────────────
# # # # chat_history = []

# # # # # ── 3. System prompt ─────────────────────────────────────────────────
# # # # system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# # # # # ── 4. Run agent ─────────────────────────────────────────────────────
# # # # def run_agent(user_input: str) -> str:

# # # #     chat_history.append(HumanMessage(content=user_input))
# # # #     messages = [system_prompt] + chat_history
# # # #     response = llm.invoke(messages)

# # # #     if response.tool_calls:
# # # #         for tool_call in response.tool_calls:
# # # #             if tool_call["name"] == "weather_tool":
# # # #                 tool_result = weather_tool.invoke(tool_call["args"])
# # # #                 messages.append(response)
# # # #                 messages.append(ToolMessage(
# # # #                     content=tool_result,
# # # #                     tool_call_id=tool_call["id"]
# # # #                 ))
# # # #                 final_response = llm.invoke(messages)
# # # #                 reply = final_response.content
# # # #     else:
# # # #         reply = response.content

# # # #     chat_history.append(AIMessage(content=reply))
# # # #     return reply


# # # # # ── 5. Test ──────────────────────────────────────────────────────────
# # # # if __name__ == "__main__":

# # # #     print("=== Test 1 - Current weather ===")
# # # #     reply = run_agent("What is the weather in Chennai right now?")
# # # #     print("Agent:", reply)

# # # #     print("\n=== Test 2 - Memory test ===")
# # # #     reply = run_agent("What about the 5 day forecast for that city?")
# # # #     print("Agent:", reply)

# # # #     print("\n=== Test 3 - Different city ===")
# # # #     reply = run_agent("How is the weather in Mumbai?")
# # # #     print("Agent:", reply)

# # # import os
# # # from dotenv import load_dotenv
# # # from langchain_groq import ChatGroq
# # # from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# # # from weather_tool import weather_tool

# # # load_dotenv()

# # # # ── LangSmith observability ──────────────────────────────────────────
# # # os.environ["LANGCHAIN_TRACING_V2"] = "true"
# # # os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# # # os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
# # # os.environ["LANGCHAIN_PROJECT"] = "weather-llm-app"

# # # # ── Fix SSL certificate error on office/corporate networks ───────────
# # # os.environ["SSL_CERT_FILE"] = ""
# # # os.environ["HTTPX_SSL_VERIFY"] = "0"

# # # import httpx
# # # import langsmith
# # # from langsmith import Client

# # # # Patch httpx to skip SSL verification for LangSmith
# # # os.environ["LANGCHAIN_VERIFY_SSL"] = "false"

# # # # ── 1. LLM ───────────────────────────────────────────────────────────
# # # llm = ChatGroq(
# # #     model="llama-3.3-70b-versatile",
# # #     temperature=0.7,
# # #     groq_api_key=os.getenv("GROQ_API_KEY")
# # # ).bind_tools([weather_tool])

# # # # ── 2. Memory ────────────────────────────────────────────────────────
# # # chat_history = []

# # # # ── 3. System prompt ─────────────────────────────────────────────────
# # # system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# # # # ── 4. Run agent ─────────────────────────────────────────────────────
# # # def run_agent(user_input: str) -> str:

# # #     chat_history.append(HumanMessage(content=user_input))
# # #     messages = [system_prompt] + chat_history
# # #     response = llm.invoke(messages)

# # #     if response.tool_calls:
# # #         for tool_call in response.tool_calls:
# # #             if tool_call["name"] == "weather_tool":
# # #                 tool_result = weather_tool.invoke(tool_call["args"])
# # #                 messages.append(response)
# # #                 messages.append(ToolMessage(
# # #                     content=tool_result,
# # #                     tool_call_id=tool_call["id"]
# # #                 ))
# # #                 final_response = llm.invoke(messages)
# # #                 reply = final_response.content
# # #     else:
# # #         reply = response.content

# # #     chat_history.append(AIMessage(content=reply))
# # #     return reply


# # # # ── 5. Test ──────────────────────────────────────────────────────────
# # # if __name__ == "__main__":

# # #     print("=== Test 1 - Current weather ===")
# # #     reply = run_agent("What is the weather in Chennai right now?")
# # #     print("Agent:", reply)

# # #     print("\n=== Test 2 - Memory test ===")
# # #     reply = run_agent("What about the 5 day forecast for that city?")
# # #     print("Agent:", reply)

# # #     print("\n=== Test 3 - Different city ===")
# # #     reply = run_agent("How is the weather in Mumbai?")
# # #     print("Agent:", reply)



# # # ------------

# # import os
# # import certifi
# # from dotenv import load_dotenv
# # from langchain_groq import ChatGroq
# # from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# # from weather_tool import weather_tool

# # load_dotenv()

# # # ── Fix SSL for corporate network ────────────────────────────────────
# # os.environ["SSL_CERT_FILE"] = certifi.where()
# # os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
# # os.environ["CURL_CA_BUNDLE"] = certifi.where()

# # # ── LangSmith setup ──────────────────────────────────────────────────
# # os.environ["LANGCHAIN_TRACING_V2"] = "true"
# # os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# # os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
# # os.environ["LANGCHAIN_PROJECT"] = "weather-llm-app"

# # # ── 1. LLM ───────────────────────────────────────────────────────────
# # llm = ChatGroq(
# #     model="llama-3.3-70b-versatile",
# #     temperature=0.7,
# #     groq_api_key=os.getenv("GROQ_API_KEY")
# # ).bind_tools([weather_tool])

# # # ── 2. Memory ────────────────────────────────────────────────────────
# # chat_history = []

# # # ── 3. System prompt ─────────────────────────────────────────────────
# # system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# # # ── 4. Run agent ─────────────────────────────────────────────────────
# # def run_agent(user_input: str) -> str:

# #     chat_history.append(HumanMessage(content=user_input))
# #     messages = [system_prompt] + chat_history
# #     response = llm.invoke(messages)

# #     if response.tool_calls:
# #         for tool_call in response.tool_calls:
# #             if tool_call["name"] == "weather_tool":
# #                 tool_result = weather_tool.invoke(tool_call["args"])
# #                 messages.append(response)
# #                 messages.append(ToolMessage(
# #                     content=tool_result,
# #                     tool_call_id=tool_call["id"]
# #                 ))
# #                 final_response = llm.invoke(messages)
# #                 reply = final_response.content
# #     else:
# #         reply = response.content

# #     chat_history.append(AIMessage(content=reply))
# #     return reply


# # # ── 5. Test ──────────────────────────────────────────────────────────
# # if __name__ == "__main__":

# #     print("=== Test 1 - Current weather ===")
# #     reply = run_agent("What is the weather in Chennai right now?")
# #     print("Agent:", reply)

# #     print("\n=== Test 2 - Memory test ===")
# #     reply = run_agent("What about the 5 day forecast for that city?")
# #     print("Agent:", reply)

# #     print("\n=== Test 3 - Different city ===")
# #     reply = run_agent("How is the weather in Mumbai?")
# #     print("Agent:", reply)


# import os
# import certifi
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# from langchain_core.tools import tool
# from weather_tool import weather_tool, get_weather

# load_dotenv()

# # ── SSL fix ──────────────────────────────────────────────────────────
# os.environ["SSL_CERT_FILE"] = certifi.where()
# os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# # ── LangSmith ────────────────────────────────────────────────────────
# os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
# os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "weather-llm-app")

# # ── LLM ──────────────────────────────────────────────────────────────
# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
#     groq_api_key=os.getenv("GROQ_API_KEY")
# ).bind_tools([weather_tool])

# # ── Memory ───────────────────────────────────────────────────────────
# chat_history = []

# # ── System prompt ────────────────────────────────────────────────────
# system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, always use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# # ── Run agent ────────────────────────────────────────────────────────
# def run_agent(user_input: str) -> str:

#     chat_history.append(HumanMessage(content=user_input))
#     messages = [system_prompt] + chat_history
#     response = llm.invoke(messages)

#     if response.tool_calls:
#         for tool_call in response.tool_calls:
#             if tool_call["name"] == "weather_tool":
#                 tool_result = weather_tool.invoke(tool_call["args"])
#                 messages.append(response)
#                 messages.append(ToolMessage(
#                     content=str(tool_result),
#                     tool_call_id=tool_call["id"]
#                 ))
#                 final_response = llm.invoke(messages)
#                 reply = final_response.content
#     else:
#         reply = response.content

#     chat_history.append(AIMessage(content=reply))
#     return reply


# if __name__ == "__main__":
#     print("=== Test 1 ===")
#     print(run_agent("What is the weather in Chennai?"))

#     print("\n=== Test 2 ===")
#     print(run_agent("How about Mumbai?"))




import os
import json
import certifi
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from weather_tool import get_weather_tool_fn, get_weather

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "weather-llm-app")


# ── Define tool here in agent.py directly ────────────────────────────
@tool
def weather_tool(city: str) -> str:
    """
    Use this tool to get current weather and 5 day forecast
    for any city. Input should be a city name like London,
    Chennai, Mumbai, Delhi, New York or Tokyo.
    """
    return get_weather_tool_fn(city)


# ── LLM ──────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY")
).bind_tools([weather_tool])

# ── Memory ───────────────────────────────────────────────────────────
chat_history = []

# ── System prompt ────────────────────────────────────────────────────
system_prompt = SystemMessage(content="You are a helpful weather assistant. When user asks about weather, always use the weather_tool to get real data. Always mention temperature, humidity, wind speed and forecast clearly.")


# ── Run agent ────────────────────────────────────────────────────────
def run_agent(user_input: str) -> str:
    chat_history.append(HumanMessage(content=user_input))
    messages = [system_prompt] + chat_history
    response = llm.invoke(messages)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "weather_tool":
                tool_result = weather_tool.invoke(tool_call["args"])
                messages.append(response)
                messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                ))
                final_response = llm.invoke(messages)
                reply = final_response.content
    else:
        reply = response.content

    chat_history.append(AIMessage(content=reply))
    return reply


if __name__ == "__main__":
    print("=== Test 1 ===")
    print(run_agent("What is the weather in Chennai?"))
    print("\n=== Test 2 ===")
    print(run_agent("How about Mumbai?"))
