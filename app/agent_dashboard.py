import streamlit as st

from revit_bim_project.ai.agent import answer_bim_question
from revit_bim_project.ai.openai_agent import answer_bim_question_with_openai

from revit_bim_project.ai.openai_agent import (
    answer_bim_question_with_openai,
    generate_bim_quality_report,
)
from revit_bim_project.ai.openai_tool_agent import (
    answer_bim_question_with_tool_calling,
    answer_bim_question_with_tool_calling_debug,
)

st.set_page_config(
    page_title="BIM Intelligence Agent",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ BIM Intelligence Agent")

st.write(
    "Ask questions about the processed BIM room data. "
    "The agent can analyze floor areas, largest rooms, anomalies, materials, and building summaries."
)

st.sidebar.header("Agent settings")

agent_mode = st.sidebar.radio(
    "Choose agent mode:",
    [
        "OpenAI tool-calling agent",
        "OpenAI explanation agent",
        "Rule-based agent",
    ],
)

example_questions = [
    "Which floor has the most area?",
    "What are the largest rooms?",
    "Are there any suspicious rooms?",
    "Give me a BIM summary.",
    "What materials are used?",
]

selected_question = st.selectbox(
    "Try an example question:",
    [""] + example_questions,
)

custom_question = st.text_input(
    "Or ask your own question:",
    placeholder="Example: Which rooms should a BIM engineer review manually?",
)


st.divider()

st.subheader("Generate BIM Quality Report")

st.write(
    "Generate a structured report summarizing building area, largest rooms, "
    "detected anomalies, missing metadata, and recommended manual checks."
)

if st.button("Generate BIM Quality Report"):
    with st.spinner("Generating BIM quality report..."):
        report = generate_bim_quality_report()

    st.markdown(report)

question = custom_question or selected_question

if st.button("Ask BIM Agent"):
    if not question:
        st.warning("Please enter or select a question.")
    else:
        with st.spinner("Analyzing BIM data..."):
            if agent_mode == "OpenAI tool-calling agent":
                result = answer_bim_question_with_tool_calling_debug(question)
                answer = result["answer"]

                st.subheader("Agent answer")
                st.markdown(answer)

                with st.expander("Agent debug info"):
                    st.write(f"Elapsed time: {result['elapsed_seconds']:.2f} seconds")

                    if result["tool_calls"]:
                        st.write("Tools selected by OpenAI:")
                        for tool_call in result["tool_calls"]:
                            st.write(f"- `{tool_call['tool_name']}`")
                            st.json(tool_call["arguments"])
                    else:
                        st.write("No tool was called.")

            elif agent_mode == "OpenAI explanation agent":
                answer = answer_bim_question_with_openai(question)
                st.subheader("Agent answer")
                st.markdown(answer)

            else:
                answer = answer_bim_question(question)
                st.subheader("Agent answer")
                st.markdown(answer)

