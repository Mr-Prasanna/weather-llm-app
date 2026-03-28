# import os
# import re
# import streamlit as st
# import plotly.graph_objects as go
# from dotenv import load_dotenv
# from agent import run_agent
# from weather_tool import get_weather

# load_dotenv()
# os.environ["LANGCHAIN_TRACING_V2"] = "false"

# # ── Page config ──────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Weather AI Assistant",
#     page_icon="🌤️",
#     layout="wide"
# )

# # ── Title ────────────────────────────────────────────────────────────
# st.title("🌤️ Weather AI Assistant")
# st.caption("Powered by Groq LLaMA3 + OpenWeatherMap")

# # ── Session state ────────────────────────────────────────────────────
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "last_city" not in st.session_state:
#     st.session_state.last_city = None

# # ── Sidebar ──────────────────────────────────────────────────────────
# with st.sidebar:
#     st.header("⚙️ Settings")

#     units = st.radio(
#         "Temperature Unit",
#         options=["metric", "imperial"],
#         format_func=lambda x: "Celsius (°C)" if x == "metric" else "Fahrenheit (°F)"
#     )

#     st.divider()
#     st.markdown("**Quick city search:**")
#     quick_cities = ["Chennai", "Mumbai", "Delhi", "London", "New York", "Tokyo"]
#     for city in quick_cities:
#         if st.button(city, use_container_width=True):
#             st.session_state.quick_city = city

#     st.divider()
#     if st.button("🗑️ Clear chat history", use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.last_city = None
#         st.rerun()

# # ── City extractor ───────────────────────────────────────────────────
# def extract_city(text: str) -> str:
#     """
#     Extract city name from user input using regex patterns.
#     """
#     text = text.strip()

#     # Pattern: "weather in CITY" or "weather of CITY"
#     match = re.search(r'weather\s+(?:in|of|for)\s+([A-Za-z\s]+?)(?:\?|$|\.)', text, re.IGNORECASE)
#     if match:
#         return match.group(1).strip().title()

#     # Pattern: "in CITY" anywhere
#     match = re.search(r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
#     if match:
#         return match.group(1).strip().title()

#     # Pattern: last capitalized word
#     words = text.split()
#     for word in reversed(words):
#         if word[0].isupper() and word.lower() not in ["what", "how", "tell", "the", "is", "are"]:
#             return word.title()

#     return None

# # ── Chart function ───────────────────────────────────────────────────
# def show_weather_chart(city: str, units: str):
#     try:
#         data = get_weather(city, units)

#         if "error" in data:
#             st.error(f"Could not get weather data for {city}: {data['error']}")
#             return

#         if not data.get("forecast"):
#             st.warning("No forecast data available.")
#             return

#         unit_symbol = "°C" if units == "metric" else "°F"
#         dates = [f["date"] for f in data["forecast"]]
#         temps = [f["temp"] for f in data["forecast"]]
#         humidity = [f["humidity"] for f in data["forecast"]]
#         feels_like = [f["feels_like"] for f in data["forecast"]]

#         # ── Temperature chart ────────────────────────────────────────
#         fig = go.Figure()

#         fig.add_trace(go.Scatter(
#             x=dates, y=temps,
#             mode="lines+markers",
#             name=f"Temperature ({unit_symbol})",
#             line=dict(color="#FF6B6B", width=3),
#             marker=dict(size=8)
#         ))

#         fig.add_trace(go.Scatter(
#             x=dates, y=feels_like,
#             mode="lines+markers",
#             name=f"Feels Like ({unit_symbol})",
#             line=dict(color="#FFA500", width=2, dash="dash"),
#             marker=dict(size=6)
#         ))

#         fig.update_layout(
#             title=f"5-Day Temperature — {data['city']}, {data['country']}",
#             xaxis_title="Date",
#             yaxis_title=f"Temperature ({unit_symbol})",
#             hovermode="x unified",
#             height=350,
#             margin=dict(l=20, r=20, t=40, b=20)
#         )
#         # st.plotly_chart(fig, use_container_width=True)
#         st.plotly_chart(fig, width='stretch')

#         # ── Humidity chart ───────────────────────────────────────────
#         fig2 = go.Figure()
#         fig2.add_trace(go.Bar(
#             x=dates, y=humidity,
#             name="Humidity (%)",
#             marker_color="#4FC3F7"
#         ))
#         fig2.update_layout(
#             title="5-Day Humidity Forecast",
#             xaxis_title="Date",
#             yaxis_title="Humidity (%)",
#             height=300,
#             margin=dict(l=20, r=20, t=40, b=20)
#         )
#         st.plotly_chart(fig2, use_container_width=True)

#     except Exception as e:
#         st.error(f"Chart error: {str(e)}")


# # ── Chat history display ─────────────────────────────────────────────
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # ── Handle quick city buttons ────────────────────────────────────────
# if "quick_city" in st.session_state and st.session_state.quick_city:
#     city = st.session_state.quick_city
#     st.session_state.quick_city = None
#     st.session_state.last_city = city
#     user_input = f"What is the weather in {city}?"

#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     with st.chat_message("assistant"):
#         with st.spinner("Fetching weather..."):
#             response = run_agent(user_input)
#             st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

#     st.subheader(f"📊 Weather Charts for {city}")
#     show_weather_chart(city, units)
#     st.rerun()


# # ✅ New — charts stay persistent
# if user_input := st.chat_input("Ask about weather... e.g. What is the weather in Paris?"):

#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = run_agent(user_input)
#             st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

#     city = extract_city(user_input)
#     if city:
#         st.session_state.last_city = city

#     st.rerun()

# # ── Always show charts if city exists ────────────────────────────────
# if st.session_state.last_city:
#     st.subheader(f"📊 Weather Charts for {st.session_state.last_city}")
#     show_weather_chart(st.session_state.last_city, units)
# # ── Chat input ───────────────────────────────────────────────────────
# # if user_input := st.chat_input("Ask about weather... e.g. What is the weather in Paris?"):

#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = run_agent(user_input)
#             st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

#     # Extract city and show charts
#     city = extract_city(user_input)
#     if city:
#         st.session_state.last_city = city
#         st.subheader(f"📊 Weather Charts for {city}")
#         show_weather_chart(city, units)
#     else:
#         st.info("💡 Tip: Ask like — 'What is the weather in London?' to see charts")




import os
import re
import streamlit as st
import plotly.graph_objects as go

# ── Load secrets ──────────────────────────────────────────────────────
try:
    os.environ["OPENWEATHERMAP_API_KEY"] = st.secrets["OPENWEATHERMAP_API_KEY"]
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
    os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
    os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
    os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
except:
    from dotenv import load_dotenv
    load_dotenv()

from agent import run_agent
from weather_tool import get_weather

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weather AI Assistant",
    page_icon="🌤️",
    layout="wide"
)

# ── Title ────────────────────────────────────────────────────────────
st.title("🌤️ Weather AI Assistant")
st.caption("Powered by Groq LLaMA3 + OpenWeatherMap")

# ── Session state ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_city" not in st.session_state:
    st.session_state.last_city = None
if "quick_city" not in st.session_state:
    st.session_state.quick_city = None

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    units = st.radio(
        "Temperature Unit",
        options=["metric", "imperial"],
        format_func=lambda x: "Celsius (°C)" if x == "metric" else "Fahrenheit (°F)"
    )

    st.divider()
    st.markdown("**Quick city search:**")
    quick_cities = ["Chennai", "Mumbai", "Delhi", "London", "New York", "Tokyo"]
    for city in quick_cities:
        if st.button(city, use_container_width=True):
            st.session_state.quick_city = city

    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_city = None
        st.rerun()

# ── City extractor ───────────────────────────────────────────────────
def extract_city(text: str) -> str:
    text = text.strip()

    match = re.search(
        r'weather\s+(?:in|of|for)\s+([A-Za-z\s]+?)(?:\?|$|\.)',
        text, re.IGNORECASE
    )
    if match:
        return match.group(1).strip().title()

    match = re.search(r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    if match:
        return match.group(1).strip().title()

    words = text.split()
    for word in reversed(words):
        if word[0].isupper() and word.lower() not in [
            "what", "how", "tell", "the", "is", "are", "will"
        ]:
            return word.title()

    return None

# ── Chart function ───────────────────────────────────────────────────
def show_weather_chart(city: str, units: str):
    try:
        data = get_weather(city, units)

        if "error" in data:
            st.error(f"Could not get weather data for {city}: {data['error']}")
            return

        if not data.get("forecast"):
            st.warning("No forecast data available.")
            return

        unit_symbol = "°C" if units == "metric" else "°F"
        dates      = [f["date"]       for f in data["forecast"]]
        temps      = [f["temp"]       for f in data["forecast"]]
        humidity   = [f["humidity"]   for f in data["forecast"]]
        feels_like = [f["feels_like"] for f in data["forecast"]]

        # ── Temperature chart ────────────────────────────────────────
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=temps,
            mode="lines+markers",
            name=f"Temperature ({unit_symbol})",
            line=dict(color="#FF6B6B", width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=feels_like,
            mode="lines+markers",
            name=f"Feels Like ({unit_symbol})",
            line=dict(color="#FFA500", width=2, dash="dash"),
            marker=dict(size=6)
        ))
        fig.update_layout(
            title=f"5-Day Temperature — {data['city']}, {data['country']}",
            xaxis_title="Date",
            yaxis_title=f"Temperature ({unit_symbol})",
            hovermode="x unified",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Humidity chart ───────────────────────────────────────────
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=dates, y=humidity,
            name="Humidity (%)",
            marker_color="#4FC3F7"
        ))
        fig2.update_layout(
            title="5-Day Humidity Forecast",
            xaxis_title="Date",
            yaxis_title="Humidity (%)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Chart error: {str(e)}")


# ── Chat history display ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Handle quick city buttons ────────────────────────────────────────
if st.session_state.quick_city:
    city = st.session_state.quick_city
    st.session_state.quick_city = None
    st.session_state.last_city = city
    user_input = f"What is the weather in {city}?"

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Fetching weather..."):
            response = run_agent(user_input)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ── Chat input ───────────────────────────────────────────────────────
if user_input := st.chat_input("Ask about weather... e.g. What is the weather in Paris?"):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_agent(user_input)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    city = extract_city(user_input)
    if city:
        st.session_state.last_city = city

    st.rerun()

# ── Always show charts if city exists ────────────────────────────────
if st.session_state.last_city:
    st.subheader(f"📊 Weather Charts for {st.session_state.last_city}")
    show_weather_chart(st.session_state.last_city, units)