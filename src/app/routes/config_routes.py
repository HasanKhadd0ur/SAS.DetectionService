import logging
from flask import Blueprint, request, jsonify
from app.detection.factory.strategy_factory import StrategyFactory
from app.detection.registry.strategy_registry import StrategyRegistry
from app.detection.factory.detection_config import DetectionConfigManager
from app.core.services.logging_service import LoggingService  # Import LoggingService

config_bp = Blueprint("config", __name__)

# Initialize the logger using LoggingService
logger = LoggingService(name="ConfigRoutes",level=logging.DEBUG).get_logger()

@config_bp.route("/set-strategy", methods=["POST"])
def set_strategy():
    data = request.get_json()
    name = data.get("strategy_name")

    if not name:
        logger.warning("No strategy_name provided in request")
        return jsonify({"error": "strategy_name is required"}), 400

    try:
        strategy = StrategyFactory.create_strategy(name)
        DetectionConfigManager.set_strategy(name, strategy)
        logger.info(f"Strategy set to {name}")
        return jsonify({"message": f"Strategy set to {name}"}), 200
    except ValueError as e:
        logger.error(f"Failed to set strategy: {e}")
        return jsonify({"error": str(e)}), 400

@config_bp.route("/get-strategy", methods=["GET"])
def get_strategy():
    name = DetectionConfigManager.get_current_strategy_name()
    logger.info(f"Current strategy requested: {name}")
    return jsonify({"current_strategy": name})

@config_bp.route("/list-strategies", methods=["GET"])
def list_strategies():
    strategies = StrategyRegistry.available_strategies()
    logger.info("Available strategies listed")
    return jsonify({"available_strategies": strategies})
