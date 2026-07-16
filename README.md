# 🍽️ Mood-Based Restaurant Recommendation System

<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status" />
  <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License" />
</div>

## 📋 Overview

A sophisticated web application that leverages machine learning and natural language processing to recommend restaurants based on your current mood. Whether you're feeling happy, sad, stressed, or anything in between, our system will suggest the perfect dining options to complement your emotional state.

## 🎯 Aim & Objectives

- Develop an intuitive mood-based recommendation system for restaurant selection
- Implement machine learning algorithms to understand the relationship between moods and food preferences
- Create a responsive and user-friendly interface for seamless interaction
- Provide personalized recommendations based on location and price preferences
- Demonstrate practical applications of NLP in everyday decision-making

## 🛠️ Technologies Used

<div align="center">

| Category         | Technologies                                                                                                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**      | ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green) ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.25+-orange)                                                                                                      |
| **Data Science** | ![Pandas](https://img.shields.io/badge/Pandas-2.0+-blue) ![NumPy](https://img.shields.io/badge/NumPy-1.26+-green) ![Scikit-learn](https://img.shields.io/badge/ScikitLearn-1.4+-red)                                                                                                      |
| **Frontend**     | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **Deployment**   | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-0.17.0+-green)                                                                                                                             |

</div>

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)
- Git

## 📝 Detailed Execution Steps

### Windows

#### Option 1: Using Git Bash

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate
   ```

   If you encounter issues with the above command, you can try:

   ```bash
   # Alternative activation in Git Bash
   source .venv/Scripts/activate

   # Or using Command Prompt
   .\.venv\Scripts\activate.bat

   # Or using PowerShell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model (if needed)**
   If the model files don't exist, run:

   ```bash
   python model/train_model.py
   ```

5. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Backend API: Open your browser and navigate to `http://localhost:8000`
   - Frontend: Open `static/index.html` directly in your browser

   You can open the HTML file by running:

   ```bash
   # Using Git Bash
   start static/index.html

   # Or manually navigate to the project folder and open index.html
   ```

#### Option 2: Using Docker on Windows

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build Docker image**

   ```bash
   docker build -t restaurant-recommender .
   ```

3. **Run the container**

   ```bash
   docker run -p 8080:80 restaurant-recommender
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:8080`

### Linux/macOS

#### Option 1: Using Command Line

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model (if needed)**

   ```bash
   python3 model/train_model.py
   ```

5. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Backend API: Open your browser and navigate to `http://localhost:8000`
   - Frontend: Open the HTML file directly

     ```bash
     # On macOS
     open static/index.html

     # On Linux with xdg-open
     xdg-open static/index.html
     ```

#### Option 2: Using Docker on Linux/macOS

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build Docker image**

   ```bash
   docker build -t restaurant-recommender .
   ```

3. **Run the container**

   ```bash
   docker run -p 80:80 restaurant-recommender
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:80`

### Troubleshooting

- **Port conflicts**: If port 8000 or 80 is already in use, you can specify a different port:

  ```bash
  # For Uvicorn
  uvicorn app.main:app --reload --port 8001

  # For Docker
  docker run -p 8080:80 restaurant-recommender
  ```

- **Model loading issues**: If you encounter errors related to loading models, ensure you've run:

  ```bash
  python model/train_model.py
  ```

- **Python version compatibility**: Ensure you're using Python 3.8 or higher. Check with:
  ```bash
  python --version  # or python3 --version on Linux/macOS
  ```

## 🔍 Usage Guide

1. Input your current mood in the mood text field
2. (Optional) Specify your location preference
3. (Optional) Select your preferred price range
4. Click "Find Restaurants" to get personalized recommendations
5. Browse through the suggested restaurants and enjoy!

## 📈 Future Work

- Integrate real-time sentiment analysis from social media posts to detect user mood
- Implement user profiles and preference learning for improved personalization
- Add ratings and reviews functionality to enhance recommendations
- Develop mobile applications for iOS and Android platforms
- Expand dataset to include more global restaurants and diverse cuisines
- Integrate with mapping services for directions to recommended restaurants

## 👥 Contributors

This project was built with dedication by:

_Baishik Poddar_

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
