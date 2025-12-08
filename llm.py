import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.messages import HumanMessage,SystemMessage


load_dotenv()



# This Function should take the datadog inputs from the webhook/ or the saved database , 
# Also check if we had this alert previously and what was the RCA and Solutions for them.
def failure_solution_lookup():
    pass


# Summarize the error and provide possible solution to the engineer.
def summarize_alerts(alert_message : str) -> str:
    # Initialize Groq model
    llm = ChatGroq(
        model_name="openai/gpt-oss-120b",   # or "llama3-70b-8192"
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
                You are a Senior Engineer and the Operations Manager of a large-scale data platform.
                Your job is to analyze FAILURE ALERTS coming from pipelines, cloud services, databases,
                integration systems, and monitoring tools.

                Your responsibilities:
                1. Read and understand the failure alert in detail.
                2. Extract the key issue and summarize it in clear, concise language.
                3. Explain *why* the failure happened (root cause reasoning).
                4. Provide *possible solutions* and recommended next actions an engineer should take.
                5. If data is missing, state what additional information is needed.

                Your tone:
                - Professional, senior-level, and precise.
                - Clear and actionable for support engineers.
                - No unnecessary details or assumptions.

                Output format:
                - **Summary**
                - **Root Cause Explanation**
                - **Possible Solutions**
                - **Next Recommended Actions**

                Each of the points in ouput format should not contain more than 50 words.
            """
        ),
        (
            "human",
            """
                Here is the failure alert:
                {alert_text}
                Analyze it and provide the required summary and solutions.
            """
        )
    ])
    chain = prompt | llm
    response = chain.invoke({"alert_text": alert_message})
    return response.content

alert = "Copy activity 'CopyCustomersToSQL' failed due to SQL pool timeout. The dedicated SQL pool did not respond within the configured timeout."
summarisation = summarize_alerts(alert)
print(summarisation)