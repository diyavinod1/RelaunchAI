"""
ReLaunchAI Frontend - Beautiful Animated Streamlit Application
User interface with premium animations, glass morphism, and micro-interactions.
"""

import streamlit as st
import requests
import json
import time
import random
from datetime import datetime

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="ReLaunchAI - Career Reintegration Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# ============================================
# PREMIUM CSS WITH ANIMATIONS & EFFECTS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #ec4899;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f0f23;
        --bg-card: rgba(255, 255, 255, 0.03);
        --glass: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== PARTICLE BACKGROUND ===== */
    .particle-container {
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
        background: rgba(99, 102, 241, 0.6);
        border-radius: 50%;
        animation: float-particle 15s infinite ease-in-out;
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* ===== 3D FLOATING SHAPES ===== */
    .floating-shape {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
    }
    
    .shape-1 {
        width: 400px;
        height: 400px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        top: -100px;
        right: -100px;
        animation: float-shape-1 20s infinite ease-in-out;
    }
    
    .shape-2 {
        width: 300px;
        height: 300px;
        background: linear-gradient(135deg, #ec4899, #f472b6);
        bottom: -50px;
        left: -50px;
        animation: float-shape-2 25s infinite ease-in-out;
    }
    
    .shape-3 {
        width: 250px;
        height: 250px;
        background: linear-gradient(135deg, #06b6d4, #22d3ee);
        top: 50%;
        left: 50%;
        animation: float-shape-3 18s infinite ease-in-out;
    }
    
    @keyframes float-shape-1 {
        0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); }
        33% { transform: translate(-30px, 30px) rotate(120deg) scale(1.1); }
        66% { transform: translate(20px, -20px) rotate(240deg) scale(0.9); }
    }
    
    @keyframes float-shape-2 {
        0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); }
        50% { transform: translate(40px, -30px) rotate(180deg) scale(1.15); }
    }
    
    @keyframes float-shape-3 {
        0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-45%, -55%) rotate(180deg); }
    }
    
    /* ===== HERO SECTION ===== */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        color: #a5b4fc;
        margin-bottom: 1.5rem;
        animation: pulse-badge 2s infinite ease-in-out;
    }
    
    @keyframes pulse-badge {
        0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 0 20px 5px rgba(99, 102, 241, 0.2); }
    }
    
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 1rem;
    animation: title-glow 3s infinite ease-in-out;
    position: relative;
    z-index: 100;
    text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
}
    
    @keyframes title-glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.3)); }
        50% { filter: drop-shadow(0 0 40px rgba(99, 102, 241, 0.6)); }
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto 2rem;
        line-height: 1.7;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    
    .hero-feature {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* ===== GLASS MORPHISM CARDS ===== */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* ===== SHIMMER EFFECT ===== */
    .shimmer {
        position: relative;
        overflow: hidden;
    }
    
    .shimmer::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 200%; }
    }
    
    /* ===== STEPPER ANIMATION ===== */
    .stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        position: relative;
    }
    
    .stepper-line {
        position: absolute;
        top: 50%;
        left: 10%;
        right: 10%;
        height: 3px;
        background: linear-gradient(90deg, #1e293b, #1e293b);
        z-index: 0;
    }
    
    .stepper-line-progress {
        position: absolute;
        top: 50%;
        left: 10%;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #ec4899);
        z-index: 1;
        transition: width 0.5s ease;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 2;
        position: relative;
    }
    
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.2rem;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        background: #1e293b;
        border: 2px solid #334155;
        color: #64748b;
    }
    
    .step.active .step-circle {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-color: #6366f1;
        color: white;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
        animation: step-pulse 1s infinite;
    }
    
    .step.completed .step-circle {
        background: linear-gradient(135deg, #10b981, #34d399);
        border-color: #10b981;
        color: white;
    }
    
    @keyframes step-pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
        50% { transform: scale(1.1); box-shadow: 0 0 40px rgba(99, 102, 241, 0.8); }
    }
    
    .step-label {
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #64748b;
        transition: color 0.3s ease;
    }
    
    .step.active .step-label {
        color: #a5b4fc;
        font-weight: 500;
    }
    
    /* ===== BUTTON MICRO-INTERACTIONS ===== */
    .premium-button {
        position: relative;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
        padding: 1rem 3rem;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.5);
    }
    
    .premium-button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .premium-button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .premium-button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.6);
    }
    
    .premium-button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* ===== CONFETTI ANIMATION ===== */
    .confetti-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
    }
    
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        animation: confetti-fall 3s ease-out forwards;
    }
    
    @keyframes confetti-fall {
        0% { 
            transform: translateY(-100px) rotate(0deg); 
            opacity: 1;
        }
        100% { 
            transform: translateY(100vh) rotate(720deg); 
            opacity: 0;
        }
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.5), transparent);
    }
    
    /* ===== FORM STYLES ===== */
    .form-container {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
    }
    
    .form-label {
        color: #cbd5e1;
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .form-input {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 0.875rem 1rem;
        color: white;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* ===== SKILL TAGS ===== */
    .skill-tag {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4));
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    /* ===== GAP LEVEL INDICATORS ===== */
    .gap-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .gap-moderate {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .gap-minor {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    /* ===== INFO BOXES ===== */
    .info-box {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(6, 182, 212, 0.05));
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* ===== LOADING SPINNER ===== */
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ===== TAB STYLES ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--glass);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid var(--glass-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        color: #94a3b8;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(99, 102, 241, 0.1);
        color: #a5b4fc;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    /* ===== EXPANDER STYLES ===== */
    .streamlit-expanderHeader {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* ===== SIDEBAR STYLES ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f0f23;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 4px;
    }
    
    /* ===== FADE IN ANIMATION ===== */
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
        opacity: 0;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* ===== SLIDE IN ANIMATION ===== */
    .slide-in-left {
        animation: slideInLeft 0.5s ease-out forwards;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ===== BOUNCE ANIMATION ===== */
    .bounce {
        animation: bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BACKGROUND EFFECTS (PARTICLES & SHAPES)
# ============================================
def render_background_effects():
    """Render animated background particles and floating shapes."""
    particles_html = '<div class="particle-container">'
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.uniform(0, 15)
        duration = random.uniform(10, 20)
        particles_html += f'<div class="particle" style="left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'
    particles_html += '</div>'
    
    shapes_html = '''
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
    '''
    
    st.markdown(particles_html + shapes_html, unsafe_allow_html=True)

# ============================================
# CONFETTI ANIMATION
# ============================================
def render_confetti():
    """Render confetti burst animation."""
    colors = ['#6366f1', '#ec4899', '#06b6d4', '#10b981', '#f59e0b', '#8b5cf6']
    confetti_html = '<div class="confetti-container">'
    
    for i in range(50):
        left = random.randint(0, 100)
        delay = random.uniform(0, 1)
        duration = random.uniform(2, 4)
        color = random.choice(colors)
        confetti_html += f'<div class="confetti" style="left: {left}%; background: {color}; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'
    
    confetti_html += '</div>'
    st.markdown(confetti_html, unsafe_allow_html=True)

# ============================================
# STEPPER COMPONENT
# ============================================
def render_stepper(current_step, total_steps=5):
    """Render animated step progress tracker."""
    steps = [
        ("Skills", "📊"),
        ("Resume", "📝"),
        ("Interview", "🎯"),
        ("Roadmap", "📅"),
        ("Programs", "🏢")
    ]
    
    progress = (current_step / total_steps) * 80 + 10
    
    stepper_html = f'''
    <div class="stepper-container">
        <div class="stepper-line"></div>
        <div class="stepper-line-progress" style="width: {progress}%"></div>
    '''
    
    for i, (label, icon) in enumerate(steps, 1):
        status_class = ""
        if i < current_step:
            status_class = "completed"
            display = "✓"
        elif i == current_step:
            status_class = "active"
            display = icon
        else:
            display = str(i)
        
        stepper_html += f'''
        <div class="step {status_class}">
            <div class="step-circle">{display}</div>
            <div class="step-label">{label}</div>
        </div>
        '''
    
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
def render_hero():
    """Render premium landing page hero."""
    hero_html = '''
    <div class="hero-container">
        <div class="hero-badge">
            <span>✨</span> AI-Powered Career Reintegration
        </div>
        <h1 class="hero-title">ReLaunchAI</h1>
        <p class="hero-subtitle">
            Your intelligent companion for confidently returning to the workforce. 
            We analyze, guide, and empower your career comeback journey.
        </p>
        <div class="hero-features">
            <div class="hero-feature">
                <span>🎯</span> Personalized Analysis
            </div>
            <div class="hero-feature">
                <span>⚡</span> Instant Insights
            </div>
            <div class="hero-feature">
                <span>🔒</span> Private & Secure
            </div>
        </div>
    </div>
    '''
    st.markdown(hero_html, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
def render_sidebar():
    """Render beautiful sidebar."""
    with st.sidebar:
        st.markdown('''
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.5rem;">
                🚀 ReLaunchAI
            </h2>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown('''
        <div style="color: #94a3b8; line-height: 1.8;">
        <p><strong style="color: #a5b4fc;">ReLaunchAI</strong> helps women returning to work after career breaks through:</p>
        
        <div style="margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span style="color: #6366f1;">📊</span> <span>Skill Gap Analysis</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span style="color: #ec4899;">📝</span> <span>Resume Rewriting</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span style="color: #06b6d4;">🎯</span> <span>Interview Coaching</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span style="color: #10b981;">📅</span> <span>30-Day Roadmap</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span style="color: #f59e0b;">🏢</span> <span>Returnship Programs</span>
            </div>
        </div>
        
        <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid rgba(99, 102, 241, 0.2);">
            <p style="margin: 0; color: #a5b4fc; font-size: 0.9rem;"><strong>How it works:</strong></p>
            <ol style="margin: 0.5rem 0 0 1rem; padding-left: 1rem; color: #94a3b8; font-size: 0.85rem;">
                <li>Fill in your profile details</li>
                <li>Click "Generate My Plan"</li>
                <li>Review personalized recommendations</li>
                <li>Take action with confidence!</li>
            </ol>
        </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("Built with ❤️ for your successful return to work")

# ============================================
# INPUT FORM
# ============================================
def render_input_form():
    """Render beautiful input form."""
    st.markdown('<div class="section-header">👤 Your Profile</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<label class="form-label">Full Name *</label>', unsafe_allow_html=True)
            name = st.text_input("", placeholder="e.g., Sarah Johnson", label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Education *</label>', unsafe_allow_html=True)
            education = st.text_input("", placeholder="e.g., MBA, Computer Science", label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Previous Job Role *</label>', unsafe_allow_html=True)
            previous_role = st.text_input("", placeholder="e.g., Marketing Manager", label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Years of Experience *</label>', unsafe_allow_html=True)
            years_experience = st.number_input("", min_value=0, max_value=50, value=5, label_visibility="collapsed")
        
        with col2:
            st.markdown('<label class="form-label">Career Break (months) *</label>', unsafe_allow_html=True)
            break_duration = st.number_input("break_months", min_value=1, max_value=240, value=24, label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Reason for Break *</label>', unsafe_allow_html=True)
            break_reason = st.selectbox(
                "break_reason",
                options=[
                    ("maternity", "Maternity Leave"),
                    ("childcare", "Childcare / Family Care"),
                    ("eldercare", "Eldercare"),
                    ("health", "Health / Personal Wellness"),
                    ("relocation", "Relocation"),
                    ("education", "Further Education"),
                    ("personal", "Personal Growth"),
                    ("other", "Other")
                ],
                format_func=lambda x: x[1],
                label_visibility="collapsed"
            )
            
            st.markdown('<label class="form-label">Additional Details</label>', unsafe_allow_html=True)
            break_details = st.text_area("", placeholder="Any context about your break...", max_chars=500, label_visibility="collapsed")
        
        st.markdown("---")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<label class="form-label">Your Skills (comma-separated) *</label>', unsafe_allow_html=True)
            skills_input = st.text_area("skills", placeholder="e.g., Project Management, Data Analysis, Python, Team Leadership", height=100, label_visibility="collapsed")
        
        with col4:
            st.markdown('<label class="form-label">Target Role *</label>', unsafe_allow_html=True)
            target_role = st.text_input("target", placeholder="e.g., Product Manager", label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Target Industry</label>', unsafe_allow_html=True)
            industry = st.text_input("industry", placeholder="e.g., Technology", label_visibility="collapsed")
            
            st.markdown('<label class="form-label">Your Location</label>', unsafe_allow_html=True)
            location = st.text_input("location", placeholder="e.g., New York, NY", label_visibility="collapsed")
    
    skills = [s.strip() for s in skills_input.split(",") if s.strip()] if skills_input else []
    
    return {
        "name": name,
        "education": education,
        "previous_role": previous_role,
        "years_experience": years_experience,
        "break_duration_months": break_duration,
        "break_reason": break_reason[0],
        "break_reason_details": break_details if break_details else None,
        "skills_known": skills,
        "target_role": target_role,
        "industry": industry if industry else None,
        "location": location if location else None
    }

# ============================================
# VALIDATION
# ============================================
def validate_inputs(data):
    """Validate form inputs."""
    errors = []
    required_fields = ["name", "education", "previous_role", "target_role"]
    
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    if not data.get("skills_known"):
        errors.append("At least one skill is required")
    
    return errors

# ============================================
# API CALL
# ============================================
def call_api(endpoint, data):
    """Make API call to backend."""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Please start the server: `python -m backend.main`")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# ============================================
# RENDER RESULTS
# ============================================
def render_skill_gap_analysis(data):
    """Render skill gap analysis with animations."""
    st.markdown('<div class="section-header fade-in">📊 Skill Gap Analysis</div>', unsafe_allow_html=True)
    
    # Transferable skills
    st.subheader("✅ Your Transferable Skills")
    skills_html = ""
    for skill in data.get("transferable_skills", []):
        skills_html += f'<span class="skill-tag">{skill}</span>'
    st.markdown(skills_html, unsafe_allow_html=True)
    
    # Skill gaps
    st.subheader("📈 Skills to Develop")
    for gap in data.get("skill_gaps", []):
        gap_class = f"gap-{gap['gap_level'].lower()}"
        importance_emoji = "🔴" if gap['importance'] == "High" else "🟡" if gap['importance'] == "Medium" else "🟢"
        
        with st.expander(f"{importance_emoji} {gap['skill_name']} ({gap['importance']} Priority)"):
            st.markdown(f'<div class="{gap_class}">', unsafe_allow_html=True)
            st.markdown(f"**Gap Level:** {gap['gap_level']}")
            st.markdown(f"**Estimated Time:** {gap['estimated_time_weeks']} weeks")
            st.markdown("**Learning Resources:**")
            for resource in gap['learning_resources']:
                st.markdown(f"- {resource}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Priority
    st.subheader("🎯 Upskilling Priority")
    for i, skill in enumerate(data.get("upskilling_priority", []), 1):
        st.markdown(f"{i}. {skill}")
    
    # Market trends
    st.markdown(f'<div class="info-box">📢 <strong>Market Insight:</strong> {data.get("market_trends_note", "")}</div>', unsafe_allow_html=True)


def render_resume_summary(data):
    """Render resume summary."""
    st.markdown('<div class="section-header fade-in">📝 Professional Summary</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="success-box shimmer">', unsafe_allow_html=True)
    st.markdown(f"**💡 Suggested LinkedIn Headline:**\n\n*{data.get('suggested_headline', '')}*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📝 Resume Summary")
    st.markdown(data.get('professional_summary', ''))
    
    st.subheader("💪 Key Strengths")
    for strength in data.get('key_strengths', []):
        st.markdown(f"✓ {strength}")
    
    st.subheader("🔄 Positioning Your Career Break")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(data.get('career_break_positioning', ''))
    st.markdown('</div>', unsafe_allow_html=True)


def render_interview_prep(data):
    """Render interview preparation."""
    st.markdown('<div class="section-header fade-in">🎯 Interview Preparation</div>', unsafe_allow_html=True)
    
    qa_sections = [
        ("💬 Explaining Your Career Break", data.get('break_explanation', {})),
        ("💬 Addressing Skill Currency", data.get('skill_refresh', {})),
        ("💬 Your Motivation to Return", data.get('motivation_return', {})),
        ("💬 Handling Concerns", data.get('handling_objections', {}))
    ]
    
    for title, qa in qa_sections:
        with st.expander(title):
            st.markdown(f"**Q: {qa.get('question', '')}**")
            st.markdown(f"**A:** {qa.get('answer', '')}")
            st.markdown("**Tips:**")
            for tip in qa.get('tips', []):
                st.markdown(f"• {tip}")
    
    st.subheader("📌 General Interview Tips")
    for tip in data.get('general_tips', []):
        st.markdown(f"✓ {tip}")


def render_roadmap(data):
    """Render 30-day roadmap."""
    st.markdown('<div class="section-header fade-in">📅 30-Day Comeback Roadmap</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(data.get('overview', ''))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("🗓️ Weekly Focus Areas")
    for week in data.get("weekly_focus", []):
        with st.expander(f"Week {week['week']}: {week['theme']}"):
            for obj in week['objectives']:
                st.markdown(f"• {obj}")
    
    st.subheader("📋 Daily Action Plan")
    weeks = {}
    for task in data.get("daily_tasks", []):
        week_num = (task['day'] - 1) // 7 + 1
        weeks.setdefault(week_num, []).append(task)
    
    for week_num, tasks in weeks.items():
        with st.expander(f"Week {week_num} Daily Tasks"):
            for task in tasks:
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"**Day {task['day']}**")
                cols[1].markdown(f"{task['task']}")
                cols[1].caption(f"Category: {task['category']}")
                cols[2].markdown(f"⏱️ {task['estimated_hours']}h")
    
    st.subheader("🏆 Key Milestones")
    for milestone in data.get('milestones', []):
        st.markdown(f"✓ {milestone}")


def render_returnships(data):
    """Render returnship programs."""
    st.markdown('<div class="section-header fade-in">🏢 Returnship Programs</div>', unsafe_allow_html=True)
    
    st.subheader("🎯 Recommended Programs")
    for program in data.get("recommended_programs", []):
        with st.expander(f"{program['program_name']} - {program['company']}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Location:** {program['location']}")
            c1.markdown(f"**Duration:** {program['duration']}")
            c2.markdown(f"**Eligibility:** {program['eligibility']}")
            if program.get('deadline'):
                c2.markdown(f"**Deadline:** {program['deadline']}")
            st.markdown(f"**Description:** {program['description']}")
            if program.get('application_link'):
                st.markdown(f"**Apply:** {program['application_link']}")
    
    st.subheader("💡 General Advice")
    st.markdown(data.get('general_advice', ''))
    
    st.subheader("🤝 Networking Tips")
    for tip in data.get('networking_tips', []):
        st.markdown(f"• {tip}")

# ============================================
# MAIN APPLICATION
# ============================================
def check_api_health():
    """Check if backend API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application function."""
    # Render background effects
    render_background_effects()
    
    # Render hero
    render_hero()
    
    # Render sidebar
    render_sidebar()
    
    # Check API health
    api_ready = check_api_health()
    if not api_ready:
        st.warning("⚠️ Backend server is not running. Start it with: `python -m backend.main`")
    
    # Input form
    form_data = render_input_form()
    
    # Generate button with micro-interaction
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_clicked = st.button("🚀 Generate My Comeback Plan", type="primary", use_container_width=True)
    
    if generate_clicked:
        errors = validate_inputs(form_data)
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            return
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### 🎯 Processing Your Profile")
            
            # Animated stepper
            step_placeholder = st.empty()
            
            # Simulate step progression
            steps = [
                ("Analyzing Skills", 1),
                ("Crafting Resume", 2),
                ("Preparing Interview Answers", 3),
                ("Building Roadmap", 4),
                ("Finding Programs", 5)
            ]
            
            for step_name, step_num in steps:
                with step_placeholder:
                    render_stepper(step_num)
                    st.info(f"⏳ {step_name}...")
                time.sleep(0.8)
            
            # Call API
            with step_placeholder:
                render_stepper(5)
                st.info("🤖 Finalizing your personalized plan...")
            
            result = call_api("/api/analyze", form_data)
        
        if result:
            # Confetti celebration
            render_confetti()
            
            # Success message
            st.markdown(f'''
            <div class="success-box bounce" style="text-align: center;">
                <h2 style="color: #10b981; margin: 0;">🎉 Welcome Back, {result['user_name']}!</h2>
                <p style="color: #94a3b8; margin: 0.5rem 0 0 0;">Your personalized comeback plan is ready!</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Results in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Skills", "📝 Resume", "🎯 Interview", "📅 Roadmap", "🏢 Returnships"
            ])
            
            with tab1:
                render_skill_gap_analysis(result['skill_gap_analysis'])
            
            with tab2:
                render_resume_summary(result['resume_summary'])
            
            with tab3:
                render_interview_prep(result['interview_prep'])
            
            with tab4:
                render_roadmap(result['comeback_roadmap'])
            
            with tab5:
                render_returnships(result['returnship_suggestions'])
            
            # Footer
            st.markdown("---")
            generated_time = datetime.fromisoformat(result['generated_at']).strftime('%B %d, %Y at %I:%M %p')
            st.caption(f"✨ Generated on {generated_time} • Powered by SambaNova AI")


if __name__ == "__main__":
    main()
