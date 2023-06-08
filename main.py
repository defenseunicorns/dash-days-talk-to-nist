import openai

prompt = "The following is a conversation with an AI assistant."
question = input("Please enter a NIST question question: ")
local_file_location = input("Please enter the location of a file that you would like to ")

# Put anything you want in `API key`
openai.api_key = 'Free the models'

# Point to your own url
openai.api_base = "https://leapfrogai.dd.bigbang.dev"
print(openai.Model.list())

response = openai.Completion.create(
  model="stablelm-3b",
  prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
  temperature=0.5,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  stop=["You:"]
)

response = openai.Completion.create(
  model="stablelm-3b",
  prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)
print(response.choices[0].text)