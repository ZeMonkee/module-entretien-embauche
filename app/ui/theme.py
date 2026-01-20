"""
Gradio Theme Configuration

Custom dark theme with premium aesthetics.
"""
import gradio as gr


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
