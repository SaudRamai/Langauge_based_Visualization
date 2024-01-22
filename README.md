# Langauge_based_visualization

This repository contains a project for natural language querying of structured databases, data visualization, and a user-friendly frontend.

## Project Structure

- **backend_api:**
  - `backend_api.py`: Contains the FastAPI server and API endpoints for database querying.
  - `cloudinary_integrations.py`: Manages interactions with Cloudinary for image uploads.
  - `database.py`: Defines the DatabaseConnection class for PostgreSQL connections.
  - `visualization.py`: Handles data visualization using the Open Interpreter tool.
  - `requirement.txt`: Lists project dependencies.

- **graph_history:** Folder to store generated visualizations.

- **env:** Virtual environment folder.

- **main_app.py:** Streamlit frontend for user interaction.

- **requirements.txt:** Specifies project dependencies.

## Prerequisites

- Python (3.10 or higher)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://gitlab.com/yourusername/langauge_based_visualization.git

Navigate to the project directory:
cd langauge_based_visualization

Install dependencies:
pip install -r requirements.txt

Usage
Database Connection and Querying:
Set up PostgreSQL database connection details in database.py.

Data Visualization:
Configure Cloudinary credentials in cloudinary_integrations.py.

API and Frontend:

Start the FastAPI server:
uvicorn backend_api:app --reload

Run the Streamlit frontend:
streamlit run main_app.py
Visit http://localhost:8501 to access the Streamlit app.

License
This project is licensed under the MIT License - see the LICENSE file for details.