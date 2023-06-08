import openai
import os
import conversation

# Put anything you want in `API key`
openai.api_key = 'Free the models'
# Point to your own url
openai.api_base = os.environ.get('REMOTE_API_URL')
debug = False
maintain_state = False


def strip_keywords(message):
    stopwords = ['<|SYSTEM|>', '<|USER|>', '<|ASSISTANT|>', '<|endoftext|>']

    if not debug:
        for word in stopwords:
            message = message.replace(word, '')

    return message

def remove_original_message(original_message, new_message):
    message = new_message.replace(original_message, '')
    return message


def trim(original_message, new_message):
    stopwords = ['<|SYSTEM|>', '<|USER|>', '<|ASSISTANT|>', '<|endoftext|>', 'Human: ', 'AI: ']

    if debug:
        print("-------------TRIM - PRE TRIM-------------")
        print(new_message)

    message = new_message.replace(original_message, '')
    message = strip_after(message, stopwords)
    if debug:
        print("-------------TRIM - POST TRIM-------------")
        print(message)
        print("-------------TRIM - END-------------")
    message = original_message + message

    return message


def strip_after(string, words):
  for word in words:
    index = string.find(word)
    if index != -1:
      return string[:index]

  return string


def load_outside_context():
    # Not Implemented
    return ""


def chat():
    system_prompt = "<|SYSTEM|>The following is a conversation with an AI assistant. The assistant is helpful, " \
                    "creative, clever, and very friendly."
    opening_text = "Please ask a question about NIST"
    conversation_history = conversation.Conversation()

    while True:
        question = input(opening_text + ": ")

        if not maintain_state or conversation_history.is_empty():
            conversation_history.clear()
            conversation_history.add_message("System", system_prompt)

        load_outside_context()

        conversation_history.add_message("AI", strip_keywords(opening_text))
        conversation_history.add_message("Human", strip_keywords(question))

        conversation_history.add_message("AI", "AI: ")

        starting_message = conversation_history.render_messages()

        response = openai.Completion.create(
            model="stablelm-3b",
            prompt=starting_message,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[]
        )

        response_text = response.choices[0].text
        new_message = remove_original_message(starting_message, response_text)

        conversation_history.append_to_last_message("AI", new_message)
        print(strip_keywords(new_message))


if __name__ == '__main__':
    chat()
