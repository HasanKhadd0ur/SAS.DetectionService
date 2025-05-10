# 🧠 SAS.DetectionService — Event Detection Microservice

This service is responsible for detecting and locating real-world events (e.g., disasters, crimes, major happenings) from raw social media messages using an AI-powered processing pipeline. It is part of the **SAS (Situational Awareness System)** platform.

---

## 📁 Project Structure

```
SAS.DetectionService/
├── assets/                     # Additional resources (e.g., models, configs)
├── src/
│   ├── app/
│   │   ├── core/               # Core logic (configs, models, services)
│   │   │   ├── configs/        # App configuration (env, constants)
│   │   │   ├── models/         # Pydantic data models
│   │   │   └── services/       # Application services (location inference, messaging, storage, etc.)
│   │   ├── detection/          # Event detection base components
│   │   ├── kafka/              # Kafka producer and consumer wrappers
│   │   ├── pipeline/           # Modular processing pipeline for event detection
│   │   │   ├── stages/         # Individual processing stages (locating, summarizing, publishing)
│   │   │   ├── pipeline.py     # Pipeline runner
│   │   │   └── registry.py     # Stage registry and configuration
│   │   ├── main.py             # Entry point
│   │   └── __init__.py
│   └── tests/                  # Unit and integration tests
├── .env                        # Environment variables (DO NOT COMMIT SECRETS)
├── .gitignore
├── Dockerfile                  # Container configuration
├── Jenkinsfile                 # CI/CD build instructions
├── Makefile                    # Task shortcuts (build, test, etc.)
├── README.md
└── requirements.txt            # Python dependencies
```

---

## 🚀 Features

* ✅ **Kafka Integration** for scalable messaging
* 🧩 **Modular Pipeline Architecture** using dynamically registered stages
* 🌍 **Location Inference** from text using NLP
* 🧵 **Event Summarization & Deduplication**
* 📤 **Publishing Detected Events** to downstream services or databases
* 🔧 Easily extendable with new stages, models, or event types

---

## 🛠️ Setup & Development

### 1. Clone and enter the project

```bash
git clone https://github.com/HasanKhadd0ur/SAS.DetectionService.git
cd SAS.DetectionService
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
---

## 🧪 Running the Service

```bash
python src/app/main.py
```

> The service will start consuming messages from the Kafka topic, apply the event detection pipeline, and publish the results.

---

## 🧪 Testing

```bash
pytest src/tests/
```

---

## 🤖 CI/CD

This project uses **Jenkins** for automated build and testing. See `Jenkinsfile` for pipeline stages.

---

## 📄 License

MIT License. See `LICENSE` (to be added).

---

## 👨‍💻 Author

Hasan Khaddour — [@HasanKhadd0ur](https://github.com/HasanKhadd0ur)
