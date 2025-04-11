import json
from chat_api_handel import OllamaChatAPIHandler
from prompts import PROMPTS   
import logging

# Initialize Logger
logger = logging.getLogger(__name__)

def analyze_dataframe(
    dataframes_list: list,
    dataframe_names: list,
    prompt_name: str,
    country_code: str,
) -> dict:
    """
    Analyze a list of DataFrames using OllamaChatAPIHandler with a specified prompt.

    Args:
        dataframes_list (list): List of pandas DataFrames to analyze.
        dataframe_names (list): List of names corresponding to each DataFrame.
        prompt_name (str): The name of the prompt to use from PROMPTS dictionary.
        country_code (str, optional): Country code to focus on in the analysis. Defaults to "US".

    Returns:
        dict: A dictionary containing individual responses for each DataFrame and a summary.

    Raises:
        ValueError: If the number of DataFrames doesn’t match the number of names, or if the prompt_name is invalid.
    """
    # Validate inputs
    if len(dataframes_list) != len(dataframe_names):
        raise ValueError(
            f"Number of DataFrames ({len(dataframes_list)}) must match number of names ({len(dataframe_names)})."
        )

    if not dataframes_list:
        raise ValueError("DataFrames list cannot be empty.")

    if prompt_name not in PROMPTS:
        raise ValueError(
            f"Prompt '{prompt_name}' not found in PROMPTS. Available prompts: {list(PROMPTS.keys())}"
        )

    # Check for empty DataFrames
    for df, name in zip(dataframes_list, dataframe_names):
        if df is None or df.empty:
            logger.warning(
                f"DataFrame '{name}' is empty or None. Skipping analysis for this DataFrame."
            )
            return {"individual_responses": [], "summary": "No valid data to analyze."}

    # Analyze each DataFrame individually
    individual_responses = []
    for df, name in zip(dataframes_list, dataframe_names):
        try:
            # Prepare the prompt
            prompt_template = PROMPTS[prompt_name]
            prompt = prompt_template.format(
                df_name=name,
                json_data1=df.to_json(orient="split", index=False),
                country_code=country_code,
            )
            # Call Ollama API
            response = OllamaChatAPIHandler.api_call(prompt)
            individual_responses.append({"df_name": name, "response": response})
            logger.info(
                f"Successfully analyzed DataFrame '{name}' with prompt '{prompt_name}'"
            )
        except Exception as e:
            logger.error(f"Error analyzing DataFrame '{name}': {e}")
            individual_responses.append(
                {"df_name": name, "response": f"Error: {str(e)}"}
            )

    # Generate summary
    try:
        all_responses = "\n\n".join(
            [f"{r['df_name']}:\n{r['response']}" for r in individual_responses]
        )
        summary_prompt = PROMPTS["summary_applicants_inventors"].format(
            all_responses=all_responses
        )
        summary_response = OllamaChatAPIHandler.api_call(summary_prompt)
        logger.info("Summary generated successfully")
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        summary_response = f"Error generating summary: {str(e)}"

    return {
        "individual_responses": individual_responses, 
        "summary": summary_response
    }
