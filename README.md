# AI Support Desk with Knowledge Routing Agent

An intelligent, multi-source support assistant built with **LangGraph**, **FastAPI**, and **Streamlit**. The system intelligently routes user queries to the appropriate data source—PostgreSQL, a Vector Knowledge Base, or an External Mock API—while maintaining a deterministic logic flow.

## Overview

This project implements a "Routing Agent" architecture that prioritizes correctness and data authority. It uses rule-based classification to ensure queries are handled by the correct internal tool before falling back to a static LLM response.

### Core Features

* **Intelligent Routing**: A deterministic `RouterNode` that classifies intent based on signal word priority.
* **Relational Data**: Real-time SQL queries against a PostgreSQL database for customer and ticket information.
* **Semantic Search**: Vector database (ChromaDB) search for support articles and policies using `all-MiniLM-L6-v2` embeddings.
* **External Mock API**: Predefined responses for real-world data like weather and cryptocurrency prices.
* **Multi-Turn History**: Maintains a sliding window of the last 10 messages for conversation context.

## Tech Stack

* **Orchestration**: LangGraph, LangChain
* **Backend**: FastAPI, Uvicorn
* **Frontend**: Streamlit
* **Database**: PostgreSQL (Relational), ChromaDB (Vector)
* **Models**: Sentence-Transformers (Embeddings)

## Project Structure

```text
AISupportDesk/
├── api/                # FastAPI endpoint logic
├── config/             # Environment and settings management
├── data/               # Static knowledge base articles
├── db/                 # SQL schema and seed data
├── docs/               # Project documentation and logic bibles
├── graph/              # LangGraph node definitions and wiring
├── router/             # Rule-based classification logic
├── testing/            # Phase-based unit and integration tests
├── tools/              # Tool implementations (Postgres, Vector, External)
├── run.py              # Main project runner
└── requirements.txt    # Python dependencies

```

## Logic & Priority

The system follows a strict **Routing Contract** to ensure predictable behavior:

1. **Vector DB Priority**: Queries regarding "How-to", "Policy", or "Escalation" take precedence to prevent knowledge queries from being trapped in database searches.
2. **Postgres Route**: Handles specific ticket IDs, customer status, and account-related info.
3. **External Route**: Mock API for general info (weather/crypto).
4. **LLM Fallback**: Provides a static system description or a "not enough information" response if no data is found.

## Setup & Installation

### 1. Prerequisites

* Python 3.10+
* PostgreSQL installed and running.

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=aiSupportDesk
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
HF_TOKEN=your_huggingface_token

```

### 3. Database Initialization

Run the SQL scripts provided in `/db` to set up your tables and seed data:

* `schema.sql`: Creates `customers` and `tickets` tables.
* `seed.sql`: Populates the database with test data (e.g., John Doe, Jane Smith, Alex Brown).

### 4. Installation

```bash
pip install -r requirements.txt

```

## Usage

Run the integrated runner to start both the FastAPI backend and the Streamlit UI:

```bash
python run.py

```

* **UI**: `http://localhost:8501`
* **API Docs**: `http://127.0.0.1:8000/docs`

## Testing

The project includes automated scripts for verifying tools and graph logic:

```bash
# Test individual tools
python testing/test_tools.py

# Test the router classification
python testing/test_router.py

# Test the full graph integration
python testing/test_graph.py

```

## Example Queries

* **Postgres**: "Show tickets for customer Alex Brown." or "Which city is customer 3 from?"
* **Vector**: "Explain ticket escalation." or "How do I reset my password?"
* **External**: "What is the price of Bitcoin?"
* **System**: "What can you do?"
