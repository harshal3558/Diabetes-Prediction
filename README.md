# 🏥 Diabetes Prediction System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Web%20App-0078D4?logo=microsoftazure&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6?logo=dvc&logoColor=white)
![Git](https://img.shields.io/badge/Git-2.47-F05032?logo=git&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive Machine Learning Web Application designed to predict the likelihood of diabetes in patients based on diagnostic measures. This project leverages advanced ML algorithms and is fully containerized and deployed using **Azure Container Registry (ACR)** and **Azure Web App**.

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Data Versioning](#-data-versioning)
- [Demo](#-demo)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Running with Docker](#running-with-docker)
- [Deployment on Azure](#-deployment-on-azure)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 📖 About the Project

The **Diabetes Prediction System** utilizes a robust machine learning pipeline to analyze health metrics (such as Glucose levels, BMI, Age, etc.) and provide an instant prediction on whether a patient is diabetic.

The system is built with a modular architecture, ensuring scalability and maintainability. It includes data ingestion, transformation, model training, and a user-friendly web interface powered by Flask.

---

## ✨ Key Features
- **Accurate Predictions**: Uses ensemble learning techniques (XGBoost, LightGBM, CatBoost) for high accuracy.
- **Web Interface**: Simple and intuitive UI for entering patient data.
- **RESTful API**: Exposes endpoints for programmatic access to predictions.
- **Data Versioning**: Utilizes **DVC** to track and manage datasets and model artifacts.
- **Containerized**: Fully Dockerized for consistent environments across development and production.
- **Cloud Native**: Optimized for deployment on Azure cloud infrastructure.

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask, Gunicorn |
| **Machine Learning** | Scikit-learn, XGBoost, LightGBM, CatBoost, Pandas, NumPy |
| **Frontend** | HTML5, CSS3, Jinja2 Templates |
| **Database** | MySQL |
| **Version Control** | Git, DVC (Data Version Control) |
| **DevOps & Cloud** | Docker, Azure Container Registry (ACR), Azure Web App, GitHub Actions (CI/CD) |
| **Tracking** | MLflow, DagsHub |

---

## 📂 Project Architecture

```
Diabetes-Prediction/
├── .github/workflows/    # CI/CD Pipelines
├── artifacts/            # Trained models and preprocessors
├── notebook/             # Jupyter notebooks for experimentation
├── src/                  # Source code for the ML pipeline
│   └── DIAP/             # Main package
│       ├── components/   # Data ingestion, transformation, training
│       ├── pipelines/    # Training and Prediction pipelines
│       └── utils.py      # Utility functions
├── templates/            # HTML templates for the Web App
├── application.py        # Main Flask application entry point
├── Dockerfile            # Docker configuration
├── requirements.txt      # Project dependencies
└── ...
```

---

## 💾 Data Versioning

This project uses **DVC (Data Version Control)** to manage datasets and machine learning models. DVC helps in tracking changes in data and artifacts just like Git tracks code.

**Key benefits used in this project:**
- **Reproducibility**: Ensures that models are trained on specific versions of data.
- **Storage Efficiency**: Large files are stored remotely (e.g., S3, Azure Blob, GDrive) and only pointers (*.dvc files) are committed to Git.

To pull the latest data and models:
```bash
dvc pull
```

---

## 🎥 Demo

### App Running Video
> *[Insert Link to Your App Running Video Here]*

### Screenshots
| Home Page | Prediction Result |
|-----------|-------------------|
| *[Add Screenshot]* | *[Add Screenshot]* |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- Docker (optional, for containerization)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshal3558/Diabetes-Prediction.git
   cd Diabetes-Prediction
   ```

2. **Create a Virtual Environment**
   ```bash
   conda create -p denv python=3.10 -y
   conda activate ./denv
   # OR using venv
   python -m venv denv
   source denv/bin/activate  # On Windows: denv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python application.py
   ```
   Access the app at `http://127.0.0.1:5000`

### Running with Docker

1. **Build the Docker Image**
   ```bash
   docker build -t diabetes-prediction-app .
   ```

2. **Run the Container**
   ```bash
   docker run -p 5000:5000 diabetes-prediction-app
   ```
   Access the app at `http://localhost:5000`

---

## ☁ Deployment on Azure

This application is designed to be deployed using **Azure Container Registry (ACR)** and **Azure Web App for Containers**.

### Steps to Deploy:

1. **Push Image to Azure Container Registry (ACR)**
   ```bash
   # Login to Azure
   az login
   
   # Login to ACR
   az acr login --name <your-registry-name>
   
   # Tag the image
   docker tag diabetes-prediction-app <your-registry-name>.azurecr.io/diabetes-app:v1
   
   # Push to ACR
   docker push <your-registry-name>.azurecr.io/diabetes-app:v1
   ```

2. **Deploy to Azure Web App**
   - Go to Azure Portal -> Create a resource -> **Web App**.
   - Select **Docker Container** as the publish method.
   - Choose **Azure Container Registry** as the image source.
   - Select the registry, image, and tag you just pushed.
   - Set the startup command (if needed): `gunicorn --bind 0.0.0.0:8000 application:app` (Azure Web Apps default to port 8000 or 80 inside the container, map accordingly).

---

## 🔌 API Endpoints

- **`GET /indexing`**: Renders the index page.
- **`GET /predictdata`**: Renders the input form.
- **`POST /predictdata`**: Handles form submission and returns the prediction result.

**Input Parameters:**
- `pregnancies` (int)
- `glucose` (int)
- `blood_pressure` (int)
- `skin_thickness` (int)
- `insulin` (int)
- `bmi` (float)
- `diabetes_pedigree_function` (float)
- `age` (int)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📩 Contact

**Harshal** - [harshal3558@gmail.com](mailto:harshal3558@gmail.com)

Project Link: [https://github.com/harshal3558/Diabetes-Prediction](https://github.com/harshal3558/Diabetes-Prediction)
