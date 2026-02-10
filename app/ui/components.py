"""
UI Components

Reusable HTML components for the Gradio interface.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.state import InterviewState


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
    """Create the landing page with animated title."""
    return """
        <div class="landing-container">
            <h1 class="landing-title">Simulateur d'Entretien</h1>
            <p class="landing-subtitle">
                Préparez-vous à décrocher le poste de vos rêves
                grâce à notre IA de simulation d'entretien
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
    """Create the step progress header for the wizard.

    Args:
        current_step: Current step number (1-4)
    """
    steps = [
        ("1", "Poste"),
        ("2", "CV"),
        ("3", "Questions"),
        ("4", "Résumé"),
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

        html += f"""
            <div class="step-item">
                <div class="step-circle {circle_class}">{icon}</div>
                <span class="step-label">{label}</span>
            </div>
        """

        if i < len(steps):
            connector_class = "completed" if i < current_step else ""
            html += f'<div class="step-connector {connector_class}"></div>'

    html += "</div>"
    return html


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


def create_progress_html(state: "InterviewState") -> str:
    """Generate HTML for the progress indicator.

    Args:
        state: Current interview state (per-session)
    """
    progress = state.progress_percentage
    return f"""
    <div class="progress-container">
        <div class="progress-text">
            <span style="color: #e0e0ff; font-weight: 500;">Question {state.question_count}</span>
            <span style="color: #606080;">sur {state.max_question_amount}</span>
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
            Propulsé par <strong>Formasup Odyssée</strong> · Module de simulation d'entretien avec IA
        </div>
    """


def create_rocket_loader() -> str:
    """Create the rocket loading animation."""
    return """
        <div class="rocket-loader-container">
            <div class="stars"></div>
            <div class="rocket-wrapper">
                <div class="rocket">
                    <div class="rocket-body">
                        <div class="rocket-window"></div>
                    </div>
                    <div class="rocket-fin left"></div>
                    <div class="rocket-fin right"></div>
                    <div class="rocket-flames">
                        <div class="flame flame-1"></div>
                        <div class="flame flame-2"></div>
                        <div class="flame flame-3"></div>
                    </div>
                </div>
                <div class="smoke-container">
                    <div class="smoke smoke-1"></div>
                    <div class="smoke smoke-2"></div>
                    <div class="smoke smoke-3"></div>
                    <div class="smoke smoke-4"></div>
                </div>
            </div>
            <div class="loader-text">
                <span class="loading-title">Décollage imminent...</span>
                <span class="loading-subtitle">Préparation de votre entretien</span>
            </div>
        </div>

        <style>
            .rocket-loader-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 60vh;
                position: relative;
                overflow: hidden;
            }

            .stars {
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: radial-gradient(2px 2px at 20px 30px, #eee, transparent),
                            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
                            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
                            radial-gradient(2px 2px at 160px 120px, rgba(255,255,255,0.9), transparent),
                            radial-gradient(1px 1px at 230px 80px, #eee, transparent),
                            radial-gradient(2px 2px at 300px 150px, #fff, transparent),
                            radial-gradient(1px 1px at 370px 50px, rgba(255,255,255,0.7), transparent),
                            radial-gradient(2px 2px at 450px 180px, #eee, transparent);
                background-repeat: repeat;
                background-size: 500px 200px;
                animation: starsMove 3s linear infinite;
            }

            @keyframes starsMove {
                from { transform: translateY(-100px); }
                to { transform: translateY(100px); }
            }

            .rocket-wrapper {
                position: relative;
                animation: rocketShake 0.1s ease-in-out infinite,
                           rocketLiftoff 3s ease-in-out infinite;
            }

            @keyframes rocketShake {
                0%, 100% { transform: translateX(-2px) rotate(-1deg); }
                25% { transform: translateX(2px) rotate(1deg); }
                50% { transform: translateX(-1px) rotate(0deg); }
                75% { transform: translateX(1px) rotate(-0.5deg); }
            }

            @keyframes rocketLiftoff {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }

            .rocket { position: relative; width: 80px; height: 180px; }

            .rocket-body {
                position: absolute; top: 0; left: 50%;
                transform: translateX(-50%);
                width: 50px; height: 120px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50% 50% 30% 30% / 60% 60% 20% 20%;
                box-shadow:
                    inset -8px 0 15px rgba(0,0,0,0.3),
                    inset 8px 0 15px rgba(255,255,255,0.2),
                    0 0 30px rgba(102, 126, 234, 0.5);
            }

            .rocket-body::before {
                content: '';
                position: absolute; top: -25px; left: 50%;
                transform: translateX(-50%);
                border-left: 15px solid transparent;
                border-right: 15px solid transparent;
                border-bottom: 35px solid #ff6b6b;
                filter: drop-shadow(0 0 10px rgba(255, 107, 107, 0.8));
            }

            .rocket-window {
                position: absolute; top: 25px; left: 50%;
                transform: translateX(-50%);
                width: 22px; height: 22px;
                background: linear-gradient(135deg, #74ebd5 0%, #acb6e5 100%);
                border-radius: 50%;
                border: 3px solid #4a5568;
                box-shadow:
                    inset -3px -3px 8px rgba(0,0,0,0.3),
                    0 0 15px rgba(116, 235, 213, 0.6);
            }

            .rocket-fin {
                position: absolute; bottom: 0;
                width: 25px; height: 45px;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
            }

            .rocket-fin.left {
                left: 0;
                border-radius: 50% 0 0 50%;
                transform: skewY(-15deg);
            }

            .rocket-fin.right {
                right: 0;
                border-radius: 0 50% 50% 0;
                transform: skewY(15deg);
            }

            .rocket-flames {
                position: absolute; bottom: -60px; left: 50%;
                transform: translateX(-50%);
                display: flex; gap: 3px;
            }

            .flame {
                width: 12px; height: 50px;
                background: linear-gradient(to bottom, #fff 0%, #ffeb3b 30%, #ff9800 60%, #ff5722 100%);
                border-radius: 50% 50% 50% 50% / 30% 30% 70% 70%;
                animation: flameFlicker 0.1s ease-in-out infinite alternate;
                box-shadow: 0 0 20px #ff9800, 0 0 40px #ff5722;
            }

            .flame-1 { animation-delay: 0s; height: 45px; }
            .flame-2 { animation-delay: 0.05s; height: 55px; }
            .flame-3 { animation-delay: 0.1s; height: 45px; }

            @keyframes flameFlicker {
                0% { transform: scaleY(0.9) scaleX(0.9); opacity: 0.9; }
                100% { transform: scaleY(1.1) scaleX(1.1); opacity: 1; }
            }

            .smoke-container {
                position: absolute; bottom: -100px; left: 50%;
                transform: translateX(-50%);
                display: flex; gap: 10px;
            }

            .smoke {
                width: 30px; height: 30px;
                background: radial-gradient(circle, rgba(200,200,200,0.8) 0%, transparent 70%);
                border-radius: 50%;
                animation: smokeRise 1s ease-out infinite;
            }

            .smoke-1 { animation-delay: 0s; }
            .smoke-2 { animation-delay: 0.2s; left: -20px; }
            .smoke-3 { animation-delay: 0.4s; left: 20px; }
            .smoke-4 { animation-delay: 0.6s; }

            @keyframes smokeRise {
                0% { transform: translateY(0) scale(0.5); opacity: 0.8; }
                100% { transform: translateY(80px) scale(2); opacity: 0; }
            }

            .loader-text {
                margin-top: 80px;
                text-align: center;
                z-index: 10;
            }

            .loading-title {
                display: block;
                font-size: 1.8rem; font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: pulseText 1.5s ease-in-out infinite;
            }

            .loading-subtitle {
                display: block; margin-top: 10px;
                font-size: 1rem; color: #a0a0c0;
                animation: fadeInOut 2s ease-in-out infinite;
            }

            @keyframes pulseText {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.02); }
            }

            @keyframes fadeInOut {
                0%, 100% { opacity: 0.6; }
                50% { opacity: 1; }
            }
        </style>
    """
