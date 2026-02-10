"""
Interview Simulation Module

Main entry point for the Gradio application.
Multi-page wizard with futuristic design.
"""
import logging

import gradio as gr

from app.config.settings import settings
from app.state import InterviewState
from app.ui.theme import custom_theme
from app.ui.styles import custom_css
from app.ui.components import (
    create_landing_page,
    create_footer,
    create_wizard_header,
    create_particles_html,
    create_rocket_loader,
)
from app.ui.handlers import (
    show_loading_and_start,
    pipeline,
    reset_interview,
    enable_submit,
    change_interactivity,
    go_to_job_page,
    go_to_resume_page,
    go_to_questions_page,
    go_to_summary_page,
    go_back_to_job,
    go_back_to_resume,
    go_back_to_questions,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


def create_app() -> gr.Blocks:
    """Create and configure the Gradio application with multi-page wizard."""

    with gr.Blocks(
        title="Simulateur d'Entretien",
        theme=custom_theme,
        css=custom_css,
    ) as app:

        # Per-session interview state (each user gets their own instance)
        session_state = gr.State(InterviewState())

        # === Particles Background ===
        gr.HTML(create_particles_html())

        # === Section 0: Landing Page ===
        with gr.Column(visible=True, elem_classes="landing-section") as landing_section:
            gr.HTML(create_landing_page())
            launch_btn = gr.Button(
                "🚀 Commencer la simulation",
                variant="primary",
                elem_classes="launch-btn",
                size="lg",
            )

        # === Section 1: Job Selection ===
        with gr.Column(visible=False, elem_classes="wizard-card") as job_section:
            gr.HTML(create_wizard_header(1, "Quel poste visez-vous ?", "💼"))
            with gr.Column(elem_classes="modern-input"):
                job_choice_input = gr.Textbox(
                    label="Intitulé du poste",
                    placeholder="Ex: Développeur Full Stack, Chef de Projet, Data Analyst...",
                    interactive=True,
                )
            with gr.Row():
                job_next_btn = gr.Button(
                    "Suivant →",
                    variant="primary",
                    elem_classes="primary-btn",
                    size="lg",
                )

        # === Section 2: Resume Upload ===
        with gr.Column(visible=False, elem_classes="wizard-card") as resume_section:
            gr.HTML(create_wizard_header(2, "Uploadez votre CV", "📄"))
            resume_input = gr.File(
                label="CV (optionnel) — formats acceptés: .pdf, .docx",
                file_types=[".docx", ".pdf"],
                elem_classes="file-upload",
            )
            gr.HTML(
                '<p style="color: #a0a0c0; font-size: 0.9rem; margin-top: 0.5rem;">'
                "Le CV permet de personnaliser les questions selon votre profil"
                "</p>"
            )
            with gr.Row():
                resume_back_btn = gr.Button(
                    "← Retour",
                    variant="secondary",
                    elem_classes="nav-btn",
                    size="lg",
                )
                resume_next_btn = gr.Button(
                    "Suivant →",
                    variant="primary",
                    elem_classes="primary-btn",
                    size="lg",
                )

        # === Section 3: Number of Questions ===
        with gr.Column(visible=False, elem_classes="wizard-card") as questions_section:
            gr.HTML(create_wizard_header(3, "Durée de l'entretien", "🔢"))
            with gr.Column(elem_classes="modern-slider"):
                nb_question_input = gr.Slider(
                    minimum=1,
                    maximum=30,
                    value=settings.DEFAULT_MAX_QUESTIONS,
                    step=1,
                    label="Nombre de questions",
                    info="Plus de questions = entretien plus approfondi",
                )
            with gr.Row():
                questions_back_btn = gr.Button(
                    "← Retour",
                    variant="secondary",
                    elem_classes="nav-btn",
                    size="lg",
                )
                questions_next_btn = gr.Button(
                    "Suivant →",
                    variant="primary",
                    elem_classes="primary-btn",
                    size="lg",
                )

        # === Section 4: Summary ===
        with gr.Column(visible=False, elem_classes="wizard-card") as summary_section:
            gr.HTML(create_wizard_header(4, "Récapitulatif", "📋"))
            summary_display = gr.HTML(value="")
            gr.HTML(
                '<p style="color: #c8c8e8; text-align: center; margin: 1rem 0;">'
                "Vérifiez vos informations avant de démarrer"
                "</p>"
            )
            with gr.Row():
                summary_back_btn = gr.Button(
                    "← Modifier",
                    variant="secondary",
                    elem_classes="nav-btn",
                    size="lg",
                )
                start_interview_btn = gr.Button(
                    "🎯 Démarrer l'entretien",
                    variant="primary",
                    elem_classes=["primary-btn", "launch-btn"],
                    size="lg",
                )

        # === Section 5: Loading Page ===
        with gr.Column(visible=False, elem_classes="wizard-card") as loading_section:
            gr.HTML(create_rocket_loader())

        # === Section 6: Interview Chat ===
        with gr.Column(visible=False, elem_classes="interview-card") as interview_section:
            gr.HTML(
                '<div class="card-title">'
                '<span class="card-icon">💬</span>Entretien en cours'
                "</div>"
            )
            progress_indicator = gr.HTML(value="")
            assistant_output = gr.Textbox(
                label="Recruteur",
                interactive=False,
                lines=4,
                max_lines=20,
                elem_classes=["auto-height", "output-box"],
            )
            gr.HTML(
                '<div style="margin: 1.5rem 0; border-top: 1px solid rgba(255,255,255,0.1);"></div>'
            )
            with gr.Row():
                with gr.Column(scale=1, elem_classes="mic-container"):
                    user_answer_input = gr.Microphone(
                        type="filepath",
                        label="🎤 Répondez oralement",
                        visible=False,
                    )
                with gr.Column(scale=2, elem_classes="modern-input"):
                    user_text_input = gr.Textbox(
                        label="✍️ Ou écrivez votre réponse",
                        placeholder="Tapez votre réponse ici...",
                        lines=3,
                        interactive=True,
                        visible=False,
                    )
            submit_answer_btn = gr.Button(
                "Valider ma réponse",
                variant="primary",
                elem_classes=["primary-btn", "secondary-btn"],
                interactive=False,
                visible=False,
                size="lg",
            )
            reset_interview_btn = gr.Button(
                "🔄 Recommencer un nouvel entretien",
                variant="secondary",
                elem_classes=["primary-btn", "success-btn"],
                visible=False,
                size="lg",
            )

        # === Footer ===
        gr.HTML(create_footer())

        # === Section list for navigation outputs ===
        all_sections = [
            landing_section,
            job_section,
            resume_section,
            questions_section,
            summary_section,
            loading_section,
            interview_section,
        ]

        # === Event Handlers: Navigation ===

        launch_btn.click(fn=go_to_job_page, outputs=all_sections)

        job_next_btn.click(
            fn=go_to_resume_page,
            inputs=[job_choice_input],
            outputs=all_sections,
        )

        resume_next_btn.click(fn=go_to_questions_page, outputs=all_sections)
        resume_back_btn.click(fn=go_back_to_job, outputs=all_sections)

        questions_next_btn.click(
            fn=go_to_summary_page,
            inputs=[job_choice_input, resume_input, nb_question_input],
            outputs=all_sections + [summary_display],
        )
        questions_back_btn.click(fn=go_back_to_resume, outputs=all_sections)

        summary_back_btn.click(fn=go_back_to_questions, outputs=all_sections)

        # === Event Handlers: Interview ===

        interview_outputs = [
            *all_sections,
            progress_indicator,
            assistant_output,
            user_answer_input,
            submit_answer_btn,
            user_text_input,
            reset_interview_btn,
            session_state,
        ]

        start_interview_btn.click(
            fn=show_loading_and_start,
            inputs=[job_choice_input, resume_input, nb_question_input, session_state],
            outputs=interview_outputs,
        )

        # Microphone events
        user_answer_input.clear(
            fn=lambda: change_interactivity(False),
            outputs=submit_answer_btn,
        )
        user_answer_input.stop_recording(
            fn=lambda: change_interactivity(True),
            outputs=submit_answer_btn,
        )
        user_text_input.change(
            fn=enable_submit,
            inputs=user_text_input,
            outputs=submit_answer_btn,
        )

        # Submit answer
        pipeline_outputs = [
            assistant_output,
            user_answer_input,
            submit_answer_btn,
            reset_interview_btn,
            user_text_input,
            progress_indicator,
            session_state,
        ]

        submit_answer_btn.click(
            fn=pipeline,
            inputs=[user_answer_input, user_text_input, session_state],
            outputs=pipeline_outputs,
        )

        # Reset interview
        reset_interview_btn.click(
            fn=reset_interview,
            inputs=[session_state],
            outputs=interview_outputs,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
