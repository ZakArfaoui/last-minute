# last-minute

# 🏦 Credit Risk Assessment System

A Streamlit-based web application for credit risk assessment, featuring separate portals for clients and banking officers. The system uses machine learning (XGBoost) with a fallback rule-based estimator for credit eligibility scoring.

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Authentication](#authentication)
- [Credit Scoring Logic](#credit-scoring-logic)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Client Portal
- Check credit eligibility without affecting credit score
- Instant results based on financial profile
- Personalized tips for improving approval chances
- No registration required for basic check

### Banker Dashboard
- Internal risk assessment tools for credit officers
- Detailed risk metrics (PD, EAD, LGD, EL)
- Visual risk factor contributions
- Manual review recommendations

### Authentication System
- Role-based access control (Client vs Banker)
- Persistent user storage in JSON format
- Secure session management

---

## 🏗️ System Architecture
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   register.py   │────▶│  Client Portal  │     │ Banker Dashboard│
│   (Auth/Entry)  │     │  (pages/client) │     │ (pages/banker)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                       │                       │
└───────────────────────┴───────────────────────┘
│
┌─────────────────┐
│  ML Model /     │
│  Rule-Based     │
│  Estimator      │
└─────────────────┘
plain
Copy

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- pip or conda

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd scoring_pipline
Create virtual environment
bash
Copy
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
Install dependencies
bash
Copy
pip install -r requirements.txt
Run the application
bash
Copy
streamlit run register.py
Access the app
Open browser: http://localhost:8501
🐳 Docker Deployment
Quick Start with Docker Compose
bash
Copy
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
Manual Docker Build
bash
Copy
# Build image
docker build -t credit-risk-app .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/users.txt:/app/users.txt \
  credit-risk-app
Docker Environment Variables
Table
Variable	Default	Description
STREAMLIT_SERVER_PORT	8501	Server port
STREAMLIT_SERVER_HEADLESS	true	Run without browser
STREAMLIT_SERVER_ENABLECORS	false	CORS policy
📖 Usage
First Time Setup
Register accounts
Go to "Register" tab
Create Client account (User 👤) for testing client portal
Create Banker account (Bank 🏦) for testing banker dashboard
Login and redirect
Client login → Auto-redirects to Client Portal
Banker login → Auto-redirects to Banker Dashboard
Client Portal Workflow
Enter financial information:
Monthly income
Desired credit amount
Affordable monthly payment
Employment duration
Answer profile questions:
Credit history
Savings habits
Employment type
Get instant eligibility score (0-100)
View personalized improvement tips if score < 80
Banker Dashboard Workflow
Enter client reference and financial data
Adjust external bureau scores (0-1 scale)
View comprehensive risk analysis:
Probability of Default (PD)
Exposure at Default (EAD)
Loss Given Default (LGD)
Expected Loss (EL)
Get approval/review/decline recommendation
📁 File Structure
plain
Copy
scoring_pipline/
├── README.md                    # This file
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker orchestration
├── requirements.txt             # Python dependencies
├── .dockerignore                # Docker build exclusions
├── register.py                  # Main entry point (auth)
├── tunisian_credit_model.pkl    # Trained XGBoost model
├── users.txt                    # User database (JSON)
└── pages/                       # Streamlit pages directory
    ├── client_portal.py         # Client eligibility checker
    └── banker_dashboard.py      # Banker risk assessment
🔐 Authentication
User Storage Format (users.txt)
JSON
Copy
{
  "user@example.com": {
    "first_name": "Ahmed",
    "last_name": "Ben Ali",
    "password": "hashed_or_plain",
    "role": "User 👤",
    "created_at": "2026-04-19T07:15:00"
  },
  "banker@banque.tn": {
    "first_name": "Sami",
    "last_name": "Trabelsi",
    "password": "secure123",
    "role": "Bank 🏦",
    "created_at": "2026-04-19T07:20:00"
  }
}
Security Notes
⚠️ Development Only: Passwords stored in plain text. For production:
Use bcrypt/argon2 for password hashing
Implement JWT tokens
Add HTTPS/TLS encryption
Use proper database (PostgreSQL/MySQL)
🧮 Credit Scoring Logic
Risk Components (Rule-Based Fallback)
Table
Factor	Weight	Calculation
Credit/Income Ratio	35%	credit_amount / monthly_income
Income Level	25%	Absolute minimum threshold
DTI (Debt-to-Income)	15%	monthly_payment / income
Credit History	10%	Bureau scores average
Employment Stability	10%	Years at current job
Overdue Days	5%	BCT registry delinquency
Score Interpretation
Table
Score	Status	Action
80-100	✅ Eligible	Proceed with application
58-79	⚠️ Maybe	Manual review required
0-57	❌ Unlikely	Decline with improvement tips
Formula
plain
Copy
risk_probability = Σ(component_risk × weight)
eligibility_score = (1 - risk_probability) × 100
🛠️ Development
Adding New Features
New page: Create file in pages/ directory
New model: Replace tunisian_credit_model.pkl and update FEATURE_COLUMNS
New fields: Update forms in both portals
Testing
bash
Copy
# Run with hot reload
streamlit run register.py --server.runOnSave true

# Debug mode
streamlit run register.py --logger.level debug
Model Retraining
Python
Copy
# After training new model
import joblib
joblib.dump(best_model, 'tunisian_credit_model.pkl')
🐛 Troubleshooting
Common Issues
Table
Issue	Solution
ModuleNotFoundError	Run pip install -r requirements.txt
users.txt not found	Ensure file exists in project root
Model not loading	Check tunisian_credit_model.pkl exists
Pages not found	Verify pages/ directory structure
Port already in use	Change port: --server.port 8502
Docker Issues
bash
Copy
# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check container logs
docker logs credit-risk-app

# Execute inside container
docker exec -it credit-risk-app bash
Streamlit Pages Error
Ensure folder structure matches:
plain
Copy
register.py          ← Main file (NOT in pages/)
pages/               ← Must be lowercase
├── client_portal.py
└── banker_dashboard.py
