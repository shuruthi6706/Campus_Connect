# CampusConnect
## Campus Complaint Management System

A production-ready web application for educational institutions to streamline complaint submission, assignment, resolution tracking, and analytics reporting.

### Key Features
- **Role-Based Access**: Student, Staff, Admin dashboards
- **Real-Time Analytics**: Interactive Chart.js visualizations  
- **Responsive Design**: Bootstrap 5 mobile-first interface
- **Secure Authentication**: Flask-Login with CSRF protection
- **File Uploads**: Evidence attachments for complaints
- **Zero-Config**: SQLite database deployment

### Quick Setup
```bash
git clone <repository>
cd campus_complaints
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
flask run
