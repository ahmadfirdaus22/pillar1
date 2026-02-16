"""
Custom CSS Styling for Streamlit UI
Provides enhanced visual styling and responsive design.
"""

import streamlit as st


def load_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #1f77b4 0%, #4a9eff 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .subsection-header {
        background: #f0f2f6;
        color: #262730;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 500;
        border-left: 4px solid #1f77b4;
    }
    
    /* Status indicators */
    .status-complete {
        color: #28a745;
        font-weight: 600;
    }
    
    .status-incomplete {
        color: #dc3545;
        font-weight: 600;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: 600;
    }
    
    /* Success/Error boxes */
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        color: #721c24;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Primary action button */
    .primary-button > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #ddd;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 1px #1f77b4;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Navigation links in sidebar */
    .nav-link {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .nav-link:hover {
        background-color: #e9ecef;
    }
    
    .nav-link-active {
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
    }
    
    /* Progress indicator */
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #1f77b4 0%, #28a745 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    .card-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #262730;
    }
    
    /* Metric styling */
    .metric-container {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #262730;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #1f77b4;
        margin-left: 0.25rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 12px;
        margin: 0 0.25rem;
    }
    
    .badge-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .badge-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .badge-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .badge-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #1f77b4;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Help text */
    .help-text {
        font-size: 0.9rem;
        color: #6c757d;
        font-style: italic;
        margin-top: 0.25rem;
    }
    
    /* Validation feedback inline */
    .validation-success {
        color: #28a745;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .validation-error {
        color: #dc3545;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    /* Code block styling */
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        .section-header {
            font-size: 1.1rem;
            padding: 0.75rem 1rem;
        }
        
        .card {
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    </style>
    """, unsafe_allow_html=True)


def create_section_header(title: str, icon: str = ""):
    """
    Create a styled section header
    
    Args:
        title: Section title
        icon: Optional emoji icon
    """
    icon_html = f"{icon} " if icon else ""
    st.markdown(f'<div class="section-header">{icon_html}{title}</div>', unsafe_allow_html=True)


def create_subsection_header(title: str):
    """
    Create a styled subsection header
    
    Args:
        title: Subsection title
    """
    st.markdown(f'<div class="subsection-header">{title}</div>', unsafe_allow_html=True)


def show_status_badge(is_complete: bool, label_complete: str = "Complete", label_incomplete: str = "Incomplete"):
    """
    Show a status badge
    
    Args:
        is_complete: Whether the item is complete
        label_complete: Label for complete state
        label_incomplete: Label for incomplete state
    """
    if is_complete:
        st.markdown(f'<span class="badge badge-success">✓ {label_complete}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge badge-danger">✗ {label_incomplete}</span>', unsafe_allow_html=True)


def show_progress_bar(percentage: float, label: str = ""):
    """
    Show a progress bar
    
    Args:
        percentage: Progress percentage (0-100)
        label: Optional label
    """
    progress_html = f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%">
            {label or f"{percentage:.0f}%"}
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)


def show_info_box(message: str, box_type: str = "info"):
    """
    Show a styled info box
    
    Args:
        message: Message to display
        box_type: Type of box (info, success, warning, error)
    """
    st.markdown(f'<div class="{box_type}-box">{message}</div>', unsafe_allow_html=True)


def create_card(title: str, content: str):
    """
    Create a styled card
    
    Args:
        title: Card title
        content: Card content
    """
    card_html = f"""
    <div class="card">
        <div class="card-header">{title}</div>
        <div>{content}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
