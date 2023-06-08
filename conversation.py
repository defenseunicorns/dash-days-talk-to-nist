class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, sender, content):
        self.messages.append(Message(sender, content))

    def display_conversation(self):
        for message in self.messages:
            print(f"{message.sender}: {message.content}")

    def is_empty(self):
        return len(self.messages) == 0
    
    def clear(self):
        self.messages = []

    def render_messages(self):
        combined_messages = ""
        for message in self.messages:
            prefix = ""
            if message.sender == "AI":
                prefix = "<|ASSISTANT|>"
            elif message.sender == "Human":
                prefix = "<|USER|>"
            elif message.sender == "System":
                prefix = "<|SYSTEM|>"
            combined_messages += f"{prefix}{message.sender}: {message.content}\n"
        return combined_messages.strip()

    def append_to_last_message(self, sender, content):
        if self.messages and self.messages[-1].sender == sender:
            self.messages[-1].content += " " + content
        else:
            self.add_message(sender, content)


class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content