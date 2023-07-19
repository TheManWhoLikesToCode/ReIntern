# Author: Jaydin F
# Date: 7/19/2023
# Purpose: Query openLLM models like GPT-3

import openllm


def query_llm(prompt):

    # Create an HTTPClient pointed to the openLLM server
    client = openllm.client.HTTPClient('http://0.0.0.0:3000')

    # Query the LLM with the provided prompt
    response = client.query(prompt)

    # Return the LLM's response
    return response

def generate_brag_sheet(summary, name):

    # Define the prompt
    prompt = """
    Act as an internship assistant for an intern {name} who has completed their weekly internship and sent me their day-to-day work for this week:

    {summary}

    Based on this, provide 5 bullet points I can add to {name}'s brag sheet that emphasize their key accomplishments, skills demonstrated, and contributions to the projects from this week in a positive and impressive way:
    """.format(summary=summary, name=name)

    # Query the LLM with the prompt
    response = query_llm(prompt)

    # Process the response to create a brag sheet
    brag_sheet = response.split('. ')
    brag_sheet = [brag_sheet[0]] + ['* ' + item for item in brag_sheet[1:] if item]

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

brag_sheet_bullets = generate_brag_sheet(summary, name)

print(brag_sheet_bullets)

