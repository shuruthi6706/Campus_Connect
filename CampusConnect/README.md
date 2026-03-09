Campus Connect — Student Networking & Opportunity Platform

Campus Connect is a web application that helps students connect with each other, discover opportunities, share resources, and collaborate on projects. The platform allows students to create profiles, post events, share opportunities, and interact within a campus community.

Key Files

app.py – Main application file that runs the web app and handles routing.

templates/ – Contains HTML pages for the user interface.

index.html – Homepage of the platform

login.html – Student login page

register.html – Student registration page

dashboard.html – User dashboard

static/ – Stores static files like CSS, JavaScript, and images.

database/db.py – Handles database connection and data storage.

models/user_model.py – Defines user profile structure and database models.

routes/auth_routes.py – Manages login, registration, and authentication.

routes/event_routes.py – Handles event posting and viewing.

Environment Setup

Create a virtual environment and install the required dependencies from requirements.txt.

Example:

pip install -r requirements.txt

Install dependencies and start the application:

python -m pip install -r requirements.txt
python app.py

Then open the application in your browser:

http://localhost:5000


Features

Student profile creation

Event and opportunity sharing

Campus community networking

Resource and knowledge sharing

Simple and user-friendly interface

Notes

Ensure all dependencies in requirements.txt are installed before running the application.

Keep sensitive information like API keys and database credentials in environment variables instead of hardcoding them in the project files.