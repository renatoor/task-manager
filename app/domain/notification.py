from typing import Protocol


class Notification(Protocol):
    def send_email(self, email: str, content: str):
        """Send email"""
