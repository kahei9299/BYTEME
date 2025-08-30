# 🌐 BYTEME Web Application

This directory contains the web interface for the BYTEME AI TikTok Analyzer.

## 📁 Directory Structure

```
webapp/
├── app.py                 # 🚀 Flask API server
├── templates/
│   └── index.html        # 🎨 Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css    # 🎨 CSS styling
│   └── js/
│       └── script.js     # ⚡ JavaScript functionality
└── README.md             # 📖 This file
```

## 🚀 Quick Start

### From Project Root:
```bash
python run_webapp.py
```

### From This Directory:
```bash
python app.py
```

## 🎯 Features

- **Modern UI**: Beautiful gradient design with glass morphism
- **Responsive**: Works on desktop, tablet, and mobile
- **Real-time Analysis**: Instant AI-powered TikTok video analysis
- **Visual Results**: Animated score displays and progress bars
- **Smart Advice**: AI-generated improvement recommendations

## 🔧 Development

### Adding New Features:
1. **HTML**: Edit `templates/index.html`
2. **CSS**: Edit `static/css/styles.css`
3. **JavaScript**: Edit `static/js/script.js`
4. **API**: Edit `app.py`

### File Organization:
- **Templates**: HTML files go in `templates/`
- **Static Files**: CSS, JS, images go in `static/`
- **API Logic**: Backend code stays in `app.py`

## 🌟 API Endpoints

- `GET /` - Main web app
- `POST /api/analyze` - Analyze TikTok video
- `GET /api/health` - Health check

## 🎨 Design System

- **Colors**: Purple-blue gradients (#667eea to #764ba2)
- **Font**: Inter (Google Fonts)
- **Icons**: Font Awesome 6.0
- **Effects**: Glass morphism, smooth animations

## 📱 Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## 🔍 Troubleshooting

### Static Files Not Loading:
- Check file paths in HTML
- Ensure Flask static route is correct
- Clear browser cache

### API Errors:
- Check server logs
- Verify TikTok URL format
- Ensure AI model is trained

## 🎉 Enjoy Your Beautiful Web App!
