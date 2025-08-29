# TikTok AI Analyzer

An AI-powered tool to analyze TikTok videos and rate them on 5 key metrics: Accuracy, Homogeneity, Comedy, Theatrism, and Coherence.

## 📁 Project Structure

```
BYTEME/
├── src/                    # Core modules
│   ├── data_collector.py   # Data management
│   ├── feature_extractor.py # Feature extraction
│   ├── simple_model.py     # AI model training
│   └── simple_tiktok_downloader.py # Video downloader
├── data/                   # Data storage
│   ├── videos/            # Downloaded videos
│   └── annotations.csv    # Video ratings database
├── train_model.py         # Training script (add data + train)
├── ai_analyzer.py         # AI analyzer (just enter URL)
├── webapp/                # 🌐 Web interface
│   ├── app.py            # Flask API server
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, assets
├── run_webapp.py         # Web app launcher
└── requirements.txt       # Dependencies
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train Your Model

```bash
python train_model.py
```

**Training Options:**

- Add single video with manual rating
- Add multiple videos with manual ratings
- View current dataset
- Train AI model

### 3. Analyze Videos

```bash
python ai_analyzer.py
```

**Just enter a TikTok URL and get instant analysis!**

## 🎯 How to Use

### 📝 Training (Adding Data)

```bash
python train_model.py
```

1. **Choose option 1 or 2** (single or batch)
2. **Enter TikTok URL**
3. **Watch video and rate** (1-10 for each metric)
4. **Confirm and add** to dataset
5. **Train model** when ready

### 🧪 Analyzing New Videos

```bash
python ai_analyzer.py
```

1. **Choose option 1** (analyze video)
2. **Enter TikTok URL**
3. **Get instant AI analysis** with:
   - 5 metric scores (1-10)
   - Average score and reward tier
   - Improvement advice

### 🌐 Web Interface

```bash
python run_webapp.py
```

1. **Open browser** to http://localhost:8080
2. **Enter TikTok URL** in the beautiful web interface
3. **Get stunning visual results** with animations and progress bars
4. **View improvement advice** and reward tiers

## 📊 How It Works

### 1. Data Collection

- Download TikTok videos using `yt-dlp`
- Extract features (video, audio, text)
- Store ratings in `data/annotations.csv`

### 2. Feature Extraction

- **Video features**: Brightness, contrast, motion
- **Audio features**: MFCC, spectral centroid
- **Text features**: TF-IDF vectorization

### 3. AI Model

- Neural network with PyTorch
- 5 output neurons (one per metric)
- Trained on manual ratings

### 4. Analysis

- Extract features from new videos
- Use trained model to predict scores
- Generate improvement advice

## 🎯 Rating Metrics

1. **Accuracy** (1-10): Information accuracy and reliability
2. **Homogeneity** (1-10): Plot structure consistency
3. **Comedy** (1-10): Humor and entertainment value
4. **Theatrism** (1-10): Performance and dramatic elements
5. **Coherence** (1-10): Story flow and logical progression

## 🏆 Reward Tiers

- **Diamond**: 8.0+ average score
- **Gold**: 6.0-7.9 average score
- **Silver**: 4.0-5.9 average score
- **Bronze**: <4.0 average score

## 🔧 Key Features

### ✅ Realistic Scoring

- **Content-aware**: Adjusts based on video type (news, comedy, sports, food)
- **Randomization**: Adds realistic variation (±1 point)
- **Anti-overfitting**: Prevents all 10s scores

### ✅ Easy to Use

- **2 simple files**: Train and analyze
- **Just enter URL**: No complex setup
- **Instant analysis**: Get results immediately

### ✅ Smart Analysis

- **Improvement advice**: Based on lowest-scoring categories
- **Reward tiers**: Automatic classification
- **Content understanding**: Different scoring for different video types

## 📈 Current Status

- **7 videos** in training dataset
- **AI model** trained and functional
- **Realistic scoring** implemented
- **Simplified interface** ready

## 🎉 Ready to Use!

Your TikTok AI Analyzer is now super simple:

**For Training:**

```bash
python train_model.py
```

**For Analysis:**

```bash
python ai_analyzer.py
```

**That's it!** Just 2 files to train and analyze TikTok videos! 🎯
