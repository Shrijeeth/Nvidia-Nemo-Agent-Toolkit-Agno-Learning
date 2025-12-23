import os
import json
from typing import Literal

from pydantic import BaseModel, Field

from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig

from .utils.climate_tools import (
    load_climate_data,
    calculate_statistics,
    filter_by_country,
    find_extreme_years,
    create_visualization,
    list_countries
)
from .utils.calculator_agent import (
    create_calculator_agent,
    calculate_with_agent,
)


current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, "data/temperature_annual.csv")


# 1. Input schemas tell LLM what each tool expects
class CalculateStatsInput(BaseModel):
    country: str = Field(
        default="",
        description="Country name to filter by (e.g., 'United States', 'France'). Leave empty for global statistics."
    )


class FilterCountryInput(BaseModel):
    country_name: str = Field(
        description="Country name to filter by (e.g., 'United States', 'France', 'Japan')"
    )


class FindExtremeInput(BaseModel):
    n: int = Field(
        default=5,
        description="Number of years to return"
    )
    extreme_type: str = Field(
        default="warmest",
        description="Type of extreme: 'warmest' or 'coldest'"
    )


class CreateVisualizationInput(BaseModel):
    plot_type: Literal["annual_trend", "country_comparison", "monthly_pattern"] = Field(
        default="annual_trend",
        description=(
            "Type of plot to create:\n"
            "- 'annual_trend': Shows temperature trend over years (global or for specific country)\n"
            "- 'country_comparison': Automatically finds and displays the TOP 5 COUNTRIES with highest warming trends\n"
            "- 'monthly_pattern': Shows average temperature by month (requires monthly data)"
        )
    )
    country: str = Field(
        default="",
        description="Country name to focus on (only used for 'annual_trend' and 'monthly_pattern'). Leave empty for global. Ignored for 'country_comparison' which always shows top 5."
    )
    save_path: str = Field(
        default="climate_plot.png",
        description="Path to save the plot image"
    )


class CalculatorInput(BaseModel):
    question: str = Field(
        description="A mathematical question or calculation request"
    )


# Config classes for each tool
class CalculateStatisticsConfig(FunctionBaseConfig, name="calculate_statistics"):
    """Configuration for calculating climate statistics."""
    pass


class ListCountriesConfig(FunctionBaseConfig, name="list_countries"):
    """Configuration for listing available countries."""
    pass


class FilterByCountryConfig(FunctionBaseConfig, name="filter_by_country"):
    """Configuration for filtering by country."""
    pass


class FindExtremeYearsConfig(FunctionBaseConfig, name="find_extreme_years"):
    """Configuration for finding extreme years."""
    pass


class CreateVisualizationConfig(FunctionBaseConfig, name="create_visualization"):
    """Configuration for creating visualizations."""
    pass

class CalculatorAgentConfig(FunctionBaseConfig, name="calculator_agent"):
    """Configuration for the mathematical calculator agent."""
    pass


# Register tools using clean wrapper pattern
@register_function(
    config_type=CalculateStatisticsConfig,
    framework_wrappers=[LLMFrameworkEnum.AGNO],
)
async def calculate_statistics_tool(config: CalculateStatisticsConfig, builder: Builder):
    """Register tool for calculating climate statistics."""
    # Load data once at startup
    df = load_climate_data(DATA_PATH)
    
    # 2. Wrapper uses pre-loaded data and ensures string output
    async def _wrapper(country: str = "") -> str:
        # Treat empty string as None for the underlying function
        country_param = None if country == "" else country
        result = calculate_statistics(df, country_param)
        return result  # Already returns JSON string
    
    # 3. Description tells LLM when to use the tool
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=CalculateStatsInput,
        description=("Calculate temperature statistics globally or for a specific country. "
                     "Returns JSON with: mean_temperature (°C), min_temperature (°C), max_temperature (°C), "
                     "std_deviation (°C), num_records (count), trend_per_decade (°C/decade), "
                     "years_analyzed (e.g. '1950-2025'), and country (if specified).")
    )


@register_function(
    config_type=ListCountriesConfig,
    framework_wrappers=[LLMFrameworkEnum.AGNO],
)
async def list_countries_tool(config: ListCountriesConfig, builder: Builder):
    """Register tool for listing available countries."""
    df = load_climate_data(DATA_PATH)
    
    async def _wrapper(dummy: str = "") -> str:
        # NAT requires at least one parameter, even if unused
        result = list_countries(df)
        return result  # Already returns JSON string
    
    yield FunctionInfo.from_fn(
        _wrapper,
        description="List all available countries in the climate dataset. Use this when unsure what countries are available."
    )


@register_function(
    config_type=FilterByCountryConfig,
    framework_wrappers=[LLMFrameworkEnum.AGNO],
)
async def filter_by_country_tool(config: FilterByCountryConfig, builder: Builder):
    """Register tool for filtering by country."""
    df = load_climate_data(DATA_PATH)
    
    async def _wrapper(country_name: str) -> str:
        result = filter_by_country(df, country_name)
        return result  # Already returns JSON string
    
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=FilterCountryInput,
        description="Get information about climate data for a specific country including number of stations and years covered."
    )


@register_function(
    config_type=FindExtremeYearsConfig,
    framework_wrappers=[LLMFrameworkEnum.AGNO],
)
async def find_extreme_years_tool(config: FindExtremeYearsConfig, builder: Builder):
    """Register tool for finding extreme years."""
    df = load_climate_data(DATA_PATH)
    
    async def _wrapper(n: int = 5, extreme_type: str = "warmest") -> str:
        result = find_extreme_years(df, n, extreme_type)
        return result  # Already returns JSON string
    
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=FindExtremeInput,
        description="Find the warmest or coldest years in the global temperature dataset."
    )


@register_function(
    config_type=CreateVisualizationConfig,
    framework_wrappers=[LLMFrameworkEnum.AGNO],
)
async def create_visualization_tool(config: CreateVisualizationConfig, builder: Builder):
    """Register tool for creating visualizations."""
    df = load_climate_data(DATA_PATH)
    
    async def _wrapper(
        plot_type: str,
        country: str = "",
        save_path: str = "climate_plot.png"
    ) -> str:
        # Treat empty string as None for the underlying function
        country_param = None if country == "" else country
        result = create_visualization(df, plot_type, country_param, save_path)
        return result  # Already returns string
    
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=CreateVisualizationInput,
        description=(
            "Create and save climate data visualizations. "
            "For 'country_comparison' plot type, it AUTOMATICALLY finds and visualizes the TOP 5 countries "
            "with highest warming trends - no need to calculate trends separately. "
            "Also creates annual temperature trends and monthly patterns using 'annual_trend' and 'monthly_pattern' plot types."
        )
    )


@register_function(config_type=CalculatorAgentConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def calculator_agent_tool(config: CalculatorAgentConfig, builder: Builder):
    """Register the LangGraph calculator agent as a NAT tool."""
    
    # Get the LLM from the builder - lifted from config
    # Use LANGCHAIN wrapper since we're using LangGraph (built on LangChain)
    llm = await builder.get_llm("calculator_llm", wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    # llm = await builder.get_llm("calculator_llm", wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    
    # Create the calculator agent with the NAT-provided LLM
    calculator_agent = create_calculator_agent(llm)
    
    async def _wrapper(question: str) -> str:
        # Use the calculator agent to process the question
        result = calculate_with_agent(question, calculator_agent)
        
        # Format the response as a JSON string
        response = {
            "calculation_steps": result["steps"],
            "final_result": result["final_result"],
            "explanation": result["explanation"]
        }
        return json.dumps(response, indent=2)
    
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=CalculatorInput,
        description=(
            "Calculates compound growth rates, percentage changes, weighted averages, "
            "projections, and multi-step calculations. Shows all calculation steps. "
            "Does not have access to climate data. If calculations need to be performed on climate data, "
            "be sure to acquire that data with other tools before including it in the input question to this tool."
        )
    )