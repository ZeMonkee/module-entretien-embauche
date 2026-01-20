"""
UI Components

Reusable HTML components for the Gradio interface.
Design futuriste avec wizard multi-pages.
"""
from app.state import interview_state


def create_particles_html() -> str:
    """Create floating particles background effect."""
    return """
        <div class="particles-container">
            <div class="particle" style="left: 10%;"></div>
            <div class="particle" style="left: 25%;"></div>
            <div class="particle" style="left: 45%;"></div>
            <div class="particle" style="left: 65%;"></div>
            <div class="particle" style="left: 85%;"></div>
        </div>
    """


def create_landing_page() -> str:
    """Create the landing page with animated title and launch button."""
    return """
        <div class="landing-container">
            <h1 class="landing-title">Simulateur d'Entretien</h1>
            <p class="landing-subtitle">
                Préparez-vous à décrocher le poste de vos rêves grâce à notre IA de simulation d'entretien
            </p>
            <div class="landing-features">
                <div class="feature-item">
                    <span class="feature-icon">🎯</span>
                    <span>Questions personnalisées</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🎤</span>
                    <span>Réponse vocale ou écrite</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span>Feedback détaillé</span>
                </div>
            </div>
        </div>
    """


def create_step_header(current_step: int) -> str:
    """
    Create the step progress header for the wizard.
    
    Args:
        current_step: Current step number (1-4)
    """
    steps = [
        ("1", "Poste"),
        ("2", "CV"),
        ("3", "Questions"),
        ("4", "Résumé")
    ]
    
    html = '<div class="step-header">'
    
    for i, (num, label) in enumerate(steps, 1):
        if i < current_step:
            circle_class = "completed"
            icon = "✓"
        elif i == current_step:
            circle_class = "active"
            icon = num
        else:
            circle_class = "inactive"
            icon = num
        
        html += f'''
            <div class="step-item">
                <div class="step-circle {circle_class}">{icon}</div>
                <span class="step-label">{label}</span>
            </div>
        '''
        
        if i < len(steps):
            connector_class = "completed" if i < current_step else ""
            html += f'<div class="step-connector {connector_class}"></div>'
    
    html += '</div>'
    return html


def create_header() -> str:
    """Create the header HTML component."""
    return """
        <div class="header-container">
            <h1 class="main-title">🚀 Simulateur d'Entretien d'Embauche</h1>
            <p class="subtitle">Propulsé par l'intelligence artificielle</p>
        </div>
    """


def create_wizard_header(step: int, title: str, icon: str = "💼") -> str:
    """Create a wizard page header with step indicator."""
    return f"""
        {create_step_header(step)}
        <div class="card-title">
            <span class="card-icon">{icon}</span>
            {title}
        </div>
    """


def create_summary_card(job: str, has_resume: bool, nb_questions: int) -> str:
    """Create the summary card showing all entered information."""
    resume_text = "✓ CV uploadé" if has_resume else "Aucun CV"
    resume_color = "#38ef7d" if has_resume else "#a0a0c0"
    
    return f"""
        <div class="summary-card">
            <div class="summary-item">
                <span class="summary-label">💼 Poste visé</span>
                <span class="summary-value">{job or "Non spécifié"}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">📄 CV</span>
                <span class="summary-value" style="color: {resume_color};">{resume_text}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">🔢 Nombre de questions</span>
                <span class="summary-value">{nb_questions}</span>
            </div>
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


def create_chat_header() -> str:
    """Create the chat interview header."""
    return """
        <div class="card-title">
            <span class="card-icon">💬</span>
            Entretien en cours
        </div>
    """


def create_footer() -> str:
    """Create the footer HTML component."""
    return """
        <div class="footer">
            Propulsé par <strong>Formasup Odyssée</strong> • Module de simulation d'entretien avec IA
        </div>
    """


def create_card_title(text: str, icon: str = "") -> str:
    """Create a card title HTML component."""
    icon_html = f'<span class="card-icon">{icon}</span>' if icon else ''
    return f'<div class="card-title">{icon_html}{text}</div>'
