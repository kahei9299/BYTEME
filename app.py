from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from demo_analyzer import InstantTikTokAnalyzer
from pathlib import Path

# ---------------- Placeholder classes ----------------
class RewardCalculator:
    def calculate_reward(self, metrics):
        # Example calculation
        overall = metrics.get("overall", 0)
        tier = "Bronze"
        if overall >= 0.75:
            tier = "Gold"
        elif overall >= 0.5:
            tier = "Silver"
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
        if value < 0.5:
            recs.append(f"Improve your {metric} for better performance")
        else:
            recs.append(f"{metric.capitalize()} looks good!")
    return recs

# ---------------- Flask app ----------------
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    # Serve the front-end HTML
    return send_from_directory('.', 'index.html')

@app.route("/analyze-video", methods=["POST"])
def analyze_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]

    # Save video temporarily
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    filepath = upload_dir / video_file.filename
    video_file.save(filepath)

    try:
        # Analyze video using YOLO analyzer
        analyzer = InstantTikTokAnalyzer()
        results = analyzer.analyze_video(str(filepath))  # Should return dict with metrics

        metrics = results.get("metrics", {})

        # Ensure 'overall' exists
        if "overall" not in metrics:
            if len(metrics) > 0:
                metrics["overall"] = sum(metrics.values()) / len(metrics)
            else:
                metrics["overall"] = 0.0

        # Calculate rewards
        calculator = RewardCalculator()
        rewards = calculator.calculate_reward(metrics)

        # Generate recommendations
        recommendations = generate_advice(metrics)

        return jsonify({
            "scores": metrics,
            "recommendations": recommendations,
            "earnings": rewards,
            "tier": rewards["tier"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if filepath.exists():
            filepath.unlink()  # Delete temporary file

if __name__ == "__main__":
    app.run(port=5000, debug=True)