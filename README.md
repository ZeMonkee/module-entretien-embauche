# Simulateur d'Entretien d'Embauche — PoC

Module de simulation d'entretien d'embauche en français, propulsé par un LLM local (Ollama).
L'application propose un wizard interactif permettant de configurer l'entretien, de répondre aux questions par écrit ou oralement, et de recevoir un feedback détaillé.


## Architecture

```
module-entretien-embauche/
├── main.py                    # Point d'entrée — crée l'app Gradio
├── requirements.txt
├── prompts/                   # Templates de prompts pour le LLM
│   ├── interview_prompt.txt   # Prompt du recruteur (questions)
│   ├── results_prompt.txt     # Prompt d'évaluation finale
│   └── summarize_resume_prompt.txt  # Résumé de CV
└── app/
    ├── config/
    │   └── settings.py        # Configuration centralisée
    ├── services/
    │   ├── llm_service.py     # Interaction avec Ollama
    │   ├── audio_service.py   # Transcription audio (Whisper)
    │   └── document_service.py # Extraction de texte (PDF/DOCX)
    ├── state/
    │   └── interview_state.py # État de session (per-user via gr.State)
    └── ui/
        ├── theme.py           # Thème Gradio personnalisé
        ├── styles.py          # CSS custom
        ├── components.py      # Composants HTML réutilisables
        └── handlers.py        # Logique des événements UI
```


## Prérequis

- **Python** 3.10+
- **Ollama** 0.5+


## Installation

### 1. Environnement virtuel (recommandé)

```shell
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Ollama

Installez et lancez le modèle :

```shell
ollama pull llama3.1:8b
```

Si vous n'utilisez pas l'application desktop Ollama, démarrez le serveur manuellement :

```shell
ollama serve
```

> Le modèle peut être changé via la variable d'environnement `OLLAMA_MODEL`
> ou dans `app/config/settings.py`.

### 3. Dépendances Python

```shell
pip install -r requirements.txt
```


## Lancement

```shell
python main.py
```

L'application sera accessible sur `http://localhost:7860`.


### Variables d'environnement optionnelles

| Variable          | Défaut                                  | Description                    |
|-------------------|-----------------------------------------|--------------------------------|
| `OLLAMA_MODEL`    | `llama3.1:8b`                           | Modèle LLM à utiliser         |
| `OLLAMA_URL`      | `http://localhost:11434/api/generate`   | URL de l'API Ollama            |
| `LLM_TIMEOUT`     | `120`                                   | Timeout des requêtes LLM (s)  |
| `WHISPER_MODEL`   | `tiny`                                  | Modèle Whisper pour l'audio   |
| `WHISPER_THREADS` | `8`                                     | Threads CPU pour Whisper      |


### Partager sur un lien public

```python
# Dans main.py, remplacez :
app.launch()
# Par :
app.launch(share=True)
```


### Transcription audio trop lente

Changez le modèle Whisper dans `settings.py` ou via la variable `WHISPER_MODEL`.
Modèles disponibles (du plus rapide au plus précis) : `tiny`, `base`, `small`, `medium`, `large`.


## Licence

Ce projet est la propriété de **Formasup Odyssée**. Tous droits réservés.