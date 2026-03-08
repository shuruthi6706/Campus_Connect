from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User, Complaint  # ← FIXED: Added Complaint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        department = request.form.get('department', 'General')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email, role=role, department=department)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return redirect(url_for('student_dashboard'))
    elif current_user.role == 'staff':
        return redirect(url_for('staff_dashboard'))
    else:
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    total = Complaint.query.count()
    open_complaints = Complaint.query.filter_by(status='Open').count()
    in_progress = Complaint.query.filter_by(status='In Progress').count()
    resolved = Complaint.query.filter_by(status='Resolved').count()
    total_users = User.query.count()
    recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total=total, open=open_complaints, 
                         in_progress=in_progress, resolved=resolved,
                         total_users=total_users, recent_complaints=recent_complaints)

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('student_dashboard.html', complaints=complaints)

@app.route('/student/submit', methods=['POST'])
@login_required
def submit_complaint():
    if current_user.role != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    complaint = Complaint(
        title=request.form['title'],
        category=request.form['category'],
        description=request.form['description'],
        priority=request.form['priority'],
        user_id=current_user.id
    )
    db.session.add(complaint)
    db.session.commit()
    flash('Complaint submitted successfully!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    complaints = Complaint.query.filter(
        Complaint.status.in_(['Open', 'In Progress'])
    ).order_by(Complaint.priority.desc(), Complaint.created_at).all()
    
    return render_template('staff_dashboard.html', complaints=complaints)

@app.route('/staff/assign/<int:complaint_id>', methods=['POST'])
@login_required
def assign_complaint(complaint_id):
    if current_user.role != 'staff':
        return jsonify({'error': 'Access denied'}), 403
    
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = 'In Progress'
    complaint.assigned_to = current_user.id
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Complaint assigned'})

@app.route('/staff/resolve/<int:complaint_id>', methods=['POST'])
@login_required
def resolve_complaint(complaint_id):
    if current_user.role != 'staff':
        return jsonify({'error': 'Access denied'}), 403
    
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = 'Resolved'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Complaint resolved'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@college.edu', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created: admin/admin123")
    app.run(debug=True, port=5000)
