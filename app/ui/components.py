"""
UI Components

Reusable HTML components for the Gradio interface.
"""
from app.state import interview_state


def create_header() -> str:
    """Create the header HTML component."""
    return """
        <div class="header-container">
            <h1 class="main-title">Simulateur d'Entretien d'Embauche</h1>
            <p class="subtitle">Préparez-vous à votre prochain entretien avec notre IA</p>
        </div>
    """


def create_progress_html() -> str:
    """Generate HTML for the progress indicator."""
    progress = interview_state.progress_percentage
    return f"""
    <div class="progress-container">
        <div class="progress-text">
            <span style="color: #e0e0ff; font-weight: 500;">Question {interview_state.question_count}</span> 
            <span style="color: #606080;">sur {interview_state.max_question_amount}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """


def create_completed_progress_html() -> str:
    """Generate HTML for completed interview progress."""
    return """
    <div class="progress-container">
        <div class="progress-text" style="color: #38ef7d;">
            ✓ Entretien terminé
        </div>
    </div>
    """


def create_footer() -> str:
    """Create the footer HTML component."""
    return """
        <div class="footer">
            Propulsé par <strong>Formasup Odyssée</strong> • Module de simulation d'entretien avec IA
        </div>
    """


def create_card_title(text: str) -> str:
    """Create a card title HTML component."""
    return f'<div class="card-title">{text}</div>'
