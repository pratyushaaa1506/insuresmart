# InsureSmart AI

AI-powered Indian Health Insurance Recommendation System built using Flask, SQLite, HTML, CSS, Bootstrap, and Machine Learning concepts.

---

# Features

- User Authentication System
- Secure Login & Registration
- Password Hashing
- Health Insurance Premium Prediction
- Indian States & Union Territories Support
- Disease-Based Risk Analysis
- BMI Calculation using Height & Weight
- Insurance Recommendation Engine
- Premium Breakdown Analytics
- Dark / Light Mode
- Profile Dashboard
- Insurance Analytics Dashboard
- Responsive Modern UI
- External Insurance Website Redirects

---

# Tech Stack

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Backend
- Flask
- Flask Login
- Flask SQLAlchemy

## Database
- SQLite

## Machine Learning
- Scikit-learn
- Joblib

---

# Project Structure

```bash
medical-insurance-predictor/
│
├── static/
│   ├── style.css
│   └── darkmode.js
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── result.html
│   ├── plans.html
│   ├── profile.html
│   └── analytics.html
│
├── dataset/
│
├── app.py
├── train_model.py
├── model.pkl
├── requirements.txt
└── README.md
```

---

# How to Run the Project

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/insuresmart-ai.git
```

## Move into Project Folder

```bash
cd insuresmart-ai
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Flask App

```bash
python app.py
```

