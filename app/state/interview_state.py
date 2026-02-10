"""
Interview State Management

Manages the state of an interview session.
Uses Gradio session state to support concurrent users.
"""
from dataclasses import dataclass, field
from typing import List, Dict

from app.config.settings import settings


@dataclass
class InterviewState:
    """Manages the state of a single interview session.

    Each user session gets its own InterviewState instance
    via Gradio's gr.State to avoid shared global state.
    """

    chat_history: List[Dict[str, str]] = field(default_factory=list)
    job_choice: str = field(default_factory=lambda: settings.DEFAULT_JOB_CHOICE)
    max_question_amount: int = field(
        default_factory=lambda: settings.DEFAULT_MAX_QUESTIONS
    )
    question_count: int = 1
    resume_summary: str = ""

    def reset(self) -> None:
        """Reset the interview state to initial values."""
        self.chat_history = []
        self.job_choice = settings.DEFAULT_JOB_CHOICE
        self.question_count = 1
        self.resume_summary = ""
        self.max_question_amount = settings.DEFAULT_MAX_QUESTIONS

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        self.chat_history.append({"role": role, "content": content})

    def increment_question(self) -> None:
        """Increment the question counter."""
        self.question_count += 1

    @property
    def is_interview_complete(self) -> bool:
        """Check if the interview has reached the maximum questions."""
        return self.question_count >= self.max_question_amount

    @property
    def progress_percentage(self) -> float:
        """Calculate the interview progress as a percentage."""
        if self.max_question_amount == 0:
            return 0.0
        return (self.question_count / self.max_question_amount) * 100
