
import streamlit as st
import pandas as pd

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
from langchain.agents import AgentType

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="AI CSV Data Assistant",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 AI CSV Data Assistant")
st.markdown("Upload your CSV file and ask questions using natural language.")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("⚙️ Configuration")

groq_api_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# -------------------------------
# MAIN APPLICATION
# -------------------------------
if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("✅ CSV File Uploaded Successfully!")

    # Display Dataset
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Dataset Information
    st.subheader("📌 Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"Rows: {df.shape[0]}")

    with col2:
        st.info(f"Columns: {df.shape[1]}")

    with col3:
        st.info(f"Missing Values: {df.isnull().sum().sum()}")

    # User Query
    st.subheader("💬 Ask Questions About Your Data")

    user_question = st.text_area(
        "Enter your question:",
        placeholder="Example: What is the average salary?"
    )

    # Button
    if st.button("Generate Answer"):

        if not groq_api_key:
            st.error("❌ Please enter your Groq API Key")
        elif not user_question:
            st.error("❌ Please enter a question")
        else:

            with st.spinner("🤖 AI is analyzing your dataset..."):

                try:

                    # Load Groq LLM
                    llm = ChatGroq(
                        groq_api_key="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",
                        model_name="llama3-8b-8192"
                    )

                    # Create Pandas Agent
                    agent = create_pandas_dataframe_agent(
                        llm=llm,
                        df=df,
                        verbose=True,
                        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        allow_dangerous_code=True
                    )

                    # Generate Response
                    response = agent.run(user_question)

                    # Display Answer
                    st.subheader("✅ AI Response")
                    st.write(response)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

else:
    st.warning("📂 Please upload a CSV file to continue.")
