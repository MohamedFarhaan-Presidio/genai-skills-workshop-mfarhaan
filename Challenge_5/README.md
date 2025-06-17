# ❄️ Alaska Department of Snow – GenAI Online Agent

Welcome to the Alaska Department of Snow (ADS) Online Agent project. This repository demonstrates a fully architected and implemented Retrieval-Augmented Generation (RAG) chatbot system, integrating modern generative AI techniques using Google Cloud services.

> ✅ Goal: Alleviate high-volume resident inquiries regarding snow-related disruptions via a secure, cost-efficient, and scalable online GenAI agent.

---

## 📚 Table of Contents

- [❄️ Alaska Department of Snow – GenAI Online Agent](#️-alaska-department-of-snow--genai-online-agent)
  - [📚 Table of Contents](#-table-of-contents)
  - [🌐 High-Level Architecture](#-high-level-architecture)
  - [📦 Components Overview](#-components-overview)
    - [1. **Firestore**](#1-firestore)
    - [2. **BigQuery**](#2-bigquery)
    - [3. **Vertex AI**](#3-vertex-ai)
    - [4. **Cloud Run**](#4-cloud-run)
  - [🔄 Data Store Creation Flow](#-data-store-creation-flow)
  - [💬 Chat Flow - API Architecture](#-chat-flow---api-architecture)
  - [📡 RAG Query Lifecycle](#-rag-query-lifecycle)
  - [🛡️ LLM Response Validation](#️-llm-response-validation)
  - [💾 Session Management](#-session-management)
  - [✅ Features Implemented](#-features-implemented)
  - [🧪 Testing and Evaluation](#-testing-and-evaluation)
  - [🚀 Deployment](#-deployment)

---

## 🌐 High-Level Architecture

![Architecture Overview](API%20architecture.png)

This architecture integrates Firestore for chat history, Vertex AI for embeddings and LLM prompts, BigQuery for vector search, and Cloud Run for scalable backend services.

---

## 📦 Components Overview

### 1. **Firestore**
- Stores user sessions and chat history.
- Structure:


### 2. **BigQuery**
- Stores raw FAQ data and generated vector embeddings.
- Powers the vector similarity search (RAG).

### 3. **Vertex AI**
- Generates embeddings (`text-embedding-005`) and LLM completions using context-enhanced prompts.

### 4. **Cloud Run**
- Hosts two services:
- `agent-communication`: RAG logic
- `agent-response-validator`: Post-response safety checks

---

## 🔄 Data Store Creation Flow

![Data Store Creation](Flow%20diagram%20for%20creating%20datastore.png)

1. **Provision Access:** Assign Vertex AI + BigQuery roles.
2. **Embedding Setup:**
 - Remote embedding model connected in BigQuery.
 - Dataset created with embedded vectors.
3. **Serve as RAG Source:** This vector table is queried during user interactions.

---

## 💬 Chat Flow - API Architecture

![Chat Flow](API%20architecture.png)

1. `GET /get-user-session` – Retrieves chat history by user ID.
2. `GET /get-session` – Retrieves chat details using session ID.
3. `POST /agent-communication` – Sends query to LLM with relevant RAG context.
4. *(Optional)* `POST /agent-response-validator` – Ensures output adheres to safety/validation constraints.

---

## 📡 RAG Query Lifecycle

![RAG Flow](Querying%20RAG%20via%20cloud%20run.png)

1. User query ➜ Cloud Run ➜ Embedded by BigQuery.
2. Vector search returns top-k matches.
3. Prompt created with context + query ➜ sent to LLM.
4. Response returned to user via frontend.

---

## 🛡️ LLM Response Validation

![Validation Flow](LLM%20response%20validator.png)

- `agent-response-validator` receives the LLM's reply.
- Validates against predefined constraints (length, content safety, grounding).
- Returns YES/NO to approve or reject the output.

---

## 💾 Session Management

![Firestore Session](User%20session%20maintaince%20in%20firestore.png)

- Maintains persistent chat sessions using Firestore.
- Enables multi-turn dialogue and session continuity across frontend and backend.

---

## ✅ Features Implemented

- ✅ RAG system using BigQuery + Vertex AI embeddings
- ✅ Serverless backend via Cloud Run
- ✅ Real-time vector search
- ✅ Prompt engineering with dynamic context
- ✅ LLM response validation (content, safety, coherence)
- ✅ Session tracking via Firestore
- ✅ Fully documented Jupyter Notebooks and code
- ✅ Architecture diagrams included

---

## 🧪 Testing and Evaluation
- 🧠 Custom prompt-based response validation

---

## 🚀 Deployment

The system is deployed using:

- 🔹 **Vertex AI** for embedding and generation
- 🔹 **BigQuery** for vector search
- 🔹 **Cloud Run** for scalable backend APIs
- 🔹 **Firestore** for chat persistence

Frontend communicates with backend through secure REST APIs.
