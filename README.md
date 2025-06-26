# 🎨 Image Filter App

A powerful and modern web application for applying various filters and effects to images. Built with Streamlit, OpenCV, and Python.

## ✨ Features

### 🎯 Basic Filters
- **Grayscale**: Convert images to black and white
- **Sepia**: Apply vintage sepia tone effect
- **Blur**: Gaussian blur with adjustable intensity
- **Sharpen**: Enhance image details
- **Edge Detection**: Canny edge detection
- **Invert**: Invert image colors

### 🎨 Artistic Effects
- **Cartoon**: Transform images into cartoon-style artwork
- **Vintage**: Apply retro vintage effect with vignette
- **Emboss**: Create 3D embossed effect

### ⚙️ Adjustments
- **Brightness & Contrast**: Fine-tune image exposure
- **Color Balance**: Adjust individual RGB channels
- **Histogram Equalization**: Enhance image contrast automatically

### 🔄 Transformations
- **Rotation**: Rotate images by any angle
- **Mirror**: Flip images horizontally or vertically
- **Resize**: Scale images up or down

### 📊 Noise & Effects
- **Gaussian Noise**: Add random noise
- **Salt & Pepper Noise**: Add impulse noise
- **Poisson Noise**: Add photon noise

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd image_filter_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📖 Usage

1. **Upload Image**: Click the upload area and select an image file (PNG, JPG, JPEG, BMP, TIFF)

2. **Choose Filter Category**: Select from the sidebar:
   - Basic Filters
   - Artistic Effects
   - Adjustments
   - Transformations
   - Noise & Effects

3. **Apply Filters**: Click on any filter button to apply the effect

4. **Adjust Parameters**: Use sliders to fine-tune filter parameters

5. **Download Result**: Click the download button to save your processed image

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **OpenCV**: Computer vision and image processing
- **Pillow**: Image manipulation
- **NumPy**: Numerical computing
- **Matplotlib**: Plotting and visualization
- **Scikit-image**: Advanced image processing

### Architecture
- **Modular Design**: Filters are organized in a separate `utils/filters.py` module
- **Session Management**: Uses Streamlit session state for image persistence
- **Real-time Processing**: Instant filter application with live preview
- **Responsive UI**: Modern, mobile-friendly interface

## 🎯 Key Features

- **Real-time Preview**: See changes instantly
- **Multiple Filter Categories**: Organized filter selection
- **Parameter Control**: Adjustable filter intensity
- **Download Support**: Save processed images
- **Reset Functionality**: Return to original image
- **Modern UI**: Clean, intuitive interface

## 🔧 Customization

### Adding New Filters
1. Add new filter method to `ImageFilters` class in `utils/filters.py`
2. Add corresponding button in `app.py`
3. Update filter categories as needed

### Modifying UI
- Edit CSS styles in the `st.markdown` section
- Modify layout using Streamlit columns and containers
- Add new sidebar sections for additional controls

## 🐛 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Image Format Issues**: Supported formats: PNG, JPG, JPEG, BMP, TIFF
3. **Memory Issues**: Large images may cause performance issues
4. **Display Issues**: Check browser compatibility

### Performance Tips
- Use smaller images for faster processing
- Close other applications to free up memory
- Use SSD storage for better I/O performance

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support and questions, please open an issue on the repository.

---

**Built with ❤️ using Streamlit, OpenCV, and Python** 