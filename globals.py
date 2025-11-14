## Pre-launch customizable variables

interview_prompt_filepath = "prompts/interview_prompt.txt"
generative_ai_model = "mistral"
generative_ai_url = "http://localhost:11434/api/generate"
results_prompt_filepath = "prompts/results_prompt.txt"
summarize_resume_prompt_filepath = "prompts/summarize_resume_prompt.txt"


##########################################################


## Dynamically changed variables

chat_history = []
job_choice = "non défini"
max_question_amount = 3
question_count = 1
resume_summary = ""

def reset():
    chat_history = []
    job_choice = "non défini"
    question_count = 1
    resume_summary = ""