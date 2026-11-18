# 🏥 Health Prediction Application

## 📌 Project Overview

The Health Prediction Application is a Python-based web application developed using Streamlit to manage patient information and blood test results. It collects patient details, including Full Name, Date of Birth, Email, Glucose, Haemoglobin, and Cholesterol levels.

The application integrates the Google Gemini API to generate AI-powered educational health interpretations based on patient blood test results. It also provides input validation and persistent data management using SQLite.

## ✨ Key Features

- **Patient Registration:** Add and store patient details and blood test results.
- **Input Validation:** Validate email addresses, dates of birth, and numerical blood test values.
- **CRUD Operations:** Create, Read, Update, and Delete patient records.
- **Database Management:** Store and retrieve patient information using SQLite.
- **AI-Powered Health Remarks:** Generate health interpretations using the Google Gemini API.
- **Failed Record Management:** Identify and maintain records that fail validation.
- **Interactive Dashboard:** Manage and view patient information through a Streamlit interface.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Google Gemini API
- Python-dotenv
- Requests

## 📂 Project Structure

```text
health-prediction-app/
│
├── app.py
├── database.py
├── validation.py
├── ai_service.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 👩‍💻 Author

**Saleth Mary**

Integrated B.Sc.–M.Sc. Data Science
