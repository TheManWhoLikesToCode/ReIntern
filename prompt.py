# Author: Jaydin F
# Date: 7/19/2023
# Purpose: Query openLLM models like GPT-3

import openllm

# To Start the openLLM server:
# openllm server flan-t5

def query_llm(prompt):
  """
  Query an openLLM model with a provided prompt.
  
  Args:
    prompt (str): The prompt to provide to the LLM.  
  Returns:
    response (str): The LLM-generated response to the prompt.
  """
  
  # Create an HTTPClient pointed to the openLLM server
  client = openllm.client.HTTPClient('http://0.0.0.0:3000') 
  
  # Query the LLM with the provided prompt  
  response = client.query(prompt)
  
  # Return the LLM's response
  return response

# Example usage:
prompt = "What is the meaning of life?"
print(query_llm(prompt))