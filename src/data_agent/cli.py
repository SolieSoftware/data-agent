import argparse
import sys

from dotenv import load_dotenv


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="data-agent",
        description="Query your Supabase database using natural language",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # query
    query_parser = subparsers.add_parser(
        "query", help="Run a natural language query"
    )
    query_parser.add_argument("user_query", help="The question to ask")

    # query-rls
    rls_parser = subparsers.add_parser(
        "query-rls", help="Run a query scoped to a user via RLS"
    )
    rls_parser.add_argument(
        "--user-id", required=True, help="The user ID for RLS scoping"
    )
    rls_parser.add_argument("user_query", help="The question to ask")

    # process
    process_parser = subparsers.add_parser(
        "process", help="Execute a multi-step data process"
    )
    process_parser.add_argument(
        "description", help="Description of the process to execute"
    )

    args = parser.parse_args()

    from data_agent.agent import SupabaseQueryAgent

    try:
        agent = SupabaseQueryAgent()
    except KeyError as e:
        print(f"Error: Missing environment variable {e}", file=sys.stderr)
        print(
            "Make sure SUPABASE_URL, SUPABASE_SERVICE_KEY, and "
            "ANTHROPIC_API_KEY are set (or defined in .env).",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.command == "query":
        result = agent.query(args.user_query)
    elif args.command == "query-rls":
        result = agent.query_with_rls(args.user_query, args.user_id)
    elif args.command == "process":
        result = agent.execute_process(args.description)

    print(result)
