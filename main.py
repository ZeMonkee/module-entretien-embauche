import gradio as gr

from audio_utils import transcribe_audio
from llm_client import generate_response, summarize_resume
import globals


### Custom Theme & CSS ###

# Modern dark theme with premium aesthetics
custom_theme = gr.themes.Base(
    primary_hue=gr.themes.colors.purple,
    secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    font=gr.themes.GoogleFont("Inter"),
    font_mono=gr.themes.GoogleFont("JetBrains Mono"),
).set(
    body_background_fill="#0f0f1a",
    body_background_fill_dark="#0f0f1a",
    background_fill_primary="#1a1a2e",
    background_fill_primary_dark="#1a1a2e",
    background_fill_secondary="#16213e",
    background_fill_secondary_dark="#16213e",
    border_color_primary="rgba(255,255,255,0.2)",
    block_background_fill="#1a1a2e",
    block_border_color="rgba(255,255,255,0.15)",
    block_label_background_fill="#252545",
    block_label_text_color="#ffffff",
    block_title_text_color="#ffffff",
    body_text_color="#ffffff",
    body_text_color_subdued="#c0c0e0",
    button_primary_background_fill="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    button_primary_background_fill_hover="linear-gradient(135deg, #7b91ed 0%, #8a5fb5 100%)",
    button_primary_text_color="#ffffff",
    button_primary_border_color="transparent",
    button_secondary_background_fill="#2a2a4a",
    button_secondary_text_color="#ffffff",
    input_background_fill="#1e1e38",
    input_background_fill_dark="#1e1e38",
    input_border_color="rgba(255,255,255,0.25)",
    input_border_color_focus="rgba(102, 126, 234, 0.8)",
    input_placeholder_color="#8888aa",
    slider_color="#667eea",
    block_shadow="0 8px 32px rgba(0,0,0,0.3)",
    block_border_width="1px",
    block_radius="16px",
    button_large_radius="12px",
    input_radius="10px",
)

# Advanced custom CSS
custom_css = """
/* === Import Fonts === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* === Root Variables === */
:root {
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%);
    --gradient-success: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    --glass-bg: rgba(26, 26, 46, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);
    --shadow-glow: 0 0 40px rgba(102, 126, 234, 0.15);
}

/* === Global Styles === */
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    background: transparent !important;
}

body {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%) !important;
    min-height: 100vh;
}

/* === Header Styles === */
.header-container {
    text-align: center;
    padding: 2.5rem 2rem;
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.15) 0%, transparent 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(10px);
    animation: fadeInDown 0.6s ease-out;
}

.main-title {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin-bottom: 0.5rem !important;
}

.subtitle {
    color: #c8c8e8 !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* === Card Styles === */
.config-card, .interview-card, .result-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    box-shadow: var(--shadow-glow), 0 8px 32px rgba(0,0,0,0.3) !important;
    animation: fadeIn 0.5s ease-out;
}

.card-title {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    color: #e0e0ff !important;
    margin-bottom: 1.5rem !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* === Progress Bar === */
.progress-container {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid var(--glass-border);
}

.progress-text {
    color: #d0d0f0;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.progress-bar {
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--gradient-primary);
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* === Button Styles === */
.primary-btn {
    background: var(--gradient-primary) !important;
    border: none !important;
    padding: 14px 32px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    cursor: pointer;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
    text-transform: none !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5) !important;
}

.secondary-btn {
    background: var(--gradient-secondary) !important;
    box-shadow: 0 4px 20px rgba(72, 198, 239, 0.3) !important;
}

.secondary-btn:hover {
    box-shadow: 0 8px 30px rgba(72, 198, 239, 0.4) !important;
}

.success-btn {
    background: var(--gradient-success) !important;
    box-shadow: 0 4px 20px rgba(56, 239, 125, 0.3) !important;
}

/* === Chat Styles === */
.chat-message {
    padding: 1rem 1.25rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    line-height: 1.6;
    animation: slideIn 0.3s ease-out;
}

.assistant-message {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 16px 16px 16px 4px;
}

.user-message {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px 16px 4px 16px;
    margin-left: 2rem;
}

/* === Input Styles === */
.modern-input textarea, .modern-input input {
    background: #1e1e38 !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 14px 16px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.modern-input textarea:focus, .modern-input input:focus {
    border-color: rgba(102, 126, 234, 0.8) !important;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
}

.modern-input label {
    color: #e0e0ff !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}

/* === File Upload === */
.file-upload {
    border: 2px dashed rgba(102, 126, 234, 0.4) !important;
    border-radius: 16px !important;
    background: rgba(102, 126, 234, 0.05) !important;
    transition: all 0.3s ease !important;
}

.file-upload:hover {
    border-color: rgba(102, 126, 234, 0.7) !important;
    background: rgba(102, 126, 234, 0.1) !important;
}

/* === Slider === */
.modern-slider input[type="range"] {
    accent-color: #667eea;
}

/* === Microphone === */
.mic-container {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
    border: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: 16px;
    padding: 1rem;
    transition: all 0.3s ease;
}

.mic-container:hover {
    border-color: rgba(239, 68, 68, 0.5);
}

/* === Textbox Output === */
.output-box textarea {
    background: rgba(102, 126, 234, 0.15) !important;
    border: 1px solid rgba(102, 126, 234, 0.4) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    line-height: 1.7 !important;
    padding: 1.25rem !important;
}

/* === Global Gradio Overrides for Visibility === */

/* All labels should be bright white */
label, .label-wrap, span.svelte-1gfkn6j, .block-label {
    color: #ffffff !important;
}

/* All text in the app */
p, span, div {
    color: inherit;
}

/* Slider labels and info text */
.wrap .head, .info {
    color: #c8c8e8 !important;
}

/* Slider value display */
input[type="number"] {
    color: #ffffff !important;
    background: #252545 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* File upload text */
.upload-text, .file-preview {
    color: #ffffff !important;
}

.secondary-text, .file-size {
    color: #b0b0d0 !important;
}

/* All input placeholders */
::placeholder {
    color: #9090b0 !important;
    opacity: 1 !important;
}

/* Dropdown and select elements */
select, option {
    color: #ffffff !important;
    background: #1e1e38 !important;
}

/* Any button text */
button {
    color: #ffffff !important;
}

/* Gradio specific label containers */
.label-wrap span, .block-title {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Info text under sliders/inputs */
.info-text, .caption {
    color: #b0b0d0 !important;
}

/* === Animations === */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.loading {
    animation: pulse 1.5s infinite;
}

/* === Status Indicators === */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.status-active {
    background: rgba(56, 239, 125, 0.15);
    color: #38ef7d;
    border: 1px solid rgba(56, 239, 125, 0.3);
}

.status-waiting {
    background: rgba(102, 126, 234, 0.15);
    color: #667eea;
    border: 1px solid rgba(102, 126, 234, 0.3);
}

/* === Responsive === */
@media (max-width: 768px) {
    .main-title { font-size: 1.6rem !important; }
    .config-card, .interview-card { padding: 1.25rem !important; }
    .gradio-container { padding: 1rem !important; }
}

/* === Custom Scrollbar === */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: rgba(102, 126, 234, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(102, 126, 234, 0.7);
}

/* === Auto-height textarea === */
.auto-height textarea {
    height: auto !important;
    min-height: 80px;
    max-height: 400px;
    overflow-y: auto !important;
}

/* === Footer === */
.footer {
    text-align: center;
    padding: 1.5rem;
    color: #606080;
    font-size: 0.85rem;
    margin-top: 2rem;
}

.footer a {
    color: #667eea;
    text-decoration: none;
}
"""


### Function and vars ###

## Short functions
def change_interactivity(enable: bool):
    return gr.update(interactive=enable)


def get_progress_html():
    """Generate HTML for progress indicator"""
    progress = (globals.question_count / globals.max_question_amount) * 100
    return f"""
    <div class="progress-container">
        <div class="progress-text">
            <span style="color: #e0e0ff; font-weight: 500;">Question {globals.question_count}</span> 
            <span style="color: #606080;">sur {globals.max_question_amount}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """


## Button functions

# submit job button
def start_interview(job_chosen, resume_file, nb_questions):
    globals.job_choice = job_chosen
    if resume_file is not None:
        globals.resume_summary = summarize_resume(resume_file)
    globals.max_question_amount = nb_questions
    globals.question_count = 1
    first_question = generate_response(globals.interview_prompt_filepath)
    globals.chat_history.append({"role": "assistant", "content": first_question})
    
    progress_html = get_progress_html()
    
    return [
        gr.update(visible=False),  # config_section
        gr.update(visible=True),   # interview_section
        gr.update(value=progress_html),  # progress_indicator
        gr.update(value=first_question),  # assistant_output
        gr.update(visible=True),   # user_answer_input
        gr.update(visible=True, interactive=False),   # submit_answer_btn
        gr.update(visible=True),   # user_text_input
        gr.update(visible=False),  # reset_interview_btn
    ]


def pipeline(audio_path=None, text_input=None):
    # Priorité au micro si disponible, sinon texte
    if audio_path:
        transcript = transcribe_audio(audio_path)
    else:
        transcript = text_input or ""

    globals.chat_history.append({"role": "user", "content": transcript})

    if globals.question_count < globals.max_question_amount:
        response = generate_response(globals.interview_prompt_filepath)
        globals.chat_history.append({"role": "assistant", "content": response})
        globals.question_count += 1
        progress_html = get_progress_html()
        return (
            response, 
            gr.update(value=None), 
            gr.update(interactive=False), 
            gr.update(visible=False),
            gr.update(value=None),
            gr.update(value=progress_html)
        )
    else:
        # Fin de l'entretien - Afficher les résultats
        response = generate_response(globals.results_prompt_filepath)
        globals.reset()
        return (
            response, 
            gr.update(value=None, visible=False), 
            gr.update(visible=False), 
            gr.update(visible=True),
            gr.update(value=None, visible=False),
            gr.update(value="<div class='progress-container'><div class='progress-text' style='color: #38ef7d;'>✓ Entretien terminé</div></div>")
        )


# restart button
def reset_interview():
    globals.reset()
    return [
        gr.update(visible=True),   # config_section
        gr.update(visible=False),  # interview_section
        gr.update(value=""),       # progress_indicator
        gr.update(value=""),       # assistant_output
        gr.update(visible=False),  # user_answer_input
        gr.update(visible=False),  # submit_answer_btn
        gr.update(visible=False),  # user_text_input
        gr.update(visible=False),  # reset_interview_btn
    ]


def enable_submit(text):
    return gr.update(interactive=bool(text and text.strip()))


### Front-end part ###

with gr.Blocks(theme=custom_theme, css=custom_css, title="Simulateur d'Entretien") as app:
    
    # === Header Section ===
    gr.HTML("""
        <div class="header-container">
            <h1 class="main-title">Simulateur d'Entretien d'Embauche</h1>
            <p class="subtitle">Préparez-vous à votre prochain entretien avec notre IA</p>
        </div>
    """)
    
    # === Configuration Section ===
    with gr.Column(visible=True, elem_classes="config-card") as config_section:
        gr.HTML('<div class="card-title">Configuration de l\'entretien</div>')
        
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
                value=globals.max_question_amount, 
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
        gr.HTML('<div class="card-title">Entretien en cours</div>')
        
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
                    max_length=60,
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
            "✓ Valider ma réponse", 
            variant="primary",
            elem_classes=["primary-btn", "secondary-btn"],
            interactive=False, 
            visible=False,
            size="lg"
        )
        
        reset_interview_btn = gr.Button(
            "🔄 Recommencer un nouvel entretien", 
            variant="secondary",
            elem_classes=["primary-btn", "success-btn"],
            visible=False,
            size="lg"
        )
    
    # === Footer ===
    gr.HTML("""
        <div class="footer">
            Propulsé par <strong>Formasup Odyssée</strong> • Module de simulation d'entretien avec IA
        </div>
    """)
    
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

    user_answer_input.clear(fn=lambda: change_interactivity(False), outputs=submit_answer_btn)
    user_answer_input.stop_recording(fn=lambda: change_interactivity(True), outputs=submit_answer_btn)
    user_text_input.change(fn=enable_submit, inputs=user_text_input, outputs=submit_answer_btn)

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


if __name__ == "__main__":
    app.launch()
