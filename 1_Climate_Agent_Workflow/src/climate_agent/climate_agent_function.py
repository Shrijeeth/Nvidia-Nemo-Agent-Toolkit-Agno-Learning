import logging
from textwrap import dedent

from pydantic import Field

from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.component_ref import FunctionRef, LLMRef
from nat.data_models.function import FunctionBaseConfig


logger = logging.getLogger(__name__)


class ClimateAgentFunctionConfig(FunctionBaseConfig, name="climate_agent"):
    llm_name: LLMRef = Field(
        ...,
        description="Name of the LLM to use for knowledgeable climate science assistant",
    )
    tools: list[FunctionRef] = Field(..., description="The tools to use for the financial research and planner agents.")


@register_function(config_type=ClimateAgentFunctionConfig, framework_wrappers=[LLMFrameworkEnum.AGNO])
async def climate_agent_function(config: ClimateAgentFunctionConfig, builder: Builder):
    """
    Create a climate science assistant using AGNO framework
    to answer questions about climate science with appropriate
    facts and references.

    Parameters:
        config: Configuration for the climate science assistant
        builder: The NAT Builder instance

    Returns:
        A FunctionInfo object that can be used to build the climate science assistant
    """

    from agno.agent import Agent

    # Get the language model and tools
    llm = await builder.get_llm(config.llm_name, wrapper_type=LLMFrameworkEnum.AGNO)
    tools = await builder.get_tools(tool_names=config.tools, wrapper_type=LLMFrameworkEnum.AGNO)

    
    # Create climate agent
    climate_agent_system_message = dedent("""
    You are a knowledgeable climate science assistant. You help users understand 
    climate data, weather patterns, and global temperature trends. Be accurate, 
    informative, and cite scientific consensus when appropriate.

    Use the tools provided to answer the user's question and fetch the required 
    data required to answer the question. If the user's question is not related 
    to climate science, just say that you are not able to answer the question.
    """)
    climate_agent = Agent(
        name="climate_agent",
        model=llm,
        tools=tools,
        instructions=climate_agent_system_message,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    async def _arun(inputs: str) -> str:
        """
        Run the climate agent with the given inputs
        """
        try:
            climate_agent_response = await climate_agent.arun(inputs, stream=False)
            logger.debug(f"Climate agent response: {climate_agent_response}")
            if hasattr(climate_agent_response, "content"):
                climate_agent_response = climate_agent_response.content
            if isinstance(climate_agent_response, str):
                return climate_agent_response
            elif isinstance(climate_agent_response, list):
                return "\n".join(climate_agent_response)
            else:
                return str(climate_agent_response)
        except Exception as e:
            logger.error(f"Error running climate agent: {e}")
            return f"Sorry, I encountered an error while running the climate agent: {e}"

    yield FunctionInfo.from_fn(
        _arun,
        description="Climate agent function",
    )
