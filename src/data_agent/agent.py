import os
import re

from langchain_anthropic import ChatAnthropic
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langgraph.prebuilt import create_react_agent


class SupabaseQueryAgent:
    """SQL agent that connects to a Supabase PostgreSQL database and uses
    Anthropic Claude to answer natural language queries."""

    def __init__(self):
        supabase_url = os.environ["SUPABASE_URL"]
        supabase_key = os.environ["SUPABASE_SERVICE_KEY"]

        # Extract project ref from the Supabase URL
        match = re.match(r"https://([^.]+)\.supabase\.co", supabase_url)
        if not match:
            raise ValueError(
                f"Invalid SUPABASE_URL format: {supabase_url}. "
                "Expected https://<project-ref>.supabase.co"
            )
        project_ref = match.group(1)

        db_uri = (
            f"postgresql://postgres.{project_ref}:{supabase_key}"
            f"@aws-1-eu-west-2.pooler.supabase.com:5432/postgres"
        )

        self.db = SQLDatabase.from_uri(db_uri)
        self.llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.tools = toolkit.get_tools()

    def _run(self, prompt: str) -> str:
        agent = create_react_agent(self.llm, self.tools)
        result = agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )
        return result["messages"][-1].content

    def query(self, user_query: str) -> str:
        """Run a natural language query against the database."""
        return self._run(user_query)

    def query_with_rls(self, user_query: str, user_id: str) -> str:
        """Run a query scoped to a specific user via RLS."""
        prompt = (
            f"You are querying on behalf of user_id='{user_id}'. "
            f"Always filter results by this user_id. "
            f"User's question: {user_query}"
        )
        return self._run(prompt)

    def execute_process(self, process_description: str) -> str:
        """Execute a multi-step data process described in natural language."""
        prompt = (
            "You are a data processing agent. Break down the following task "
            "into SQL steps and execute them sequentially. Provide a summary "
            f"of what was done and the results.\n\nTask: {process_description}"
        )
        return self._run(prompt)
