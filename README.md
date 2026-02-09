# Data Agent

A CLI tool that lets you query your Supabase (PostgreSQL) database using natural language. Powered by Anthropic Claude and LangChain.

## Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com) project with a PostgreSQL database
- An [Anthropic API key](https://console.anthropic.com)

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd data-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the package

```bash
pip install -e .
```

This installs the `data-agent` CLI command and all dependencies (LangChain, SQLAlchemy, psycopg2, etc.).

### 4. Configure environment variables

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Where to find these:**

- **SUPABASE_URL** — Go to your Supabase dashboard > Project Settings > API. Copy the Project URL.
- **SUPABASE_SERVICE_KEY** — Same page, under "Project API keys", copy the `service_role` key (not the `anon` key). This key bypasses RLS and has full database access.
- **ANTHROPIC_API_KEY** — Go to [console.anthropic.com](https://console.anthropic.com) > API Keys > Create Key.

## Usage

### Basic query

Ask a natural language question about your database:

```bash
data-agent query "List all tables in the database"
data-agent query "Show me the top 10 users by signup date"
data-agent query "How many orders were placed last month?"
```

### RLS-scoped query

Query data filtered to a specific user (simulates Row Level Security):

```bash
data-agent query-rls --user-id abc123 "Show my orders"
data-agent query-rls --user-id user_456 "What are my recent transactions?"
```

This instructs the agent to always filter results by the given `user_id`.

### Multi-step process

Describe a complex, multi-step data operation in plain English:

```bash
data-agent process "Calculate monthly revenue totals and identify the top 3 months"
data-agent process "Find all inactive users who haven't logged in for 90 days and count them by signup source"
```

The agent will break the task into SQL steps, execute them sequentially, and return a summary.

### Help

```bash
data-agent --help
data-agent query --help
data-agent query-rls --help
data-agent process --help
```

## Project Structure

```
data-agent/
├── pyproject.toml              # Package config, dependencies, CLI entry point
├── .env.example                # Environment variable template
├── .gitignore
├── README.md
└── src/
    └── data_agent/
        ├── __init__.py         # Package exports
        ├── agent.py            # SupabaseQueryAgent class
        └── cli.py              # CLI entry point (argparse)
```

## How It Works

1. The agent connects to your Supabase PostgreSQL database via SQLAlchemy using the connection pooler
2. It uses LangChain's `SQLDatabaseToolkit` to give Claude access to SQL tools (list tables, describe schemas, run queries)
3. When you ask a question, Claude interprets it, writes the appropriate SQL, executes it, and returns a natural language answer

## Troubleshooting

**"Missing environment variable" error** — Make sure your `.env` file exists in the project root and contains all three variables (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `ANTHROPIC_API_KEY`).

**"Invalid SUPABASE_URL format" error** — The URL must be in the format `https://<project-ref>.supabase.co`. Check your Supabase dashboard for the correct URL.

**Connection errors** — Verify your `SUPABASE_SERVICE_KEY` is the service role key (not the anon key), and that your Supabase project is active and not paused.
