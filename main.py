import openai
import os

# Put anything you want in `API key`
openai.api_key = 'Free the models'
# Point to your own url
openai.api_base = os.environ.get('REMOTE_API_URL')
debug = True
maintain_state = True


def parse(message):
    stopwords = ['<|SYSTEM|>', '<|USER|>', '<|ASSISTANT|>', '<|endoftext|>']

    if not debug:
        for word in stopwords:
            message = message.replace(word, '')

    return message


def trim(original_message, new_message):
    stopwords = ['<|SYSTEM|>', '<|USER|>', '<|ASSISTANT|>', '<|endoftext|>']

    message = new_message.replace(original_message, '')
    message = strip_after(message, stopwords)
    message = original_message + message

    return message


def strip_after(string, words):
  for word in words:
    index = string.find(word)
    if index != -1:
      return string[:index]

  return string


def chat():
    system_prompt = "<|SYSTEM|>The following is a conversation with an AI assistant. The assistant is helpful, " \
                    "creative, clever, and very friendly."
    opening_text = "Please ask a question about NIST"
    combined_prompt = ""

    while True:
        question = input(opening_text + ": ")
        # local_file_location = input("Please enter the location of a file that you would like to ")

        if not maintain_state or combined_prompt == "":
            combined_prompt = system_prompt + "\n<|ASSISTANT|>AI: " + opening_text + "\n<|USER|>Human: "

        combined_prompt += question + "\n<|ASSISTANT|>AI:"

        response = openai.Completion.create(
            model="stablelm-3b",
            prompt=combined_prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[]
        )

        response_text = response.choices[0].text

        if maintain_state:
            combined_prompt = response_text

            if debug:
                print("-------------STATE START-------------")
                print(combined_prompt)
                print("-------------STATE END-------------")

        parsed_text = parse(response_text)
        parsed_prompt = parse(combined_prompt)
        trimmed_text = trim(parsed_prompt, parsed_text)

        print(trimmed_text)


if __name__ == '__main__':
    chat()
