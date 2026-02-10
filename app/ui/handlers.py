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
from app.services.tts_service import tts_service
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

    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=True),   # summary_section
        gr.update(visible=False),  # loading_section
        gr.update(visible=False),  # interview_section
        gr.update(value=summary_html),  # summary_display
    ]


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


def show_loading_and_start(job_chosen: str, resume_file, nb_questions: int):
    """
    Show loading animation and start interview.
    Uses Gradio generator to show loading first, then start interview.

    Args:
        job_chosen: The job position selected
        resume_file: Optional uploaded resume file path
        nb_questions: Number of questions for the interview

    Yields:
        Tuple of Gradio updates for UI components + updated state
    """
    import time

    # First yield: show loading page
    yield [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=True),   # loading_section
        gr.update(visible=False),  # interview_section
        gr.update(),               # progress_indicator
        gr.update(),               # assistant_output
        gr.update(),               # user_answer_input
        gr.update(),               # submit_answer_btn
        gr.update(),               # user_text_input
        gr.update(),               # reset_interview_btn
        gr.update(),               # assistant_audio
    ]

    # Update state
    interview_state.job_choice = job_chosen
    interview_state.max_question_amount = int(nb_questions)
    interview_state.question_count = 1

    # Process resume if provided
    if resume_file is not None:
        interview_state.resume_summary = document_service.summarize_resume(resume_file)

    # Generate first question
    first_question = llm_service.generate_response(
        settings.INTERVIEW_PROMPT_PATH,
        job_choice=state.job_choice,
        max_questions=state.max_question_amount,
        resume_summary=state.resume_summary,
        chat_history=state.chat_history,
    )
    interview_state.add_message("assistant", first_question)

    # Generate Audio
    audio_path = tts_service.generate_audio(first_question)
    audio_update = gr.update(value=audio_path, visible=True, autoplay=True) if audio_path else gr.update(visible=False)

    progress_html = create_progress_html()

    # Minimum loading time for animation effect
    time.sleep(2)

    # Second yield: show interview page
    yield [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # loading_section
        gr.update(visible=True),   # interview_section
        gr.update(value=progress_html),  # progress_indicator
        gr.update(value=first_question),  # assistant_output
        audio_update,                     # assistant_audio
        gr.update(visible=True),   # user_answer_input
        gr.update(visible=True, interactive=False),  # submit_answer_btn
        gr.update(visible=True),   # user_text_input
        gr.update(visible=False),  # reset_interview_btn
    ]


def pipeline(audio_path=None, text_input=None):
    """
    Process user input and generate next question or results.

    Args:
        audio_path: Optional path to recorded audio
        text_input: Optional text input

    Returns:
        Tuple of Gradio updates for UI components + updated state
    """
    # Get transcript from audio or text
    if audio_path:
        transcript = audio_service.transcribe(audio_path)
    else:
        transcript = text_input or ""

    interview_state.add_message("user", transcript)

    if not interview_state.is_interview_complete:
        # Generate next question
        response = llm_service.generate_response(
            settings.INTERVIEW_PROMPT_PATH,
            job_choice=state.job_choice,
            max_questions=state.max_question_amount,
            resume_summary=state.resume_summary,
            chat_history=state.chat_history,
        )
        interview_state.add_message("assistant", response)
        interview_state.increment_question()

        # Generate Audio
        audio_file = tts_service.generate_audio(response)
        audio_update = gr.update(value=audio_file, visible=True, autoplay=True) if audio_file else gr.update(visible=False)

        progress_html = create_progress_html()

        return (
            response,
            gr.update(value=None),
            gr.update(interactive=False),
            gr.update(visible=False),
            gr.update(value=None),
            gr.update(value=progress_html),
            audio_update # assistant_audio
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
        interview_state.reset()

        # Audio for results (optional, maybe too long?)
        # User asked for "synthèse vocale", implying the interviewer speaks.
        # Results are usually written feedback. I'll omit audio for results to keep it natural, or include it if short.
        # But usually results are long. I'll skip audio for the final feedback for now.

        return (
            response,
            gr.update(value=None, visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=None, visible=False),
            gr.update(value=create_completed_progress_html()),
            gr.update(visible=False) # assistant_audio
        )


def reset_interview():
    """
    Reset the interview to start a new session.

    Returns:
        Tuple of Gradio updates for UI components + updated state
    """
    interview_state.reset()

    return [
        gr.update(visible=True),   # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # loading_section
        gr.update(visible=False),  # interview_section
        gr.update(value=""),       # progress_indicator
        gr.update(value=""),       # assistant_output
        gr.update(visible=False),  # assistant_audio
        gr.update(visible=False),  # user_answer_input
        gr.update(visible=False),  # submit_answer_btn
        gr.update(visible=False),  # user_text_input
        gr.update(visible=False),  # reset_interview_btn
    ]
