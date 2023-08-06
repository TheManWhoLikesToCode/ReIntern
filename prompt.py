# Author: Jaydin F
# Date: 7/19/2023
# Purpose: Query openLLM models like GPT-3
import os
import asyncio
from typing import Union
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


async def query_llm(prompt):
    # Create an instance of Chatbot
    bot = await Chatbot.create()

    # Query the LLM with the provided prompt
    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)

    # Close the bot
    await bot.close()

    # Return the LLM's response
    return response['text']


def generate_weekly_email(tasks, name):
    # Convert the list of tasks into a string
    tasks_str = ', '.join(
        [f"{task['task']} on {task['date']}" for task in tasks])

    prompt = f"""
    You are an AI language model. Your task is to generate a weekly email for an intern named {name} based on their weekly activities. Here are the activities:

    {tasks_str}

    Now, let's break down these activities and translate them into key accomplishments, skills demonstrated, and contributions to the projects. 

    Start by identifying specific tasks and projects {name} has worked on. Highlight any technical skills {name} has demonstrated during these tasks. 

    Next, look for instances where {name} has shown soft skills such as communication and teamwork. 

    Then, identify any improvements or optimizations {name} has made. 

    Finally, summarize {name}'s contributions to the team and the project. 

    Based on this analysis, generate a paragraph for {name}'s weekly email to their boss from the first person perspective.
    
    Remember: Only output the emai and Write in FIRST PERSON.
    """

    # Query the LLM with the prompt
    response = asyncio.run(query_llm(prompt))

    # Process the response to create the email content
    email_content = response.split('. ')
    email_content = [email_content[0]] + \
        [item for item in email_content[1:] if item]

    email = '\n'.join(email_content)

    # Return the email
    return email


def generate_brag_sheet(summary, name):
    # Define the prompt
    prompt = """
    You are an AI language model. Your task is to generate a brag sheet for an intern named {name} based on their weekly activities. Here are the activities:

    {summary}

    Now, let's break down these activities and translate them into key accomplishments, skills demonstrated, and contributions to the projects. 

    Start by identifying specific tasks and projects {name} has worked on. Highlight any technical skills {name} has demonstrated during these tasks. 

    Next, look for instances where {name} has shown soft skills such as communication and teamwork. 

    Then, identify any improvements or optimizations {name} has made. 

    Finally, summarize {name}'s contributions to the team and the project. 

    Based on this analysis, generate 5 bullet points for {name}'s brag sheet.
    """.format(summary=summary, name=name)

    # Query the LLM with the prompt
    response = asyncio.run(query_llm(prompt))

    # Process the response to create a brag sheet
    brag_sheet = response.split('. ')
    brag_sheet = [brag_sheet[0]] + \
        ['* ' + item for item in brag_sheet[1:] if item]

    # Return the brag sheet
    return '\n'.join(brag_sheet)


# Example usage:
name = "Jaydin"
summary = """
   Monday: I started the week by attending a project kickoff meeting for a new client. I took detailed notes and was able to ask insightful questions about the client's needs.

   Tuesday: I spent the day working on a data analysis task for the new project. I used Python and pandas to clean the data and generate preliminary insights.

   Wednesday: I presented my initial findings to the project team. My clear communication and thorough analysis were appreciated by all team members.

   Thursday: I worked on improving the project's codebase. I refactored several key functions to improve readability and performance.

   Friday: I ended the week by documenting my work on the project. I created a detailed README file and commented my code to ensure that future team members can understand my work.
   """
# brag_sheet_bullets = generate_brag_sheet(summary, name)
# print(brag_sheet_bullets)
