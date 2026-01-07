# 🚀 AI Dispatcher Agent

An **Agentic AI system** built using **FastAPI, LangGraph, and LangChain** that intelligently reads incoming user or stakeholder emails, classifies them, takes appropriate actions, and responds automatically.

The AI Dispatcher acts as a **virtual first-line support agent**, reducing manual triage effort and ensuring faster, consistent responses.

---

## 🧠 What This Agent Does

The AI Dispatcher Agent performs **end-to-end email triaging and handling**:

1. Reads incoming emails from users or stakeholders  
2. Classifies the email into one of the following categories:
   - 🚨 **Incident**
   - 🛠️ **Service Request**
   - ❓ **General Query**
3. Decides next actions based on classification  
4. Creates a ticket if required  
5. Generates and sends a contextual response back to the user  

All decisions are made using **LLM-driven reasoning orchestrated via LangGraph**.

---

## 🏗️ Architecture Overview

```text
Incoming Email
      ↓
Dispatcher Agent (LangGraph)
      ↓
Intent Classification
      ↓
┌───────────────────────────────┐
│ Incident | Service | Query    │
└───────────────────────────────┘
      ↓
Action Routing
      ↓
Ticket Creation (Optional)
      ↓
Automated Email Response
