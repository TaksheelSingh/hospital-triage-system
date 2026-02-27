# 🩺 Hospital Triage System – Frontend

This is the frontend for the Hospital Triage and Doctor Consultation System.

Built using **Next.js (App Router)** with **Tailwind CSS** and **ShadCN UI**.

---

# 🚀 Tech Stack

- Next.js
- React (Client Components)
- Tailwind CSS
- ShadCN UI
- Lucide Icons

---

# 🧩 Features

## Doctor Dashboard

- Patient search by name
- Hierarchical patient → visit selection
- Scrollable visit list
- RHS structured clinical view
- Floating prescription modal
- Visit status badge
- Classification toggle (Critical / Needs Review)
- Prescription status dropdown
- Mark visit as completed

---

# 🎨 UI Architecture

## Layout Structure

Sidebar  
Header (sticky, consistent across system)  
Two-panel grid:

### Left Panel
- Search card (compact)
- Scrollable patient + visit list
- Format:  
  `Patient Name – Visit ID`

### Right Panel
- Structured patient vitals form layout
- RFV display
- Clinical snapshot
- Button to open prescription modal

### Prescription Modal (Floating)
- Add prescription row
- Dynamic table
- Status dropdown
- Delete action
- Mark as Completed button

---

# 🔁 Workflow

1. Search patient
2. Select visit
3. Review intake data
4. Add prescriptions
5. Update classification
6. Mark visit completed

---

# ⚙ Setup Instructions

## Install Dependencies

```bash
npm install
Run Dev Server
npm run dev

Frontend runs at:

http://localhost:3000
🔗 Backend Connection

Backend must be running at:

http://127.0.0.1:8000

Ensure CORS is enabled for:

http://localhost:3000

🧪 Current Status
Search route fixed
Proper visit filtering
Scrollable UI panels
Floating prescription modal implemented
Layout proportional adjustments applied
Header consistency maintained

📌 Notes
All medical data displayed is from backend API.
Prescription total tablets calculated server-side.
Visit selection required before consultation.