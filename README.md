🏎️ Bootcamp Rally Racing Management App
This project is a simple web application for managing racing cars and teams, and simulating rally races. It leverages Snowflake for data storage and Streamlit for the interactive user interface, all powered by Python.
The application allows users to:
View a dashboard of current teams, their budgets, cars, and upcoming races.
Add new racing teams.
Add new cars and assign them to existing teams.
Simulate a rally race, including participation fees, dynamic car performance based on characteristics and track type, and prize distribution.
View historical race results.

✨ Features
Snowflake Integration: Secure and scalable data storage for teams, cars, races, and results.
Team Management: Add new teams and track their budgets.
Car Management: Add new cars with detailed characteristics (speed, horsepower, handling, durability) and assign them to teams.
Race Simulation:
Simulates a 100km run, considering car characteristics (speed, horsepower, handling, durability).
Adjusts performance based on track type (Asphalt, Snow, Gravel).
Introduces random factors for unpredictable race outcomes.
Teams pay a participation fee.
Winning teams receive a prize from a prize pool, and their budgets are updated accordingly.
Interactive UI: Built with Streamlit for an intuitive and responsive user experience.
Demo Mode: If Snowflake connection fails or is not configured, the app runs with local demo data.

🛠️ Technologies Used
Frontend: Streamlit
Backend/Logic: Python
Database: Snowflake
Database Connector: snowflake-connector-python
Data Manipulation: Pandas

🚀 Setup and Installation
Follow these steps to set up and run the application.

1. Snowflake Database Setup
First, execute the provided SQL scripts in your Snowflake environment to create the necessary database, schemas, and tables (rally_schema.sql).

2. Python Environment Setup
Clone the repository:
git clone https://github.com/AnastasijaLe/rally-racing-management-app.git
cd rally-racing-management-app

Create a virtual environment (recommended):
python -m venv venv

Activate the virtual environment:
On Windows: .\venv\Scripts\activate
On macOS/Linux: source venv/bin/activate

Install dependencies:
Create a requirements.txt file in the root of your project with the following content:
streamlit
snowflake-connector-python
pandas

Then install them:
pip install -r requirements.txt

▶️ How to Run the App
Deploying to Streamlit Cloud
Commit your changes to your GitHub repository, including app.py and requirements.txt. Do not commit your secrets.toml file directly to GitHub. Streamlit Cloud has a secure way to manage secrets.

Go to Streamlit Cloud (share.streamlit.io).
Click "New app" and connect your GitHub repository.
Specify the main file as app.py.
In the "Advanced settings" or "Secrets" section on Streamlit Cloud, add your Snowflake credentials securely:

[snowflake]
user = "YOUR_SNOWFLAKE_USER"
password = "YOUR_SNOWFLAKE_PASSWORD"
account = "YOUR_SNOWFLAKE_ACCOUNT_IDENTIFIER" # e.g., 'xyz12345.us-east-1' or 'yourorg-youraccount'
warehouse = "YOUR_SNOWFLAKE_WAREHOUSE" # e.g., 'COMPUTE_WH'
database = "BOOTCAMP_RALLY"
schema = "PUBLIC" # Or specific schema if needed by your user's default settings
role = "YOUR_SNOWFLAKE_ROLE" # e.g., 'ACCOUNTADMIN' or a specific role

Deploy the app. 

🤝 Contributing
Feel free to fork this repository, open issues, and submit pull requests.

📝 License
This project is open-source. (Consider adding a specific license, e.g., MIT, Apache 2.0).
