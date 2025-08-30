# BYTEME

BYTEME is an AI-powered web application that analyzes TikTok videos to extract features and generate insightful results using advanced machine learning techniques.

## Features

- Download and process TikTok videos
- Extract visual and audio features
- AI-driven analysis and result generation
- Modern frontend built with Lynx.js

## Getting Started

### Prerequisites

- Node.js (v16+ recommended)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kahei9299/BYTEME.git
   cd BYTEME
   ```

2. Install dependencies for the frontend:
   ```bash
   cd frontend-lynx
   npm install
   ```
   
3. Install dependencies for the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
### Running the Application

In the backend folder, the target video to be analysed must be at /backend/local_video.MP4. Lynx Explorer must also be running on the same device for this demo.

#### Frontend

```bash
cd frontend-lynx
npm run dev
```

#### Backend

```bash
cd backend
python ./app.py
```

## Project Structure

- `frontend-lynx/` — React-based frontend using Lynx.js
- `backend/` — API and AI processing logic

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

