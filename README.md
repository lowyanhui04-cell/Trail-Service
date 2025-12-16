# TrailService API

**Module:** MAL2018 Information Management and Retrieval  
**Student ID:** BSCS2506056  
**Course:** BSc (Hons) Computer Science (Cyber Security)  
**Year:** 2025/2026

---

## 📖 Project Overview

[cite_start]The **TrailService** is a RESTful API micro-service designed to manage hiking trail data for the "Trail Application" ecosystem[cite: 1109]. It serves as the central data management component, responsible for the persistent storage, retrieval, and modification of hiking trails, GPS points, and associated features.

[cite_start]This service is built using **Python** and **Flask**, utilizing **Connexion** for "contract-first" API development (OpenAPI 3.0) and **SQLAlchemy** for database interactions with Microsoft SQL Server[cite: 1109, 1116].

### Key Features
* **CRUD Operations:** Full Create, Read, Update, Delete functionality for Trails, Categories, Difficulties, and Route Types.
* [cite_start]**Spatial Data Management:** Manages trails as a composition of multiple GPS points (One-to-Many relationship)[cite: 1061].
* [cite_start]**Secure Authentication:** Implements stateless **JWT (JSON Web Token)** authentication to enforce Role-Based Access Control (RBAC)[cite: 1094].
* [cite_start]**Privacy-First Design:** Public endpoints provide a "Limited View" that automatically sanitizes sensitive data (e.g., `User_ID`) to comply with GDPR.
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
git clone [https://github.com/](https://github.com/)lowyanhui04-cell/TrailService.git
cd TrailService