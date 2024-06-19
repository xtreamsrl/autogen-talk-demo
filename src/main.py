import os
import autogen
from dotenv import load_dotenv

load_dotenv()


def run_agents(link: str, query: str):
    llm_config = {
        "config_list": [{"model": os.environ["OPENAI_MODEL"],
                         "api_key": os.environ["OPENAI_API_KEY"]}],
    }

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
    )

    coder = autogen.AssistantAgent(
        name="Coder",
        description="A helpful assistant highly skilled in evaluating a given code snippet.",
        llm_config=llm_config,
    )

    sw_eng = autogen.AssistantAgent(
        name="Software_Engineer",
        description="A helpful assistant highly skilled in evaluating a given code snippet.",
        system_message="""SoftwareEngineer. You are a helpful assistant highly skilled in evaluating a given code snippet 
        by providing a score from 1 (bad) to 10 (good) while providing clear rationale. Specifically, you can carefully 
        evaluate the code across the following dimensions:
        - syntax error: are there any syntax error or typos in the code? If ANY syntax error exists, the bug score MUST 
        be less than 5
        - logic errors: there are some logic errors that may prevent the code from running as expected? If ANY logic 
        error exists, the bug score MUST be less than 5
    YOU MUST PROVIDE A SCORE for each of the above dimensions.
    {syntax error: 0, logic errors: 0} Do not suggest code, just evaluate it.
    Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
    """,
        llm_config=llm_config,
    )

    dataviz_specialist = autogen.AssistantAgent(
        name="Data_Visualization_Specialist",
        description="A helpful assistant highly skilled in evaluating a given code snippet for data visualization.",
        system_message="""Data Visualization Specialist. You are a helpful assistant highly skilled in evaluating if a 
        given code will produce the desired data visualization output. You can provide a score from 1 (bad) to 10 (good) 
        while providing clear rationale. Specifically, you can carefully evaluate the code across the following dimensions:
        - Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is
    the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field
    first converted to a date object etc?
    - Goal compliance (compliance): how well the code meets the specified visualization goals?
    - Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and
    intent? Is there a visualization type that would be more effective in conveying insights? If a different
    visualization type is more appropriate, the score MUST BE LESS THAN 5.
    - Data encoding (encoding): Is the data encoded appropriately for the visualization type?
    - aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?
    YOU MUST PROVIDE A SCORE for each of the above dimensions.
    {transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0} Do not suggest code, just evaluate it.
    Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
    """,
        llm_config=llm_config,
    )

    groupchat = autogen.GroupChat(agents=[user_proxy, coder, dataviz_specialist, sw_eng], messages=[], max_round=20)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager,
        message=f"download data from {link} and use it to plot something that reply to the following query: {query}. "
                f"Save the plot to a file named results.png",
    )

if __name__ == "__main__":
    run_agents("https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv",
               "plot a visualization that tells us about the relationship between weight and horsepower")
