import openai
import os
import conversation
from document_store import DocumentStore

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


def trim(new_message):
    stopwords = ['<|SYSTEM|>', '<|USER|>', '<|ASSISTANT|>', '<|endoftext|>', 'Human:', 'AI:']

    earliest_ocurrence_index = len(new_message)

    for word in stopwords:
        index = new_message.find(word)
        if index != -1 and index < earliest_ocurrence_index:
            earliest_ocurrence_index = index

    if earliest_ocurrence_index != -1:
        return new_message[:earliest_ocurrence_index].strip()

    return new_message.strip()


def strip_after(string, words):
  for word in words:
    index = string.find(word)
    if index != -1:
      return string[:index]

  return string


def load_outside_context(doc_store, question):
    # Not Implemented
    return doc_store.query(question)


def chat():
    system_prompt = "<|SYSTEM|>The following is a conversation with an AI assistant. The assistant is helpful, " \
                    "creative, clever, and very friendly."
    opening_text = "Please ask a question about NIST 800.53"
    conversation_history = conversation.Conversation()
    doc_store = DocumentStore()
    doc_store.load_pdf("./data/")

    while True:
        question = input(opening_text + ": ")

        if not maintain_state or conversation_history.is_empty():
            conversation_history.clear()
            conversation_history.add_message("System", system_prompt)

        outside_context = load_outside_context(doc_store, question)

        conversation_history.add_message("AI", strip_keywords(opening_text))
        conversation_history.add_message("Human", strip_keywords(question))

        conversation_history.add_message("AI", "")

        starting_message = conversation_history.render_messages()

        compound_message = outside_context + starting_message

        response = openai.Completion.create(
            model="stablelm-3b",
            prompt=compound_message,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[]
        )

        response_text = response.choices[0].text
        new_message = remove_original_message(outside_context, response_text)
        new_message = remove_original_message(starting_message, new_message)
        new_message = trim(new_message)

        conversation_history.append_to_last_message("AI", new_message)
        print("AI: " + strip_keywords(new_message))


if __name__ == '__main__':
    chat()
