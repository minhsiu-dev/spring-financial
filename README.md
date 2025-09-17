# 🚀 Dynamic Product Search Application

This is a full-stack web application that demonstrates a dynamic, real-time product filtering system. The project consists of a Python Flask REST API for the backend and a responsive frontend built with the Ionic Framework and React.

## ✨ Features

* **RESTful API:** A backend API for generating, retrieving, and searching products.
* **Dynamic Search:** A real-time search that filters products across multiple attributes (name, description, SKU, etc.) as the user types.
* **Mock Data Generation:** An endpoint to instantly populate the database with 100+ realistic product records.
* **Responsive Frontend:** A clean, mobile-first user interface built with Ionic/React components.
* **Optimized Performance:**
    * Frontend uses **debouncing** to limit API requests during rapid typing.
    * Backend uses **bulk inserts** for efficient data generation.
* **Automated Testing:** Includes a suite of tests for the critical search endpoint using Pytest.

---

## 💻 Tech Stack

### Backend
* **Language:** Python 3
* **Framework:** Flask
* **ORM:** SQLAlchemy
* **Database:** SQLite
* **Testing:** Pytest

### Frontend
* **Framework:** React
* **UI Toolkit:** Ionic Framework
* **Language:** TypeScript

---

## ⚙️ Setup and Installation

### Prerequisites
* Node.js and npm
* Python 3 and pip
* Git

### Backend
```
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create the instance folder and initialize the database
mkdir instance
flask init-db
flask run
```

### Frontend
```
cd frontend

# Install dependencies
npm install

ionic serve
```