# TrailService API

**Module:** MAL2018 Information Management and Retrieval  
**Student ID:** BSCS2506056  
**Course:** BSc (Hons) Computer Science (Cyber Security)  
**Year:** 2025/2026

---

## 📖 Project Overview

The **TrailService** is a RESTful API micro-service designed to manage hiking trail data for the "Trail Application" ecosystem. It serves as the central data management component, responsible for the persistent storage, retrieval, and modification of hiking trails, GPS points, and associated features.

This service is built using **Python** and **Flask**, utilizing **Connexion** for "contract-first" API development (OpenAPI 3.0) and **SQLAlchemy** for database interactions with Microsoft SQL Server.

### Key Features
* **CRUD Operations:** Full Create, Read, Update, Delete functionality for Trails, Categories, Difficulties, and Route Types.
* **Spatial Data Management:** Manages trails as a composition of multiple GPS points (One-to-Many relationship).
* **Secure Authentication:** Implements stateless **JWT (JSON Web Token)** authentication to enforce Role-Based Access Control (RBAC).
* **Privacy-First Design:** Public endpoints provide a "Limited View" that automatically sanitizes sensitive data (e.g., `User_ID`) to comply with GDPR.
* **Interactive Documentation:** Automatically generated Swagger UI for testing and exploration.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11+
* **Framework:** Flask & Connexion
* **Database:** Microsoft SQL Server (via ODBC Driver 18)
* **ORM:** SQLAlchemy
* **Serialization:** Marshmallow
* **Authentication:** PyJWT
* **Specification:** OpenAPI 3.0 (Swagger)

---

## ⚙️ Installation & Setup

### Prerequisites
Ensure you have the following installed on your machine:
* Python 3.x
* Microsoft SQL Server (Local or Remote)
* [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/TrailService.git
cd TrailService

### 2. Install Dependencies
Create a virtual environment (optional but recommended) and install the required packages:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

### 3. Database Configuration
Ensure your SQL Server is running. The application is configured to connect to `localhost` with the following default credentials (see `config.py`):
* **Server:** `localhost`
* **Database:** `MAL2018_Information_Management_Retrieval`
* **User:** `SA`
* **Password:** `C0mp2001!`

*If your database credentials differ, please update `config.py` before proceeding.*

### 4. Build and Seed the Database
Run the initialization script to create the schema (`CW2`), tables, views, and seed sample data:
```bash
python build_database.py

🚀 Usage
1. Start the Server
Run the application using the following command:
```bash
python app.py
The server will start on http://0.0.0.0:8000.

2. Access Swagger UI
Open your web browser and navigate to: 👉 http://localhost:8000/api/ui

This interface allows you to interact with the API endpoints directly.

3. Authentication (How to Login)
Most POST, PUT, and DELETE endpoints are protected and require an Admin token.
- Go to the /login endpoint in Swagger UI.
- Use the following sample Admin credentials (seeded by build_database.py):
  - Email: grace@plymouth.ac.uk
  - Password: ISAD123!
- Copy the token string from the response.
- Click the Authorize 🔓 button at the top of the Swagger page and paste the token (Format: Bearer <your-token>).

⚖️ Legal, Social, Ethical, and Professional (LSEP)
This project strictly adheres to LSEP principles as detailed in the project report:
- Legal (Privacy): Complies with GDPR via "Data Minimization." The TrailPublicSchema ensures that Personally Identifiable Information (PII), such as the creator's User ID, is stripped from public API responses.
- Social (Trust): Prevents digital vandalism by restricting "Write" access to authorized Administrators only, ensuring the community can trust the integrity of the trail data.
- Ethical (Security): Mitigates OWASP Top 10 risks.
  - Broken Access Control is prevented via JWT Role-Based Access Control.
  - SQL Injection is prevented by using parameterized Stored Procedures (sp_InsertTrail, etc.) for all database modifications.
- Professional (Standards): Adheres to the OpenAPI 3.0 standard for documentation and follows strict separation of concerns (Modularity) in the codebase structure.

📂 Project Structure
TrailService/
├── app.py              # Application entry point
├── config.py           # Database and Flask configuration
├── models.py           # SQLAlchemy database models & Marshmallow schemas
├── auth.py             # JWT handling and login logic
├── trails.py           # Core business logic (CRUD) for Trails
├── lookups.py          # Logic for Categories, Difficulties, Route Types
├── features.py         # Logic for Trail Features
├── build_database.py   # Database seeding and initialization script
├── swagger.yml         # OpenAPI 3.0 specification
└── requirements.txt    # Python dependencies

🔗 References
OpenAPI (2025) OpenAPI specification, Swagger. Available at: https://swagger.io/specification/ (Accessed: 10 December 2025). 
OWASP (2021) OWASP Top 10, Owasp top 10:2021. Available at: https://owasp.org/Top10/2021/ (Accessed: 10 December 2025). 
VanMSFT (2025) SQL Injection - SQL server, SQL Injection - SQL Server | Microsoft Learn. Available at: https://learn.microsoft.com/en-us/sql/relational-databases/security/sql-injection?view=sql-server-ver17 (Accessed: 10 December 2025). 
