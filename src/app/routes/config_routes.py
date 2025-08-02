import logging
from flask import Flask, request, jsonify
from app.detection.factory.strategy_factory import StrategyFactory
from app.detection.registry.strategy_registry import StrategyRegistry
from app.detection.factory.detection_config import DetectionConfigManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = Flask(__name__)

@app.route("/set-strategy", methods=["POST"])
def set_strategy():
    data = request.get_json()
    name = data.get("strategy_name")

    if not name:
        logging.warning("Strategy name not provided in request")
        return jsonify({"error": "strategy_name is required"}), 400

    try:
        strategy = StrategyFactory.create_strategy(name)
        DetectionConfigManager.set_strategy(name, strategy)
        logging.info(f"Strategy changed successfully to '{name}'")
        return jsonify({"message": f"Strategy set to {name}"}), 200
    except ValueError as e:
        logging.error(f"Failed to set strategy: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route("/get-strategy", methods=["GET"])
def get_strategy():
    name = DetectionConfigManager.get_current_strategy_name()
    logging.info(f"Current strategy requested: '{name}'")
    return jsonify({"current_strategy": name})

@app.route("/list-strategies", methods=["GET"])
def list_strategies():
    strategies = StrategyRegistry.available_strategies()
    logging.info(f"Listing available strategies: {strategies}")
    return jsonify({"available_strategies": strategies})
