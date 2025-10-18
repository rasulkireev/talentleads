import math

from pydantic_ai import capture_run_messages

import structlog


def get_talentleads_logger(name):
    """This will add a `talentleads` prefix to logger for easy configuration."""

    return structlog.get_logger(
        f"talentleads.{name}",
        project="talentleads",
    )


logger = get_talentleads_logger(__name__)


def floor_to_thousands(x):
    return int(math.floor(x / 1000.0)) * 1000


def floor_to_tens(x):
    return int(math.floor(x / 10.0)) * 10


def run_agent_synchronously(agent, input_string, deps=None, function_name="", model_name=""):
    """
    Run a PydanticAI agent synchronously.

    Args:
        agent: The PydanticAI agent to run
        input_string: The input string to pass to the agent
        deps: Optional dependencies to pass to the agent

    Returns:
        The result of the agent run

    Raises:
        RuntimeError: If the agent execution fails
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    with capture_run_messages() as messages:
        try:
            logger.info(
                "[Run Agent Synchronously] Running agent",
                messages=messages,
                input_string=input_string,
                deps=deps,
                function_name=function_name,
                model_name=model_name,
            )
            if deps is not None:
                result = loop.run_until_complete(agent.run(input_string, deps=deps))
            else:
                result = loop.run_until_complete(agent.run(input_string))

            logger.info(
                "[Run Agent Synchronously] Agent run successfully",
                messages=messages,
                input_string=input_string,
                deps=deps,
                result=result,
                function_name=function_name,
                model_name=model_name,
            )
            return result
        except Exception as e:
            logger.error(
                "[Run Agent Synchronously] Failed execution",
                messages=messages,
                exc_info=True,
                error=str(e),
                function_name=function_name,
                model_name=model_name,
            )
            raise
