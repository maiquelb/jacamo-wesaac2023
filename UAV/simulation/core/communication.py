from dataclasses import dataclass
import time
from typing import List

@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    timestamp: float
    duration: float = 2.0

class CommunicationSystem:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, sender: str, receiver: str, content: str):
        message = Message(sender, receiver, content, time.time())
        self.messages.append(message)

    def update(self):
        self.messages = [m for m in self.messages
                        if time.time() - m.timestamp <= m.duration]