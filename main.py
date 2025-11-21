import gradio as gr

from audio_utils import transcribe_audio
from llm_client import generate_response, summarize_resume
import globals

import pyttsx3
from TTS.api import TTS
import simpleaudio as sa
import numpy as np

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

tts_engine = pyttsx3.init()

### Function and vars ###

## Short functions

def speak(text: str):
    tts_engine.say(text)
    tts_engine.runAndWait()

def speak_output(text: str):
    if text:
        speak(text)
    return text

def change_interactivity(enable: bool):
    return gr.update(interactive=enable)


## Button functions

# submit job button
def start_interview(job_chosen, resume_file, nb_questions):
    globals.job_choice = job_chosen
    if resume_file is not None:
        globals.resume_summary = summarize_resume(resume_file)
    globals.nb_questions = nb_questions
    first_question = generate_response(globals.interview_prompt_filepath)
    return [
        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
        gr.update(visible=True, value=first_question), gr.update(visible=True), gr.update(visible=True)
    ]

# submit answer button
def pipeline(audio_path):
    # Transcript the user audio and store int
    transcript = transcribe_audio(audio_path)
    globals.chat_history.append({"role" : "user", "content": transcript})

    if globals.question_count < globals.max_question_amount:
        # Generates answer, stores it and returns data
        response = generate_response(globals.interview_prompt_filepath)
        globals.chat_history.append({"role" : "assistant", "content": response})
        globals.question_count += 1
        return response, gr.update(value=None), gr.update(), gr.update()
    else:
        # Generates results, resets vars, and switch element visibility
        response = generate_response(globals.results_prompt_filepath)
        globals.chat_history.clear()
        return response, gr.update(value=None, visible=False), gr.update(visible=False), gr.update(visible=True)

# restart button
def reset_interview():
    globals.reset()
    return [
        gr.update(visible=False), gr.update(visible=False),
        gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True),
    ]



### Front-end part ###

with gr.Blocks() as app:
    ## UI elements
    # Pre-interview elements
    page_title =            gr.Markdown("Module de simulation d'entretien d'embauche")
    job_choice_input =      gr.Textbox(label="Choix du poste visé :", interactive=True)
    resume_input =          gr.File(label="Uploadez votre C.V.", file_types=[".docx", ".pdf"])
    nb_question_input =     gr.Slider(1, 30, value=globals.max_question_amount, step=1, label="Nombre de question", info="Choisissez le nombre de question de l'entretien :")
    submit_job_btn =        gr.Button("Valider les paramètres d'entretien")

    # During interview elements
    assistant_output =      gr.Textbox(label="Assistant virtuel :", interactive=False, visible=False)
    user_answer_input =     gr.Microphone(type="filepath", label="Parlez...", max_length=60, elem_id="audio", visible=False)
    #user_transcription_output = gr.Textbox(label="Transcription", interactive=False, visible=False)
    submit_answer_btn =     gr.Button("Valider la réponse", interactive=False, visible=False)

    # Post-interview elements
    reset_interview_btn =   gr.Button("Recommencer un entretien", visible=False)

    # Function assignation
    submit_job_btn.click(
        fn=start_interview,
        inputs=[job_choice_input,
                resume_input,
                nb_question_input],
        outputs=[job_choice_input,
                 resume_input,
                 nb_question_input,
                 submit_job_btn,
                 assistant_output,
                 user_answer_input,
                 submit_answer_btn]
    ).then(
        fn=speak_output,
        inputs=assistant_output,
        outputs=None
    )

    user_answer_input.clear(fn=lambda: change_interactivity(False), outputs=submit_answer_btn)
    user_answer_input.stop_recording(fn=lambda: change_interactivity(True), outputs=submit_answer_btn)
    submit_answer_btn.click(
        fn=pipeline,
        inputs=user_answer_input,
        outputs=[assistant_output,
                 user_answer_input,
                 submit_answer_btn,
                 reset_interview_btn]
    ).then(
        fn=speak_output,
        inputs=assistant_output,
        outputs=None
    )

    reset_interview_btn.click(fn=reset_interview, outputs=[assistant_output, reset_interview_btn, job_choice_input, resume_input, nb_question_input, submit_job_btn])

app.launch()
reset_interview()
