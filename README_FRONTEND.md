# Secure AI-Driven Emergency Assistance Framework – Frontend

## Overview

This frontend application provides the user interface for the AI-assisted emergency triage system.

The frontend allows:
- Patient intake and visit registration
- Real-time severity prediction display
- Doctor dashboard access
- Prescription management
- Monitoring of patient workflows

The frontend communicates with the FastAPI backend through REST APIs.

---

# Technologies Used

- Next.js
- React.js
- Tailwind CSS
- Axios
- TypeScript

---

# Project Structure

```text
frontend/
│
├── app/
├── components/
├── pages/
├── services/
├── styles/
├── public/
└── package.json
```

---

# Frontend Setup Instructions

## 1. Install Dependencies

```bash
npm install
```

---

# 2. Run Development Server

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

# Backend Connection

Ensure the backend server is running:

```text
http://127.0.0.1:8000
```

Frontend API requests are connected through:
- Axios
- REST API endpoints

---

# Main Features

## Patient Intake Interface
- Patient registration
- Visit entry
- Vital signs input

---

## Doctor Dashboard
- View patient severity predictions
- Monitor visit history
- Manage prescriptions

---

## Severity Prediction Display
The frontend displays:
- Predicted severity level
- Risk probability
- Override status

---

## Prescription Management
Doctors can:
- Add prescriptions
- Update medicine details
- Manage treatment records

---

# Security Features

The frontend supports secure communication with backend APIs.

Sensitive data is processed securely through:
- AES-encrypted backend storage
- Integrity-verified prediction outputs
- IDS-monitored backend services

---

# Workflow

```text
Patient Input
      ↓
Backend API
      ↓
ML Severity Prediction
      ↓
Cybersecurity Validation
      ↓
Doctor Dashboard Response
```

---

# Output

The frontend provides:
- Interactive hospital workflow management
- Real-time emergency triage assistance
- Prescription and patient monitoring
- Secure integration with backend services

---

# Authors

- Taksheel Rawat
- Aryan Arora