from dataclasses import dataclass
from typing import Tuple, List
import time

@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    timestamp: float
    duration: float = 2.0  # Message visualization duration in seconds

    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.duration

class CommunicationSystem:
    def __init__(self):
        self.messages = []

    def add_message(self, sender: str, receiver: str, content: str):
        message = Message(
            sender=sender,
            receiver=receiver,
            content=content,
            timestamp=time.time()
        )
        self.messages.append(message)

    def update(self):
        # Remove expired messages
        self.messages = [m for m in self.messages if not m.is_expired()]