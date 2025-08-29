# 🌐 BYTEME Web App

A beautiful, modern web interface for your AI TikTok analyzer!

## ✨ Features

- **🎨 Modern Design**: Beautiful gradient backgrounds, smooth animations, and responsive layout
- **📱 Mobile Friendly**: Works perfectly on desktop, tablet, and mobile devices
- **⚡ Real-time Analysis**: Instant AI-powered TikTok video analysis
- **📊 Visual Results**: Animated score displays with progress bars and tier badges
- **💡 Smart Advice**: AI-generated improvement recommendations
- **🔄 Easy Reset**: Start new analysis with one click

## 🚀 Quick Start

### 1. Start the Web Server

```bash
# Activate your virtual environment
source venv/bin/activate

# Start the Flask server
python app.py
```

### 2. Open in Browser

Open your browser and go to: **http://localhost:8080**

### 3. Analyze Videos

1. Enter a TikTok URL
2. (Optional) Add a description
3. Click "Analyze"
4. Watch the magic happen! ✨

## 🎯 How It Works

1. **Input**: Enter any TikTok video URL
2. **Download**: The server downloads the video using yt-dlp
3. **Analysis**: Your AI model analyzes the video features
4. **Results**: Get scores for 5 metrics + improvement advice
5. **Visualization**: Beautiful animated display of results

## 📁 File Structure

```
BYTEME/
├── index.html          # 🎨 Main web app interface
├── styles.css          # 🎨 Beautiful CSS styling
├── script.js           # ⚡ JavaScript functionality
├── app.py              # 🚀 Flask API server
├── train_model.py      # 🧠 Training interface
├── ai_analyzer.py      # 🧠 Command-line analyzer
└── src/                # 📦 Core AI modules
```

## 🎨 Design Features

- **Gradient Backgrounds**: Purple-blue gradients for modern look
- **Glass Morphism**: Translucent cards with backdrop blur
- **Smooth Animations**: Loading steps, score animations, hover effects
- **Responsive Grid**: Adapts to any screen size
- **Tier Badges**: Color-coded reward tiers (Diamond, Gold, Silver, Bronze)
- **Progress Bars**: Visual representation of scores

## 🔧 Customization

### Colors

Edit `styles.css` to change the color scheme:

```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent colors */
color: #667eea;
```

### Animations

Adjust animation timing in `script.js`:

```javascript
// Score animation duration (ms)
this.animateNumber(element.score, 0, score, 1000);

// Loading step interval (ms)
}, 800);
```

## 🌟 API Endpoints

- `GET /` - Main web app
- `POST /api/analyze` - Analyze TikTok video
- `GET /api/health` - Health check

## 🎯 Usage Examples

### Basic Analysis

1. Go to http://localhost:8080
2. Paste TikTok URL: `https://www.tiktok.com/@user/video/1234567890`
3. Click "Analyze"
4. Get instant results!

### With Description

1. Enter TikTok URL
2. Add description: "Funny cooking tutorial with quick tips"
3. Click "Analyze"
4. Get context-aware analysis

## 🚨 Troubleshooting

### Server Won't Start

```bash
# Check if Flask is installed
pip install flask flask-cors

# Check if port 5000 is available
lsof -i :5000
```

### Analysis Fails

- Ensure yt-dlp is installed: `pip install yt-dlp`
- Check internet connection
- Verify TikTok URL format
- Check server logs for detailed error messages

### Web App Not Loading

- Ensure you're accessing http://localhost:8080
- Check browser console for JavaScript errors
- Verify all files are in the correct directory

## 🎉 Enjoy Your Beautiful AI Analyzer!

Your BYTEME web app is now ready to provide stunning, AI-powered TikTok analysis with a modern, professional interface! 🚀
