from ollama import Client

client = Client(host='http://localhost:11434')
response = client.generate(
    model='deepseek-r1:1.5b',
    prompt='Explica la teoría de la relatividad en 3 líneas'
)
print(response['response'])