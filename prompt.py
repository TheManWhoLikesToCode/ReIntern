import openllm
client = openllm.client.HTTPClient('http://localhost:3000')
prompt = "Insert Propmt Engineered Prompt Here"
print(client.query(prompt))
