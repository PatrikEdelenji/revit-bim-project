import streamlit as st

from revit_bim_project.ai.agent import answer_bim_question
from revit_bim_project.ai.safe_agent import answer_bim_question_safely
from revit_bim_project.ai.openai_agent import (
    answer_bim_question_with_openai,
    generate_bim_quality_report,
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

if "messages" not in st.session_state:
    st.session_state.messages = []

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

    st.download_button(
        label="Download report as Markdown",
        data=report,
        file_name="bim_quality_report.md",
        mime="text/markdown",
    )

question = custom_question or selected_question

if st.button("Ask BIM Agent"):
    if not question:
        st.warning("Please enter or select a question.")
    else:
        with st.spinner("Analyzing BIM data..."):
            if agent_mode == "OpenAI tool-calling agent":
                result = answer_bim_question_safely(question)
                answer = result["answer"]

                st.subheader("Agent answer")
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "question": question,
                        "answer": answer,
                        "mode": agent_mode,
                    }
                )
                with st.expander("Agent debug info"):
                    if result["elapsed_seconds"] is not None:
                        st.write(f"Elapsed time: {result['elapsed_seconds']:.2f} seconds")
                    else:
                        st.write("Elapsed time: not available")
                    st.write(f"Mode: `{result['mode']}`")

                    if result["fallback_used"]:
                        st.warning("OpenAI failed, so the app used the local rule-based fallback.")
                        st.code(result["error"])

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

                st.session_state.messages.append(
                    {
                        "question": question,
                        "answer": answer,
                        "mode": agent_mode,
                    }
                )


            else:
                answer = answer_bim_question(question)

                st.subheader("Agent answer")
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "question": question,
                        "answer": answer,
                        "mode": agent_mode,
                    }
                )


st.divider()
st.subheader("Conversation History")

if st.button("Clear conversation history"):
    st.session_state.messages = []
    st.rerun()

for message in reversed(st.session_state.messages):
    with st.chat_message("user"):
        st.markdown(message["question"])

    with st.chat_message("assistant"):
        st.markdown(message["answer"])
        st.caption(f"Mode: {message['mode']}")