"""
Interview Simulation Module

Main entry point for the Gradio application.
"""
import gradio as gr

from app.config.settings import settings
from app.ui.theme import custom_theme
from app.ui.styles import custom_css
from app.ui.components import create_header, create_footer, create_card_title
from app.ui.handlers import (
    start_interview,
    pipeline,
    reset_interview,
    enable_submit,
    change_interactivity
)


def create_app() -> gr.Blocks:
    """Create and configure the Gradio application."""
    
    with gr.Blocks(theme=custom_theme, css=custom_css, title="Simulateur d'Entretien") as app:
        
        # === Header Section ===
        gr.HTML(create_header())
        
        # === Configuration Section ===
        with gr.Column(visible=True, elem_classes="config-card") as config_section:
            gr.HTML(create_card_title("Configuration de l'entretien"))
            
            with gr.Column(elem_classes="modern-input"):
                job_choice_input = gr.Textbox(
                    label="Poste visé",
                    placeholder="Ex: Développeur Full Stack, Chef de Projet, Data Analyst...",
                    interactive=True,
                )
            
            resume_input = gr.File(
                label="Uploadez votre CV (optionnel)",
                file_types=[".docx", ".pdf"],
                elem_classes="file-upload"
            )
            
            with gr.Column(elem_classes="modern-slider"):
                nb_question_input = gr.Slider(
                    minimum=1,
                    maximum=30,
                    value=settings.DEFAULT_MAX_QUESTIONS,
                    step=1,
                    label="Nombre de questions",
                    info="Choisissez la durée de votre simulation"
                )
            
            submit_job_btn = gr.Button(
                "Démarrer l'entretien",
                variant="primary",
                elem_classes="primary-btn",
                size="lg"
            )
        
        # === Interview Section ===
        with gr.Column(visible=False, elem_classes="interview-card") as interview_section:
            gr.HTML(create_card_title("Entretien en cours"))
            
            progress_indicator = gr.HTML(value="")
            
            assistant_output = gr.Textbox(
                label="Recruteur",
                interactive=False,
                lines=4,
                max_lines=20,
                elem_classes=["auto-height", "output-box"]
            )
            
            gr.HTML('<div style="margin: 1.5rem 0; border-top: 1px solid rgba(255,255,255,0.1);"></div>')
            
            with gr.Row():
                with gr.Column(scale=1, elem_classes="mic-container"):
                    user_answer_input = gr.Microphone(
                        type="filepath",
                        label="Répondez oralement",
                        max_length=settings.MAX_AUDIO_LENGTH,
                        visible=False
                    )
                
                with gr.Column(scale=2, elem_classes="modern-input"):
                    user_text_input = gr.Textbox(
                        label="Ou écrivez votre réponse",
                        placeholder="Tapez votre réponse ici...",
                        lines=3,
                        interactive=True,
                        visible=False
                    )
            
            submit_answer_btn = gr.Button(
                "Valider ma réponse",
                variant="primary",
                elem_classes=["primary-btn", "secondary-btn"],
                interactive=False,
                visible=False,
                size="lg"
            )
            
            reset_interview_btn = gr.Button(
                "Recommencer un nouvel entretien",
                variant="secondary",
                elem_classes=["primary-btn", "success-btn"],
                visible=False,
                size="lg"
            )
        
        # === Footer ===
        gr.HTML(create_footer())
        
        # === Event Handlers ===
        submit_job_btn.click(
            fn=start_interview,
            inputs=[job_choice_input, resume_input, nb_question_input],
            outputs=[
                config_section,
                interview_section,
                progress_indicator,
                assistant_output,
                user_answer_input,
                submit_answer_btn,
                user_text_input,
                reset_interview_btn
            ]
        )
        
        user_answer_input.clear(
            fn=lambda: change_interactivity(False),
            outputs=submit_answer_btn
        )
        user_answer_input.stop_recording(
            fn=lambda: change_interactivity(True),
            outputs=submit_answer_btn
        )
        user_text_input.change(
            fn=enable_submit,
            inputs=user_text_input,
            outputs=submit_answer_btn
        )
        
        submit_answer_btn.click(
            fn=pipeline,
            inputs=[user_answer_input, user_text_input],
            outputs=[
                assistant_output,
                user_answer_input,
                submit_answer_btn,
                reset_interview_btn,
                user_text_input,
                progress_indicator
            ]
        )
        
        reset_interview_btn.click(
            fn=reset_interview,
            outputs=[
                config_section,
                interview_section,
                progress_indicator,
                assistant_output,
                user_answer_input,
                submit_answer_btn,
                user_text_input,
                reset_interview_btn
            ]
        )
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
