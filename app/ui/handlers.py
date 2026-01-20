"""
UI Event Handlers

Handles all UI events and user interactions.
Includes navigation functions for the wizard and interview logic.
"""
import gradio as gr

from app.config.settings import settings
from app.state import interview_state
from app.services.llm_service import llm_service
from app.services.audio_service import audio_service
from app.services.document_service import document_service
from app.ui.components import (
    create_progress_html, 
    create_completed_progress_html,
    create_step_header,
    create_summary_card,
    create_wizard_header
)


def change_interactivity(enable: bool):
    """Toggle interactivity of a component."""
    return gr.update(interactive=enable)


def enable_submit(text: str):
    """Enable submit button when text is not empty."""
    return gr.update(interactive=bool(text and text.strip()))


# === Navigation Handlers ===

def go_to_job_page():
    """Navigate from landing to job page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=True),   # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


def go_to_resume_page(job: str):
    """Navigate from job page to resume page."""
    if not job or not job.strip():
        # Reste sur la page si le champ est vide
        return [
            gr.update(),  # landing_section
            gr.update(),  # job_section
            gr.update(),  # resume_section
            gr.update(),  # questions_section
            gr.update(),  # summary_section
            gr.update(),  # interview_section
        ]
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=True),   # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


def go_to_questions_page():
    """Navigate from resume page to questions page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=True),   # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


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
        gr.update(visible=False),  # interview_section
        gr.update(value=summary_html),  # summary_display
    ]


def go_back_to_job():
    """Navigate back to job page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=True),   # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


def go_back_to_resume():
    """Navigate back to resume page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=True),   # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


def go_back_to_questions():
    """Navigate back to questions page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=True),   # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
    ]


def show_loading_page():
    """Navigate to loading page."""
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=True),   # loading_section
        gr.update(visible=False),  # interview_section
    ]


# === Interview Handlers ===

def start_interview(job_chosen: str, resume_file, nb_questions: int):
    """
    Start a new interview session.
    
    Args:
        job_chosen: The job position selected
        resume_file: Optional uploaded resume file
        nb_questions: Number of questions for the interview
        
    Returns:
        Tuple of Gradio updates for UI components
    """
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
        job_choice=interview_state.job_choice,
        max_questions=interview_state.max_question_amount,
        resume_summary=interview_state.resume_summary,
        chat_history=interview_state.chat_history
    )
    interview_state.add_message("assistant", first_question)
    
    progress_html = create_progress_html()
    
    return [
        gr.update(visible=False),  # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # loading_section
        gr.update(visible=True),   # interview_section
        gr.update(value=progress_html),  # progress_indicator
        gr.update(value=first_question),  # assistant_output
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
        Tuple of Gradio updates for UI components
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
            job_choice=interview_state.job_choice,
            max_questions=interview_state.max_question_amount,
            resume_summary=interview_state.resume_summary,
            chat_history=interview_state.chat_history
        )
        interview_state.add_message("assistant", response)
        interview_state.increment_question()
        
        progress_html = create_progress_html()
        
        return (
            response,
            gr.update(value=None),
            gr.update(interactive=False),
            gr.update(visible=False),
            gr.update(value=None),
            gr.update(value=progress_html)
        )
    else:
        # Interview complete - generate results
        response = llm_service.generate_response(
            settings.RESULTS_PROMPT_PATH,
            job_choice=interview_state.job_choice,
            max_questions=interview_state.max_question_amount,
            resume_summary=interview_state.resume_summary,
            chat_history=interview_state.chat_history
        )
        interview_state.reset()
        
        return (
            response,
            gr.update(value=None, visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=None, visible=False),
            gr.update(value=create_completed_progress_html())
        )


def reset_interview():
    """
    Reset the interview to start a new session.
    
    Returns:
        Tuple of Gradio updates for UI components
    """
    interview_state.reset()
    
    return [
        gr.update(visible=True),   # landing_section
        gr.update(visible=False),  # job_section
        gr.update(visible=False),  # resume_section
        gr.update(visible=False),  # questions_section
        gr.update(visible=False),  # summary_section
        gr.update(visible=False),  # interview_section
        gr.update(value=""),       # progress_indicator
        gr.update(value=""),       # assistant_output
        gr.update(visible=False),  # user_answer_input
        gr.update(visible=False),  # submit_answer_btn
        gr.update(visible=False),  # user_text_input
        gr.update(visible=False),  # reset_interview_btn
    ]
