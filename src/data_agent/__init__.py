def __getattr__(name):
    if name == "SupabaseQueryAgent":
        from data_agent.agent import SupabaseQueryAgent
        return SupabaseQueryAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["SupabaseQueryAgent"]
