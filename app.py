import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64
from utils.filters import ImageFilters
import os
import json
import requests
from urllib.parse import urlencode
from datetime import datetime

# --- Google OAuth Configuration ---
GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"  # Replace with your actual client ID
GOOGLE_CLIENT_SECRET = "your-google-client-secret"  # Replace with your actual client secret
GOOGLE_REDIRECT_URI = "http://localhost:8501"

def google_oauth_url():
    """Generate Google OAuth URL"""
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline'
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

def handle_google_callback(code):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': GOOGLE_REDIRECT_URI
        }
        response = requests.post(token_url, data=token_data)
        tokens = response.json()
        
        if 'access_token' in tokens:
            # Get user info
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f"Bearer {tokens['access_token']}"}
            user_response = requests.get(user_info_url, headers=headers)
            user_info = user_response.json()
            
            return {
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture')
            }
    except Exception as e:
        st.error(f"Google OAuth error: {str(e)}")
    return None

# --- User management ---
def load_users():
    """Load users from JSON file or return default users."""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default users for demo
        default_users = {
            'admin': 'admin123',
            'user': 'user123'
        }
        save_users(default_users)
        return default_users

def save_users(users):
    """Save users to JSON file."""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def signup_page():
    st.markdown('<h1 class="main-header">📝 Sign Up</h1>', unsafe_allow_html=True)
    
    # Google OAuth Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Continue with Google", use_container_width=True, key="google_signup"):
            st.markdown(f'<a href="{google_oauth_url()}" target="_self">Click here to authenticate with Google</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Or create account with email:")
    
    with st.form("signup_form"):
        new_username = st.text_input("Choose Username")
        new_email = st.text_input("Email Address")
        new_password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_signup = st.form_submit_button("Sign Up")
        with col2:
            back_to_login = st.form_submit_button("Back to Login")
        
        if submit_signup:
            users = load_users()
            
            if not new_username or not new_password or not new_email:
                st.error("Username, email and password are required!")
            elif new_username in users:
                st.error("Username already exists! Please choose a different one.")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long!")
            else:
                users[new_username] = {
                    'password': new_password,
                    'email': new_email,
                    'created_at': str(datetime.now())
                }
                save_users(users)
                st.success("Account created successfully! You can now login.")
                st.session_state['show_signup'] = False
                st.rerun()
        
        if back_to_login:
            st.session_state['show_signup'] = False
            st.rerun()

def login_page():
    st.markdown('<h1 class="main-header">🔒 Login to Image Filter App</h1>', unsafe_allow_html=True)
    
    # Google OAuth Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔐 Continue with Google", use_container_width=True, key="google_login"):
            st.markdown(f'<a href="{google_oauth_url()}" target="_self">Click here to authenticate with Google</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Or login with email:")
    
    # Check if user wants to signup
    if st.button("Don't have an account? Sign Up"):
        st.session_state['show_signup'] = True
        st.rerun()
    
    if st.session_state.get('show_signup', False):
        signup_page()
        return
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        
        if login_btn:
            users = load_users()
            if username in users:
                user_data = users[username]
                if isinstance(user_data, str):  # Old format
                    stored_password = user_data
                else:  # New format
                    stored_password = user_data.get('password', '')
                
                if stored_password == password:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid password!")
            else:
                st.error("Username not found!")

# Page configuration
st.set_page_config(
    page_title="Image Filter App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
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
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        border: 2px dashed #ddd;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App ---
def main():
    st.markdown('<h1 class="main-header">🎨 Image Filter App</h1>', unsafe_allow_html=True)
    
    # Add logout button in sidebar
    with st.sidebar:
        st.header("👤 User")
        st.write(f"Welcome, **{st.session_state.get('username', 'User')}**!")
        if st.button("🚪 Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()
        
        st.markdown("---")
        st.header("🛠️ Filters & Effects")
        filter_type = st.selectbox(
            "Choose Filter Type:",
            [
                "Basic Filters",
                "Artistic Effects", 
                "Adjustments",
                "Transformations",
                "Noise & Effects",
                "Crop & Resize"
            ]
        )
        if 'original_image' not in st.session_state:
            st.session_state.original_image = None
        if 'processed_image' not in st.session_state:
            st.session_state.processed_image = None
        if 'current_filter' not in st.session_state:
            st.session_state.current_filter = None
        if 'crop_coords' not in st.session_state:
            st.session_state.crop_coords = None
    
    # --- Layout: Always show both columns with proper alignment ---
    st.markdown("### 📸 Image Processing")
    
    # Upload section
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload an image to apply filters"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_array = np.array(image)
        if len(image_array.shape) == 3 and image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        st.session_state.original_image = image_array
        st.session_state.processed_image = image_array.copy()
        st.success("✅ Image uploaded successfully!")
    
    # Image display section - always show both images side by side
    if st.session_state.original_image is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Original Image")
            st.image(st.session_state.original_image, channels="RGB", use_container_width=True)
        
        with col2:
            st.subheader("🎯 Processed Image")
            apply_filters(filter_type, st.session_state.original_image)
            if st.session_state.processed_image is not None:
                st.image(st.session_state.processed_image, channels="RGB", use_container_width=True)
                download_processed_image()
    else:
        # Show placeholder when no image is uploaded
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📤 Original Image")
            st.markdown('<div class="image-container">👆 Please upload an image to get started!</div>', unsafe_allow_html=True)
        with col2:
            st.subheader("🎯 Processed Image")
            st.markdown('<div class="image-container">Image will appear here after processing</div>', unsafe_allow_html=True)

def apply_filters(filter_type, original_image):
    with st.sidebar:
        if filter_type == "Basic Filters":
            st.subheader("🔧 Basic Filters")
            if st.button("Grayscale"):
                st.session_state.processed_image = ImageFilters.apply_grayscale(original_image)
                st.session_state.current_filter = "Grayscale"
            if st.button("Sepia"):
                st.session_state.processed_image = ImageFilters.apply_sepia(original_image)
                st.session_state.current_filter = "Sepia"
            if st.button("Blur"):
                kernel_size = st.slider("Blur Intensity", 3, 31, 15, step=2)
                st.session_state.processed_image = ImageFilters.apply_blur(original_image, kernel_size)
                st.session_state.current_filter = f"Blur (Kernel: {kernel_size})"
            if st.button("Sharpen"):
                st.session_state.processed_image = ImageFilters.apply_sharpen(original_image)
                st.session_state.current_filter = "Sharpen"
            if st.button("Edge Detection"):
                st.session_state.processed_image = ImageFilters.apply_edge_detection(original_image)
                st.session_state.current_filter = "Edge Detection"
            if st.button("Invert"):
                st.session_state.processed_image = ImageFilters.apply_invert(original_image)
                st.session_state.current_filter = "Invert"
        elif filter_type == "Artistic Effects":
            st.subheader("🎨 Artistic Effects")
            if st.button("Cartoon"):
                st.session_state.processed_image = ImageFilters.apply_cartoon(original_image)
                st.session_state.current_filter = "Cartoon"
            if st.button("Vintage"):
                st.session_state.processed_image = ImageFilters.apply_vintage(original_image)
                st.session_state.current_filter = "Vintage"
            if st.button("Emboss"):
                st.session_state.processed_image = ImageFilters.apply_emboss(original_image)
                st.session_state.current_filter = "Emboss"
            if st.button("Pencil Sketch"):
                st.session_state.processed_image = ImageFilters.apply_pencil_sketch(original_image)
                st.session_state.current_filter = "Pencil Sketch"
            if st.button("HDR Effect"):
                st.session_state.processed_image = ImageFilters.apply_hdr(original_image)
                st.session_state.current_filter = "HDR Effect"
            if st.button("Color Splash"):
                st.session_state.processed_image = ImageFilters.apply_color_splash(original_image)
                st.session_state.current_filter = "Color Splash"
        elif filter_type == "Adjustments":
            st.subheader("⚙️ Adjustments")
            brightness = st.slider("Brightness", -100, 100, 0)
            contrast = st.slider("Contrast", -100, 100, 0)
            if st.button("Apply Brightness/Contrast"):
                st.session_state.processed_image = ImageFilters.apply_brightness_contrast(
                    original_image, brightness, contrast
                )
                st.session_state.current_filter = f"Brightness: {brightness}, Contrast: {contrast}"
            st.subheader("🎨 Color Balance")
            red_adj = st.slider("Red", -50, 50, 0)
            green_adj = st.slider("Green", -50, 50, 0)
            blue_adj = st.slider("Blue", -50, 50, 0)
            if st.button("Apply Color Balance"):
                st.session_state.processed_image = ImageFilters.apply_color_balance(
                    original_image, red_adj, green_adj, blue_adj
                )
                st.session_state.current_filter = f"Color Balance (R:{red_adj}, G:{green_adj}, B:{blue_adj})"
            if st.button("Histogram Equalization"):
                st.session_state.processed_image = ImageFilters.apply_histogram_equalization(original_image)
                st.session_state.current_filter = "Histogram Equalization"
        elif filter_type == "Transformations":
            st.subheader("🔄 Transformations")
            rotation_angle = st.slider("Rotation Angle", -180, 180, 0)
            if st.button("Rotate"):
                st.session_state.processed_image = ImageFilters.apply_rotate(original_image, rotation_angle)
                st.session_state.current_filter = f"Rotate {rotation_angle}°"
            mirror_direction = st.selectbox("Mirror Direction", ["horizontal", "vertical"])
            if st.button("Mirror"):
                st.session_state.processed_image = ImageFilters.apply_mirror(original_image, mirror_direction)
                st.session_state.current_filter = f"Mirror {mirror_direction}"
            scale_factor = st.slider("Scale Factor", 0.1, 3.0, 1.0, 0.1)
            if st.button("Resize"):
                st.session_state.processed_image = ImageFilters.apply_resize(original_image, scale=scale_factor)
                st.session_state.current_filter = f"Resize {scale_factor}x"
        elif filter_type == "Noise & Effects":
            st.subheader("📊 Noise & Effects")
            noise_type = st.selectbox("Noise Type", ["gaussian", "salt_pepper", "poisson"])
            noise_intensity = st.slider("Noise Intensity", 0.01, 0.5, 0.1, 0.01)
            if st.button("Add Noise"):
                st.session_state.processed_image = ImageFilters.apply_noise(
                    original_image, noise_type, noise_intensity
                )
                st.session_state.current_filter = f"{noise_type.title()} Noise ({noise_intensity})"
        elif filter_type == "Crop & Resize":
            st.subheader("✂️ Crop & Resize")
            
            # Get image dimensions
            height, width = original_image.shape[:2]
            
            # Crop controls
            st.write("**Crop Image:**")
            crop_left = st.slider("Left", 0, width, 0, key="crop_left")
            crop_top = st.slider("Top", 0, height, 0, key="crop_top")
            crop_right = st.slider("Right", crop_left, width, width, key="crop_right")
            crop_bottom = st.slider("Bottom", crop_top, height, height, key="crop_bottom")
            
            if st.button("Apply Crop"):
                cropped_image = original_image[crop_top:crop_bottom, crop_left:crop_right]
                st.session_state.processed_image = cropped_image
                st.session_state.current_filter = f"Crop ({crop_left},{crop_top},{crop_right},{crop_bottom})"
            
            st.markdown("---")
            st.write("**Resize Image:**")
            resize_width = st.number_input("Width", min_value=1, max_value=2000, value=width, key="resize_width")
            resize_height = st.number_input("Height", min_value=1, max_value=2000, value=height, key="resize_height")
            
            if st.button("Apply Resize"):
                resized_image = ImageFilters.apply_resize(original_image, width=resize_width, height=resize_height)
                st.session_state.processed_image = resized_image
                st.session_state.current_filter = f"Resize ({resize_width}x{resize_height})"
        
        if st.button("🔄 Reset to Original"):
            st.session_state.processed_image = original_image.copy()
            st.session_state.current_filter = "Original"
        if st.session_state.current_filter:
            st.info(f"Current Filter: {st.session_state.current_filter}")

def download_processed_image():
    if st.session_state.processed_image is not None:
        pil_image = Image.fromarray(st.session_state.processed_image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Handle case when current_filter is None
        filter_name = st.session_state.current_filter or "original"
        safe_filter_name = filter_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace(':', '')
        
        st.download_button(
            label="💾 Download Processed Image",
            data=buffer.getvalue(),
            file_name=f"filtered_image_{safe_filter_name}.png",
            mime="image/png"
        )

# --- Streamlit App Entry Point ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    login_page()
else:
    main()
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎨 Image Filter App - Transform your images with powerful filters and effects</p>
        <p>Built with Streamlit, OpenCV, and Python</p>
    </div>
    """, unsafe_allow_html=True)
