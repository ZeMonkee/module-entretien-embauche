"""
Custom CSS Styles

All custom CSS styles for the Gradio interface.
Design futuriste avec animations, particules et fond animé.
"""

custom_css = """
/* === Import Fonts === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap');

/* === Root Variables === */
:root {
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%);
    --gradient-success: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    --gradient-animated: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
    --glass-bg: rgba(26, 26, 46, 0.85);
    --glass-border: rgba(255, 255, 255, 0.1);
    --shadow-glow: 0 0 60px rgba(102, 126, 234, 0.25);
    --neon-purple: #a855f7;
    --neon-blue: #3b82f6;
    --neon-cyan: #06b6d4;
}

/* === Animated Background === */
body {
    background: var(--gradient-animated) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 15s ease infinite !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(6, 182, 212, 0.1) 0%, transparent 40%);
    pointer-events: none;
    z-index: 0;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* === Particle Effects === */
.particles-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(168, 85, 247, 0.6);
    border-radius: 50%;
    animation: floatParticle 20s infinite ease-in-out;
}

.particle:nth-child(2) { left: 20%; animation-delay: -5s; background: rgba(59, 130, 246, 0.5); }
.particle:nth-child(3) { left: 40%; animation-delay: -10s; background: rgba(6, 182, 212, 0.5); }
.particle:nth-child(4) { left: 60%; animation-delay: -15s; background: rgba(168, 85, 247, 0.4); }
.particle:nth-child(5) { left: 80%; animation-delay: -7s; background: rgba(59, 130, 246, 0.4); }

@keyframes floatParticle {
    0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
}

/* === Global Container === */
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    background: transparent !important;
    position: relative;
    z-index: 1;
}

/* === Landing Page === */
.landing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
    padding: 2rem;
    animation: fadeInScale 1s ease-out;
}

.landing-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #764ba2, #48c6ef);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 3s ease infinite;
    margin-bottom: 1rem;
    text-shadow: 0 0 60px rgba(102, 126, 234, 0.5);
}

.landing-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem;
    color: #c8c8e8;
    margin-bottom: 3rem;
    opacity: 0;
    animation: fadeInUp 0.8s ease-out 0.3s forwards;
}

.landing-features {
    display: flex;
    gap: 2rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
    justify-content: center;
    opacity: 0;
    animation: fadeInUp 0.8s ease-out 0.5s forwards;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #a0a0c0;
    font-size: 0.95rem;
}

.feature-icon {
    font-size: 1.2rem;
}

@keyframes gradientText {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* === Launch Button === */
.launch-btn {
    background: var(--gradient-primary) !important;
    border: none !important;
    padding: 18px 48px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.2rem !important;
    border-radius: 50px !important;
    cursor: pointer;
    transition: all 0.4s ease !important;
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.5) !important;
    position: relative;
    overflow: hidden;
    animation: pulseGlow 2s infinite;
}

.launch-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.launch-btn:hover::before {
    left: 100%;
}

.launch-btn:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 0 50px rgba(102, 126, 234, 0.7) !important;
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.5); }
    50% { box-shadow: 0 0 50px rgba(102, 126, 234, 0.8); }
}

/* === Step Header / Progress Stepper === */
.step-header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: rgba(26, 26, 46, 0.5);
    border-radius: 16px;
    border: 1px solid var(--glass-border);
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.step-circle.active {
    background: var(--gradient-primary);
    color: white;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
}

.step-circle.completed {
    background: var(--gradient-success);
    color: white;
}

.step-circle.inactive {
    background: rgba(255,255,255,0.1);
    color: #606080;
}

.step-label {
    font-size: 0.85rem;
    color: #a0a0c0;
    display: none;
}

.step-connector {
    width: 40px;
    height: 2px;
    background: rgba(255,255,255,0.1);
    margin: 0 0.25rem;
}

.step-connector.completed {
    background: var(--gradient-primary);
}

@media (min-width: 768px) {
    .step-label { display: block; }
    .step-connector { width: 60px; }
}

/* === Glassmorphism Cards === */
.wizard-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 2.5rem !important;
    box-shadow: var(--shadow-glow), 0 8px 32px rgba(0,0,0,0.4) !important;
    animation: slideUp 0.5s ease-out;
    position: relative;
    overflow: hidden;
}

.wizard-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.config-card, .interview-card, .result-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 2.5rem !important;
    box-shadow: var(--shadow-glow), 0 8px 32px rgba(0,0,0,0.4) !important;
    animation: slideUp 0.5s ease-out;
}

/* === Card Titles === */
.card-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #e0e0ff, #a0a0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1.5rem !important;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.card-icon {
    font-size: 1.8rem;
}

/* === Summary Card === */
.summary-card {
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    color: #a0a0c0;
    font-size: 0.9rem;
}

.summary-value {
    color: #ffffff;
    font-weight: 500;
}

/* === Header Styles === */
.header-container {
    text-align: center;
    padding: 2.5rem 2rem;
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.2) 0%, transparent 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(10px);
    animation: fadeInDown 0.6s ease-out;
}

.main-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
}

.subtitle {
    color: #c8c8e8 !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
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
    position: relative;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
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
    position: relative;
    overflow: hidden;
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

.nav-btn {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #ffffff !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.nav-btn:hover {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.3) !important;
}

/* === Chat Styles === */
.chat-container {
    background: rgba(0,0,0,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

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
    position: relative;
}

.assistant-message::before {
    content: '🤖';
    position: absolute;
    left: -2rem;
    top: 0.75rem;
    font-size: 1.2rem;
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
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
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

/* === Global Gradio Overrides === */
label, .label-wrap, span.svelte-1gfkn6j, .block-label {
    color: #ffffff !important;
}

p, span, div {
    color: inherit;
}

.wrap .head, .info {
    color: #c8c8e8 !important;
}

input[type="number"] {
    color: #ffffff !important;
    background: #252545 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

.upload-text, .file-preview {
    color: #ffffff !important;
}

.secondary-text, .file-size {
    color: #b0b0d0 !important;
}

::placeholder {
    color: #9090b0 !important;
    opacity: 1 !important;
}

select, option {
    color: #ffffff !important;
    background: #1e1e38 !important;
}

button {
    color: #ffffff !important;
}

.label-wrap span, .block-title {
    color: #ffffff !important;
    font-weight: 500 !important;
}

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
    .landing-title { font-size: 2.2rem; }
    .main-title { font-size: 1.6rem !important; }
    .config-card, .interview-card, .wizard-card { padding: 1.5rem !important; }
    .gradio-container { padding: 1rem !important; }
    .landing-features { flex-direction: column; gap: 1rem; }
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
