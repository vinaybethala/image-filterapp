# Configuration file for Image Filter App

# Application settings
APP_CONFIG = {
    'title': 'Image Filter App',
    'icon': '🎨',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Supported image formats
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff']

# Filter categories
FILTER_CATEGORIES = [
    "Basic Filters",
    "Artistic Effects", 
    "Adjustments",
    "Transformations",
    "Noise & Effects"
]

# Default filter parameters
DEFAULT_PARAMS = {
    'blur_kernel_size': 15,
    'brightness': 0,
    'contrast': 0,
    'red_balance': 0,
    'green_balance': 0,
    'blue_balance': 0,
    'rotation_angle': 0,
    'scale_factor': 1.0,
    'noise_intensity': 0.1
}

# UI styling
CSS_STYLES = """
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .filter-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .upload-area {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
""" 