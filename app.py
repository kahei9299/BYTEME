from flask import Flask, request, jsonify
from flask_cors import CORS
from demo_analyzer import InstantTikTokAnalyzer
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ---------------- Placeholder classes ----------------
class RewardCalculator:
    def calculate_reward(self, metrics):
        # Your existing reward calculation code
        overall = metrics.get("overall", 0)
        tier = "bronze"
        if overall >= 0.75:
            tier = "gold"
        elif overall >= 0.6:
            tier = "silver"
        return {
            "amount": int(overall * 1000),
            "breakdown": f"Base: {int(overall*500)} • Tier Bonus: +{int(overall*500)}",
            "tier": tier
        }

def generate_advice(metrics):
    recs = []
    for metric, value in metrics.items():
        if metric == "overall":
            continue
        if value < 6.0:
            recs.append(f"Improve your {metric} for better performance (current: {value:.1f}/10.0)")
        else:
            recs.append(f"{metric.capitalize()} looks good! ({value:.1f}/10.0)")
    return recs

# ---------------- Flask app ----------------
app = Flask(__name__)

# CORS configuration - CRITICAL for Lynx frontend
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})


# Replace with a simple API status endpoint
@app.route("/")
def index():
    return jsonify({
        "status": "success",
        "message": "TikTok Analyzer API is running",
        "endpoints": {
            "analyze_video": "POST /analyze-video"
        }
    })

@app.route("/analyze-video", methods=["POST", "OPTIONS"])
def analyze_video():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    logger.debug("Analyze video endpoint called")
    
    if "video" not in request.files:
        logger.warning("No video file in request")
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]
    logger.debug(f"Received file: {video_file.filename}")

    # Save video temporarily
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    filepath = upload_dir / video_file.filename
    
    try:
        video_file.save(filepath)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return jsonify({"error": f"Error saving file: {str(e)}"}), 500

    try:
        # Analyze video using YOLO analyzer
        analyzer = InstantTikTokAnalyzer()
        results = analyzer.analyze_video(str(filepath))

        metrics = results.get("metrics", {})
        logger.debug(f"Analysis results: {metrics}")

        # Transform metrics to frontend format (0-10 scale)
        transformed_metrics = {
            "accuracy": metrics.get("accuracy", 0.5) * 10,
            "plot_homogeneity": metrics.get("plot_homogeneity", 0.5) * 10,
            "comedic_value": metrics.get("comedic_value", 0.5) * 10,
            "theatrism": metrics.get("theatrism", 0.5) * 10,
            "plot_coherence": metrics.get("plot_coherence", 0.5) * 10,
            "overall": metrics.get("overall_score", 0.5) * 10
        }

        # Calculate rewards
        calculator = RewardCalculator()
        rewards = calculator.calculate_reward(transformed_metrics)

        # Generate recommendations
        recommendations = generate_advice(transformed_metrics)

        response_data = {
            "scores": transformed_metrics,
            "recommendations": recommendations,
            "earnings": rewards,
            "tier": rewards["tier"]
        }
        
        logger.debug(f"Sending response: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up temporary file
        try:
            if filepath.exists():
                filepath.unlink()
        except Exception as e:
            logger.warning(f"Error deleting temp file: {str(e)}")

def _build_cors_preflight_response():
    response = jsonify({"status": "OK"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

if __name__ == "__main__":
    logger.info("Starting Flask API server...")
    app.run(port=5000, debug=True, host='0.0.0.0')