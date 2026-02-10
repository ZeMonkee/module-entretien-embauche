"""
UI Event Handlers

Handles all UI events and user interactions.
Includes navigation functions for the wizard and interview logic.

All interview state is managed per-session via gr.State (InterviewState).
"""
import logging
import time

import gradio as gr

from app.config.settings import settings
from app.state import InterviewState
from app.services.llm_service import llm_service
from app.services.audio_service import audio_service
from app.services.document_service import document_service
from app.ui.components import (
    create_progress_html,
    create_completed_progress_html,
    create_summary_card,
    create_wizard_header,
)

logger = logging.getLogger(__name__)

NUM_SECTIONS = 7

SECTION_LANDING = 0
SECTION_JOB = 1
SECTION_RESUME = 2
SECTION_QUESTIONS = 3
SECTION_SUMMARY = 4
SECTION_LOADING = 5
SECTION_INTERVIEW = 6


def _show_section(active_index: int) -> list:
    """Return a list of gr.update() to show only the section at `active_index`.

    Args:
        active_index: Index of the section to display (0-based)

    Returns:
        List of NUM_SECTIONS gr.update() calls
    """
    return [
        gr.update(visible=(i == active_index))
        for i in range(NUM_SECTIONS)
    ]


def change_interactivity(enable: bool):
    """Toggle interactivity of a component."""
    return gr.update(interactive=enable)


def enable_submit(text: str):
    """Enable submit button when text is not empty."""
    return gr.update(interactive=bool(text and text.strip()))


# === Navigation Handlers ===


def go_to_job_page():
    """Navigate from landing to job page."""
    return _show_section(SECTION_JOB)


def go_to_resume_page(job: str):
    """Navigate from job page to resume page (validates job is filled)."""
    if not job or not job.strip():
        return [gr.update() for _ in range(NUM_SECTIONS)]
    return _show_section(SECTION_RESUME)


def go_to_questions_page():
    """Navigate from resume page to questions page."""
    return _show_section(SECTION_QUESTIONS)


def go_to_summary_page(job: str, resume_file, nb_questions: int):
    """Navigate to summary page with entered data."""
    has_resume = resume_file is not None
    summary_html = create_summary_card(job, has_resume, int(nb_questions))

    return _show_section(SECTION_SUMMARY) + [gr.update(value=summary_html)]


def go_back_to_job():
    """Navigate back to job page."""
    return _show_section(SECTION_JOB)


def go_back_to_resume():
    """Navigate back to resume page."""
    return _show_section(SECTION_RESUME)


def go_back_to_questions():
    """Navigate back to questions page."""
    return _show_section(SECTION_QUESTIONS)


# === Interview Handlers ===


def show_loading_and_start(
    job_chosen: str, resume_file, nb_questions: int, state: InterviewState
):
    """Show loading animation and start interview.

    Uses a Gradio generator to show loading first, then transition
    to the interview once the first question is generated.

    Args:
        job_chosen: The job position selected
        resume_file: Optional uploaded resume file path
        nb_questions: Number of questions for the interview
        state: Per-session InterviewState instance

    Yields:
        Tuple of Gradio updates for UI components + updated state
    """
    # First yield: show loading page
    yield (
        _show_section(SECTION_LOADING)
        + [
            gr.update(),  # progress_indicator
            gr.update(),  # assistant_output
            gr.update(),  # user_answer_input
            gr.update(),  # submit_answer_btn
            gr.update(),  # user_text_input
            gr.update(),  # reset_interview_btn
            state,
        ]
    )

    # Reset and configure state for new interview
    state.reset()
    state.job_choice = job_chosen.strip()
    state.max_question_amount = int(nb_questions)
    state.question_count = 1

    # Process resume if provided
    if resume_file is not None:
        logger.info("Processing uploaded resume...")
        state.resume_summary = document_service.summarize_resume(resume_file)

    # Generate first question
    first_question = llm_service.generate_response(
        settings.INTERVIEW_PROMPT_PATH,
        job_choice=state.job_choice,
        max_questions=state.max_question_amount,
        resume_summary=state.resume_summary,
        chat_history=state.chat_history,
    )
    state.add_message("assistant", first_question)

    progress_html = create_progress_html(state)

    # Minimum loading time for animation
    time.sleep(1.5)

    # Second yield: show interview page
    yield (
        _show_section(SECTION_INTERVIEW)
        + [
            gr.update(value=progress_html),
            gr.update(value=first_question),
            gr.update(visible=True),
            gr.update(visible=True, interactive=False),
            gr.update(visible=True),
            gr.update(visible=False),
            state,
        ]
    )


def pipeline(audio_path, text_input, state: InterviewState):
    """Process user input and generate the next question or final results.

    Args:
        audio_path: Optional path to recorded audio
        text_input: Optional text input
        state: Per-session InterviewState instance

    Returns:
        Tuple of Gradio updates for UI components + updated state
    """
    # Get transcript from audio or text
    if audio_path:
        transcript = audio_service.transcribe(audio_path)
    else:
        transcript = (text_input or "").strip()

    if not transcript:
        return (
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            state,
        )

    state.add_message("user", transcript)

    if not state.is_interview_complete:
        # Generate next question
        response = llm_service.generate_response(
            settings.INTERVIEW_PROMPT_PATH,
            job_choice=state.job_choice,
            max_questions=state.max_question_amount,
            resume_summary=state.resume_summary,
            chat_history=state.chat_history,
        )
        state.add_message("assistant", response)
        state.increment_question()

        progress_html = create_progress_html(state)

        return (
            response,
            gr.update(value=None),
            gr.update(interactive=False),
            gr.update(visible=False),
            gr.update(value=None),
            gr.update(value=progress_html),
            state,
        )
    else:
        # Interview complete — generate evaluation
        response = llm_service.generate_response(
            settings.RESULTS_PROMPT_PATH,
            job_choice=state.job_choice,
            max_questions=state.max_question_amount,
            resume_summary=state.resume_summary,
            chat_history=state.chat_history,
        )
        state.reset()

        return (
            response,
            gr.update(value=None, visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=None, visible=False),
            gr.update(value=create_completed_progress_html()),
            state,
        )


def reset_interview(state: InterviewState):
    """Reset the interview to start a new session.

    Args:
        state: Per-session InterviewState instance

    Returns:
        Tuple of Gradio updates for UI components + updated state
    """
    state.reset()

    return (
        _show_section(SECTION_LANDING)
        + [
            gr.update(value=""),   # progress_indicator
            gr.update(value=""),   # assistant_output
            gr.update(visible=False),  # user_answer_input
            gr.update(visible=False),  # submit_answer_btn
            gr.update(visible=False),  # user_text_input
            gr.update(visible=False),  # reset_interview_btn
            state,
        ]
    )
