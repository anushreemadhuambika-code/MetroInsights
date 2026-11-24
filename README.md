# MetroInsights
### AI-Powered Metro Operations Intelligence Platform

MetroInsights is an AI-powered metro operations intelligence platform developed by a six-member team as part of a hackathon project. It combines document intelligence, passenger-demand analysis, and operational analytics to support smarter decision-making in metro operations.

The platform brings together AI-based document analysis and machine-learning-based demand prediction in an interactive Streamlit application.

---

## Project Overview

MetroInsights is designed to explore how artificial intelligence, machine learning, and data analytics can be applied to metro operations.

The platform consists of three major modules:

### 1. MetroDoc AI – Intelligent Document Analysis

MetroDoc AI helps users extract useful operational insights from documents.

**Key features:**
- Upload PDF and TXT documents.
- Analyse document content using Google's Gemini API.
- Extract relevant operational information and insights.
- Store document records in an SQLite database.
- Search and retrieve stored documents.
- Provide rule-based analysis as a fallback when AI analysis is unavailable.

### 2. Train Induction Planning – Passenger Demand Prediction

This module explores passenger-demand prediction to support train deployment planning.

**Key features:**
- Analyse passenger demand across stations and time slots.
- Predict passenger demand using a Random Forest Regressor.
- Examine demand patterns across different stations and periods.
- Calculate train capacity requirements.
- Generate train deployment recommendations based on predicted demand.

### 3. Operations Analytics Dashboard

The dashboard provides an overview of operational document data through interactive visualisations.

**Key features:**
- View document statistics.
- Analyse document categories and departments.
- Examine priority distributions.
- Explore operational information through interactive charts.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Integration | Google Gemini API |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas |
| Data Visualisation | Plotly |
| Database | SQLite |
| Document Processing | PyMuPDF |
| Environment Management | Python-dotenv |

---

## Project Structure

```text
MetroInsights/
│
├── app.py                 # Main Streamlit application
├── generate_data.py       # Passenger-demand demonstration data generator
├── train_data.csv         # Passenger-demand dataset (if included)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .env.example           # Environment variable template
├── .gitignore             # Git exclusion rules
│
└── metrodoc.db            # Local SQLite database (created at runtime)
```

**Note:** `metrodoc.db` is a local runtime database and is not included in the Git repository. The application can create its database when run locally.

---

## Dataset and Data Sources

The project was developed with reference to publicly available information from Kochi Metro Rail Limited (KMRL).

Official resources:

- [KMRL Open Data](https://kochimetro.org/open-data/)
- [KMRL Ridership Details](https://kochimetro.org/ridership/)

The passenger-demand demonstration dataset used by the current application is generated through `generate_data.py`. It contains 2,250 records covering five metro stations, 30 days, and hourly time slots. The script introduces weekday/weekend patterns, station-specific factors, and random variation to demonstrate demand analysis and prediction.

This generated dataset is intended for demonstration and model experimentation; it should not be interpreted as raw KMRL passenger-level data.

**KMRL attribution:** Contains data provided by Kochi Metro Rail Limited.

---

## Machine Learning Approach

The Train Induction Planning module uses a Random Forest Regressor to explore passenger-demand prediction.

The model is intended to identify demand patterns using station and time-related information and support train deployment planning.

The predicted passenger demand is used alongside train-capacity calculations to explore possible deployment requirements.

---

## Getting Started

Follow these steps to run MetroInsights locally.

### Prerequisites

- Python 3.10 or later
- Git
- A Google Gemini API key for AI-powered document analysis

### 1. Clone the Repository

```bash
git clone https://github.com/anushreemadhuambika-code/MetroInsights.git
cd MetroInsights
```

Replace the repository URL with your actual GitHub repository URL if it differs.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Copy the structure from `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_configured_gemini_model
```

Replace the placeholder values with your own valid Gemini API credentials and the model configured for the application.

**Important:** Never upload your actual `.env` file or expose your API key on GitHub.

### 5. Generate the Demonstration Dataset (If Needed)

If `train_data.csv` is not included in the repository, generate it using:

```bash
python generate_data.py
```

This creates the passenger-demand demonstration dataset used by the Train Induction Planning module.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser through Streamlit.

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key used for Gemini integration |
| `GEMINI_MODEL` | Gemini model configured for document analysis |

Refer to `.env.example` for the environment-variable template.

---

## Security and Data Management

The repository excludes sensitive and locally generated files.

The following files should remain outside version control:

- `.env` – Contains private API credentials.
- `metrodoc.db` – Local database that may contain uploaded document information.
- Python virtual environments.
- Python cache files.
- Local logs and temporary files.

The `.gitignore` file is configured to prevent these files from being accidentally committed.

---

## Team and Contributors

**Team Size:** 6 Members  
**Project Type:** Hackathon Project  
**Repository Maintainer:** [Anushree](https://github.com/anushreemadhuambika-code)

MetroInsights was developed collaboratively by a six-member team as a hackathon project.

---

## Project Objective

The objective of MetroInsights is to demonstrate how AI-powered document intelligence, machine learning, and interactive data analytics can be brought together to explore practical challenges in metro operations.

By combining document analysis with passenger-demand prediction and operational visualisation, the project demonstrates a data-driven approach to exploring operational efficiency and planning.

---

## Disclaimer

MetroInsights is an independent academic and hackathon project developed for educational and experimental purposes. It is not an official product of, affiliated with, or endorsed by Kochi Metro Rail Limited.

The project uses publicly available information as a reference and includes generated demonstration data for experimentation. Its predictions and recommendations are illustrative and should not be treated as official operational decisions.

