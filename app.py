
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
# pyrefly: ignore [missing-import]
import mysql.connector
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────
# APP CONFIGURATION
# ─────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'lms_super_secret_key_2024'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─────────────────────────────────────────────
# EMAIL CONFIGURATION
# ─────────────────────────────────────────────
EMAIL_CONFIG = {
    'sender_email': 'your_email@gmail.com',  # Update with your Gmail
    'sender_password': 'your_app_password',  # Use Google App Password (not regular password)
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dexter',
    'database': 'lms_db',
    'port': 3306,
    'autocommit': True
}

def get_db():
    """Get a new MySQL connection."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def query_db(sql, args=(), one=False, commit=False):
    """Helper to execute DB queries."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, args)
    if commit:
        conn.commit()
        result = cursor.lastrowid
    elif one:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(recipient_email, subject, body_html):
    """Send email notification to user."""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = recipient_email
        
        msg.attach(MIMEText(body_html, 'html'))
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_approval_email(user_email, user_name, institute_name):
    """Send approval notification email."""
    subject = "✅ Your Registration Has Been Approved!"
    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 8px; color: white; text-align: center;">
                    <h2 style="margin: 0;">🎉 Great News!</h2>
                </div>
                <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none;">
                    <p>Hi <strong>{user_name}</strong>,</p>
                    <p>Your registration request for <strong>{institute_name}</strong> has been <strong style="color: #28a745;">APPROVED</strong>! ✅</p>
                    <p>You can now log in to EduVerse LMS and start exploring courses. Click the link below to log in:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000/login" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Login Now</a>
                    </div>
                    <p style="color: #666; font-size: 13px;">If you have any issues, please contact the support team.</p>
                </div>
                <div style="background: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; color: #999;">
                    <p>EduVerse LMS © 2024. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    return send_email(user_email, subject, body_html)

def send_rejection_email(user_email, user_name, institute_name, reason):
    """Send rejection notification email."""
    subject = "Registration Request - Status Update"
    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; border-radius: 8px; color: white; text-align: center;">
                    <h2 style="margin: 0;">Registration Update</h2>
                </div>
                <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none;">
                    <p>Hi <strong>{user_name}</strong>,</p>
                    <p>Thank you for your interest in <strong>{institute_name}</strong>.</p>
                    <p>Unfortunately, your registration request has been <strong style="color: #dc3545;">REJECTED</strong> at this time.</p>
                    <p><strong>Reason:</strong> {reason if reason else 'The institute has decided not to approve your request at this time.'}</p>
                    <p>You can try registering again in the future or contact another institute. If you have questions, please reach out to our support team.</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Return to Homepage</a>
                    </div>
                </div>
                <div style="background: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; color: #999;">
                    <p>EduVerse LMS © 2024. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    return send_email(user_email, subject, body_html)

def send_pending_notification_email(user_email, user_name, institute_name):
    """Send pending approval notification email."""
    subject = "Registration Pending - We'll Notify You Soon"
    body_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ffa500 0%, #ffb700 100%); padding: 30px; border-radius: 8px; color: white; text-align: center;">
                    <h2 style="margin: 0;">⏳ Registration Received</h2>
                </div>
                <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none;">
                    <p>Hi <strong>{user_name}</strong>,</p>
                    <p>Thank you for registering with <strong>{institute_name}</strong> on EduVerse LMS! 🎓</p>
                    <p>Your registration request has been received and is now <strong>pending approval</strong> from the institute administrator.</p>
                    <p>Here's what happens next:</p>
                    <ul style="line-height: 2;">
                        <li>✓ The administrator will review your request</li>
                        <li>✓ You'll receive an email notification once approved or if more information is needed</li>
                        <li>✓ Once approved, you can log in and access all courses</li>
                    </ul>
                    <p style="background: #e8f4f8; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                        <strong>Typical approval time:</strong> 24-48 hours
                    </p>
                    <p style="color: #666; font-size: 13px;">If you don't receive an approval email within 48 hours, please contact the support team.</p>
                </div>
                <div style="background: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; color: #999;">
                    <p>EduVerse LMS © 2024. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    return send_email(user_email, subject, body_html)

# ─────────────────────────────────────────────
# AUTH DECORATORS
# ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') != role:
                flash('Access denied.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'trainer':
        return redirect(url_for('trainer_dashboard'))
    elif role == 'institute':
        return redirect(url_for('institute_dashboard'))
    return redirect(url_for('login'))

# ─────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    # Allow showing only one role card when ?role=student|trainer|institute is provided
    selected_role = request.args.get('role')
    # Fetch stats for landing page
    stats = {}
    try:
        stats['courses'] = query_db("SELECT COUNT(*) as cnt FROM courses WHERE status='published'", one=True)['cnt']
        stats['students'] = query_db("SELECT COUNT(*) as cnt FROM students", one=True)['cnt']
        stats['trainers'] = query_db("SELECT COUNT(*) as cnt FROM trainers", one=True)['cnt']
        stats['institutes'] = query_db("SELECT COUNT(*) as cnt FROM institutes", one=True)['cnt']
    except:
        stats = {'courses': 0, 'students': 0, 'trainers': 0, 'institutes': 0}
    categories = []
    try:
        categories = query_db("SELECT * FROM categories LIMIT 8")
    except:
        pass
    return render_template('index.html', stats=stats, categories=categories, selected_role=selected_role)

# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    # Fetch all institutes for the dropdown
    institutes = []
    try:
        institutes = query_db("SELECT id, institute_name FROM institutes")
    except Exception as e:
        print(f"Error fetching institutes: {e}")

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', '')
        phone = request.form.get('phone', '').strip()

        # Validation
        if not all([full_name, email, password, role]):
            flash('All fields are required.', 'danger')
            return render_template('register.html', institutes=institutes)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', institutes=institutes)

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html', institutes=institutes)

        if role not in ['student', 'trainer', 'institute']:
            flash('Invalid role selected.', 'danger')
            return render_template('register.html', institutes=institutes)

        # Check duplicate email
        existing = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
        if existing:
            flash('Email already registered. Please login.', 'danger')
            return render_template('register.html', institutes=institutes)

        # Hash password and insert user
        hashed = generate_password_hash(password)
        try:
            # Set default values for approval_status and is_active
            approval_status = 'approved'
            is_active = 1
            approval_message = request.form.get('approval_message', '').strip()

            if role in ['student', 'trainer']:
                approval_status = 'pending'
                is_active = 0

            user_id = query_db(
                "INSERT INTO users (full_name, email, password_hash, role, phone, approval_status, approval_message, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (full_name, email, hashed, role, phone, approval_status, approval_message, is_active),
                commit=True
            )

            # Insert into role-specific table
            if role == 'student':
                institute_id = request.form.get('institute_id')
                query_db("INSERT INTO students (user_id, institute_id) VALUES (%s, %s)", (user_id, institute_id), commit=True)
            elif role == 'trainer':
                specialization = request.form.get('specialization', '')
                experience = request.form.get('experience_years', 0)
                institute_id = request.form.get('institute_id')
                query_db(
                    "INSERT INTO trainers (user_id, specialization, experience_years, institute_id) VALUES (%s, %s, %s, %s)",
                    (user_id, specialization, experience, institute_id),
                    commit=True
                )
            elif role == 'institute':
                institute_name = request.form.get('institute_name', full_name)
                address = request.form.get('address', '')
                query_db(
                    "INSERT INTO institutes (user_id, institute_name, address) VALUES (%s, %s, %s)",
                    (user_id, institute_name, address),
                    commit=True
                )

            # Add welcome notification
            query_db(
                "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
                (user_id, f'Welcome to EduVerse LMS, {full_name}! Your account has been created.'),
                commit=True
            )

            # Send email based on role and approval status
            if role in ['student', 'trainer']:
                # Get institute name for pending users
                institute_id = request.form.get('institute_id')
                institute = query_db("SELECT institute_name FROM institutes WHERE id = %s", (institute_id,), one=True)
                institute_name = institute['institute_name'] if institute else 'the Institute'
                
                # Send pending notification email
                send_pending_notification_email(email, full_name, institute_name)
                flash('✅ Registration submitted successfully! Your account is pending approval by the selected institution. A confirmation email has been sent to your email address.', 'success')
            else:
                flash('✅ Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('register.html', institutes=institutes)

    return render_template('register.html', institutes=institutes)

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    # Allow pre-selecting a role via query param: /login?role=student
    selected_role = request.args.get('role')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('login.html', selected_role=selected_role)

        # Check if the user exists
        user = query_db("SELECT * FROM users WHERE email = %s", (email,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            # Check approval status and active state
            if user['approval_status'] == 'pending':
                flash('⏳ Your registration request is pending approval by the selected institution. We will notify you and send a confirmation email once the institute reviews your request. Typical approval time: 24-48 hours.', 'warning')
                return render_template('login.html', selected_role=selected_role)
            elif user['approval_status'] == 'rejected':
                flash('❌ Your registration request has been rejected by the institution. You can try registering with a different institution or contact support for more information.', 'danger')
                return render_template('login.html', selected_role=selected_role)
            elif not user['is_active']:
                flash('Your account is inactive. Please contact support.', 'danger')
                return render_template('login.html', selected_role=selected_role)

            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['role'] = user['role']
            session['email'] = user['email']

            # Get role-specific ID
            if user['role'] == 'student':
                s = query_db("SELECT id FROM students WHERE user_id = %s", (user['id'],), one=True)
                session['role_id'] = s['id'] if s else None
            elif user['role'] == 'trainer':
                t = query_db("SELECT id FROM trainers WHERE user_id = %s", (user['id'],), one=True)
                session['role_id'] = t['id'] if t else None
            elif user['role'] == 'institute':
                i = query_db("SELECT id FROM institutes WHERE user_id = %s", (user['id'],), one=True)
                session['role_id'] = i['id'] if i else None

            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html', selected_role=selected_role)

    return render_template('login.html', selected_role=selected_role)

# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ══════════════════════════════════════════════
#  STUDENT ROUTES
# ══════════════════════════════════════════════

@app.route('/student/dashboard')
@role_required('student')
def student_dashboard():
    student_id = session.get('role_id')
    # Enrolled courses
    enrolled = query_db("""
        SELECT c.*, e.progress_percent, e.status as enroll_status, e.enrolled_at,
               u.full_name as trainer_name, cat.name as category_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN trainers t ON c.trainer_id = t.id
        LEFT JOIN users u ON t.user_id = u.id
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE e.student_id = %s
        ORDER BY e.enrolled_at DESC
        LIMIT 5
    """, (student_id,))

    # Stats
    total_enrolled = query_db("SELECT COUNT(*) as cnt FROM enrollments WHERE student_id = %s", (student_id,), one=True)['cnt']
    completed = query_db("SELECT COUNT(*) as cnt FROM enrollments WHERE student_id = %s AND status='completed'", (student_id,), one=True)['cnt']
    pending_assignments = query_db("""
        SELECT COUNT(*) as cnt FROM assignments a
        JOIN enrollments e ON a.course_id = e.course_id
        WHERE e.student_id = %s
        AND a.id NOT IN (SELECT assignment_id FROM submissions WHERE student_id = %s)
    """, (student_id, student_id), one=True)['cnt']

    # Notifications
    notifications = query_db("""
        SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 5
    """, (session['user_id'],))

    return render_template('student/dashboard.html',
        enrolled=enrolled,
        total_enrolled=total_enrolled,
        completed=completed,
        pending_assignments=pending_assignments,
        notifications=notifications
    )

@app.route('/student/courses')
@role_required('student')
def student_courses():
    category_filter = request.args.get('category', '')
    search = request.args.get('search', '')
    student_id = session.get('role_id')

    sql = """
        SELECT c.*, u.full_name as trainer_name, cat.name as category_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count,
               EXISTS(SELECT 1 FROM enrollments WHERE course_id = c.id AND student_id = %s) as is_enrolled
        FROM courses c
        LEFT JOIN trainers t ON c.trainer_id = t.id
        LEFT JOIN users u ON t.user_id = u.id
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.status = 'published'
    """
    params = [student_id]

    if category_filter:
        sql += " AND cat.name = %s"
        params.append(category_filter)
    if search:
        sql += " AND (c.title LIKE %s OR c.description LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])

    sql += " ORDER BY c.created_at DESC"

    courses = query_db(sql, params)
    categories = query_db("SELECT * FROM categories")
    return render_template('student/courses.html',
        courses=courses, categories=categories,
        category_filter=category_filter, search=search)

@app.route('/student/enroll/<int:course_id>', methods=['POST'])
@role_required('student')
def enroll_course(course_id):
    student_id = session.get('role_id')
    # Check already enrolled
    existing = query_db(
        "SELECT id FROM enrollments WHERE student_id = %s AND course_id = %s",
        (student_id, course_id), one=True
    )
    if existing:
        flash('You are already enrolled in this course.', 'info')
    else:
        query_db(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
            (student_id, course_id), commit=True
        )
        course = query_db("SELECT title FROM courses WHERE id = %s", (course_id,), one=True)
        query_db(
            "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
            (session['user_id'], f'You have successfully enrolled in "{course["title"]}"!'),
            commit=True
        )
        flash('Successfully enrolled in the course!', 'success')
    return redirect(url_for('student_courses'))

@app.route('/student/my-courses')
@role_required('student')
def student_my_courses():
    student_id = session.get('role_id')
    courses = query_db("""
        SELECT c.*, e.progress_percent, e.status as enroll_status, e.enrolled_at,
               u.full_name as trainer_name, cat.name as category_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        LEFT JOIN trainers t ON c.trainer_id = t.id
        LEFT JOIN users u ON t.user_id = u.id
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE e.student_id = %s
        ORDER BY e.enrolled_at DESC
    """, (student_id,))
    return render_template('student/my_courses.html', courses=courses)

@app.route('/student/course/<int:course_id>')
@role_required('student')
def student_view_course(course_id):
    student_id = session.get('role_id')
    # Check enrolled
    enrollment = query_db(
        "SELECT * FROM enrollments WHERE student_id = %s AND course_id = %s",
        (student_id, course_id), one=True
    )
    if not enrollment:
        flash('Please enroll in this course first.', 'warning')
        return redirect(url_for('student_courses'))

    course = query_db("""
        SELECT c.*, u.full_name as trainer_name, cat.name as category_name
        FROM courses c
        LEFT JOIN trainers t ON c.trainer_id = t.id
        LEFT JOIN users u ON t.user_id = u.id
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.id = %s
    """, (course_id,), one=True)

    lessons = query_db("SELECT * FROM lessons WHERE course_id = %s ORDER BY lesson_order", (course_id,))
    assignments = query_db("""
        SELECT a.*, s.marks_obtained, s.status as sub_status
        FROM assignments a
        LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = %s
        WHERE a.course_id = %s
        ORDER BY a.due_date
    """, (student_id, course_id))

    return render_template('student/view_course.html',
        course=course, lessons=lessons, assignments=assignments, enrollment=enrollment)

# ══════════════════════════════════════════════
#  TRAINER ROUTES
# ══════════════════════════════════════════════

@app.route('/trainer/dashboard')
@role_required('trainer')
def trainer_dashboard():
    trainer_id = session.get('role_id')

    courses = query_db("""
        SELECT c.*, cat.name as category_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.trainer_id = %s
        ORDER BY c.created_at DESC
        LIMIT 5
    """, (trainer_id,))

    total_courses = query_db("SELECT COUNT(*) as cnt FROM courses WHERE trainer_id = %s", (trainer_id,), one=True)['cnt']
    total_students = query_db("""
        SELECT COUNT(DISTINCT e.student_id) as cnt
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE c.trainer_id = %s
    """, (trainer_id,), one=True)['cnt']
    pending_grading = query_db("""
        SELECT COUNT(*) as cnt FROM submissions s
        JOIN assignments a ON s.assignment_id = a.id
        JOIN courses c ON a.course_id = c.id
        WHERE c.trainer_id = %s AND s.status = 'pending'
    """, (trainer_id,), one=True)['cnt']

    notifications = query_db(
        "SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",
        (session['user_id'],)
    )

    return render_template('trainer/dashboard.html',
        courses=courses,
        total_courses=total_courses,
        total_students=total_students,
        pending_grading=pending_grading,
        notifications=notifications
    )

@app.route('/trainer/create-course', methods=['GET', 'POST'])
@role_required('trainer')
def trainer_create_course():
    trainer_id = session.get('role_id')
    categories = query_db("SELECT * FROM categories")

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id')
        price = request.form.get('price', 0)
        duration_weeks = request.form.get('duration_weeks', 0)
        level = request.form.get('level', 'beginner')
        max_students = request.form.get('max_students', 100)

        if not title:
            flash('Course title is required.', 'danger')
            return render_template('trainer/create_course.html', categories=categories)

        try:
            course_id = query_db("""
                INSERT INTO courses (title, description, trainer_id, category_id, price, duration_weeks, level, max_students, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'published')
            """, (title, description, trainer_id, category_id, price, duration_weeks, level, max_students), commit=True)

            flash('Course created successfully!', 'success')
            return redirect(url_for('trainer_manage_courses'))
        except Exception as e:
            flash(f'Error creating course: {str(e)}', 'danger')

    return render_template('trainer/create_course.html', categories=categories)

@app.route('/trainer/courses')
@role_required('trainer')
def trainer_manage_courses():
    trainer_id = session.get('role_id')
    courses = query_db("""
        SELECT c.*, cat.name as category_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count,
               (SELECT COUNT(*) FROM lessons WHERE course_id = c.id) as lesson_count
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.trainer_id = %s
        ORDER BY c.created_at DESC
    """, (trainer_id,))
    return render_template('trainer/manage_courses.html', courses=courses)

@app.route('/trainer/course/<int:course_id>/add-lesson', methods=['GET', 'POST'])
@role_required('trainer')
def trainer_add_lesson(course_id):
    trainer_id = session.get('role_id')
    course = query_db("SELECT * FROM courses WHERE id = %s AND trainer_id = %s", (course_id, trainer_id), one=True)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('trainer_manage_courses'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        video_url = request.form.get('video_url', '').strip()
        duration = request.form.get('duration_minutes', 0)
        order = request.form.get('lesson_order', 1)

        query_db("""
            INSERT INTO lessons (course_id, title, content, video_url, duration_minutes, lesson_order)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (course_id, title, content, video_url, duration, order), commit=True)
        flash('Lesson added successfully!', 'success')
        return redirect(url_for('trainer_manage_courses'))

    lessons = query_db("SELECT * FROM lessons WHERE course_id = %s ORDER BY lesson_order", (course_id,))
    return render_template('trainer/add_lesson.html', course=course, lessons=lessons)

@app.route('/trainer/students')
@role_required('trainer')
def trainer_students():
    trainer_id = session.get('role_id')
    students = query_db("""
        SELECT u.full_name, u.email, u.phone, c.title as course_title, 
               e.enrolled_at, e.progress_percent, e.status as enroll_status
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        JOIN students s ON e.student_id = s.id
        JOIN users u ON s.user_id = u.id
        WHERE c.trainer_id = %s
        ORDER BY e.enrolled_at DESC
    """, (trainer_id,))
    return render_template('trainer/students.html', students=students)

@app.route('/trainer/delete-course/<int:course_id>', methods=['POST'])
@role_required('trainer')
def trainer_delete_course(course_id):
    trainer_id = session.get('role_id')
    query_db("DELETE FROM courses WHERE id = %s AND trainer_id = %s", (course_id, trainer_id), commit=True)
    flash('Course deleted successfully.', 'success')
    return redirect(url_for('trainer_manage_courses'))

# ══════════════════════════════════════════════
#  INSTITUTE ROUTES
# ══════════════════════════════════════════════

@app.route('/institute/dashboard')
@role_required('institute')
def institute_dashboard():
    institute_id = session.get('role_id')

    total_trainers = query_db("SELECT COUNT(*) as cnt FROM trainers WHERE institute_id = %s", (institute_id,), one=True)['cnt']
    total_courses = query_db("SELECT COUNT(*) as cnt FROM courses WHERE institute_id = %s", (institute_id,), one=True)['cnt']
    
    # Query count of students belonging to this institute (using students.institute_id)
    total_students = query_db("SELECT COUNT(*) as cnt FROM students WHERE institute_id = %s", (institute_id,), one=True)['cnt']

    recent_trainers = query_db("""
        SELECT u.full_name, u.email, t.specialization, t.experience_years, t.id
        FROM trainers t
        JOIN users u ON t.user_id = u.id
        WHERE t.institute_id = %s
        LIMIT 5
    """, (institute_id,))

    recent_courses = query_db("""
        SELECT c.*, cat.name as category_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.institute_id = %s
        ORDER BY c.created_at DESC
        LIMIT 5
    """, (institute_id,))

    notifications = query_db(
        "SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",
        (session['user_id'],)
    )

    # Fetch pending approvals count
    pending_count = query_db("""
        SELECT COUNT(*) as cnt FROM users u
        LEFT JOIN students s ON u.id = s.user_id
        LEFT JOIN trainers t ON u.id = t.user_id
        WHERE u.approval_status = 'pending' AND (s.institute_id = %s OR t.institute_id = %s)
    """, (institute_id, institute_id), one=True)['cnt']

    return render_template('institute/dashboard.html',
        total_trainers=total_trainers,
        total_courses=total_courses,
        total_students=total_students,
        recent_trainers=recent_trainers,
        recent_courses=recent_courses,
        notifications=notifications,
        pending_count=pending_count
    )

@app.route('/institute/trainers')
@role_required('institute')
def institute_trainers():
    institute_id = session.get('role_id')
    trainers = query_db("""
        SELECT u.full_name, u.email, u.phone, t.specialization, t.experience_years,
               t.qualification, t.id,
               (SELECT COUNT(*) FROM courses WHERE trainer_id = t.id) as course_count
        FROM trainers t
        JOIN users u ON t.user_id = u.id
        WHERE t.institute_id = %s
        ORDER BY u.full_name
    """, (institute_id,))
    return render_template('institute/manage_trainers.html', trainers=trainers)

@app.route('/institute/assign-trainer', methods=['POST'])
@role_required('institute')
def institute_assign_trainer():
    institute_id = session.get('role_id')
    trainer_email = request.form.get('trainer_email', '').strip().lower()

    user = query_db("SELECT id FROM users WHERE email = %s AND role = 'trainer'", (trainer_email,), one=True)
    if not user:
        flash('No trainer found with that email.', 'danger')
        return redirect(url_for('institute_trainers'))

    trainer = query_db("SELECT id FROM trainers WHERE user_id = %s", (user['id'],), one=True)
    if not trainer:
        flash('Trainer profile not found.', 'danger')
        return redirect(url_for('institute_trainers'))

    query_db("UPDATE trainers SET institute_id = %s WHERE id = %s", (institute_id, trainer['id']), commit=True)
    flash('Trainer successfully added to your institute!', 'success')
    return redirect(url_for('institute_trainers'))

@app.route('/institute/courses')
@role_required('institute')
def institute_courses():
    institute_id = session.get('role_id')
    courses = query_db("""
        SELECT c.*, cat.name as category_name, u.full_name as trainer_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as enrolled_count
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        LEFT JOIN trainers t ON c.trainer_id = t.id
        LEFT JOIN users u ON t.user_id = u.id
        WHERE c.institute_id = %s
        ORDER BY c.created_at DESC
    """, (institute_id,))
    return render_template('institute/courses.html', courses=courses)

# ─────────────────────────────────────────────
#  INSTITUTE APPROVALS
# ─────────────────────────────────────────────

@app.route('/institute/approvals')
@role_required('institute')
def institute_approvals():
    institute_id = session.get('role_id')
    
    # Fetch pending student registration requests
    pending_students = query_db("""
        SELECT u.id as user_id, u.full_name, u.email, u.phone, u.approval_message, u.created_at, s.education_level
        FROM users u
        JOIN students s ON u.id = s.user_id
        WHERE u.approval_status = 'pending' AND s.institute_id = %s
        ORDER BY u.created_at DESC
    """, (institute_id,))

    # Fetch pending trainer registration requests
    pending_trainers = query_db("""
        SELECT u.id as user_id, u.full_name, u.email, u.phone, u.approval_message, u.created_at, t.specialization, t.experience_years
        FROM users u
        JOIN trainers t ON u.id = t.user_id
        WHERE u.approval_status = 'pending' AND t.institute_id = %s
        ORDER BY u.created_at DESC
    """, (institute_id,))

    return render_template('institute/approvals.html', 
                           pending_students=pending_students, 
                           pending_trainers=pending_trainers)

@app.route('/institute/approve/<int:user_id>', methods=['POST'])
@role_required('institute')
def institute_approve_user(user_id):
    institute_id = session.get('role_id')
    
    # Verify the user exists and is pending for this institute
    user = query_db("SELECT id, role, full_name, email FROM users WHERE id = %s AND approval_status = 'pending'", (user_id,), one=True)
    if not user:
        flash('Pending user not found.', 'danger')
        return redirect(url_for('institute_approvals'))
        
    # Check if they belong to this institute
    belongs = False
    if user['role'] == 'student':
        check = query_db("SELECT id FROM students WHERE user_id = %s AND institute_id = %s", (user_id, institute_id), one=True)
        if check: belongs = True
    elif user['role'] == 'trainer':
        check = query_db("SELECT id FROM trainers WHERE user_id = %s AND institute_id = %s", (user_id, institute_id), one=True)
        if check: belongs = True
        
    if not belongs:
        flash('Access denied.', 'danger')
        return redirect(url_for('institute_approvals'))
        
    # Update user status
    query_db("UPDATE users SET approval_status = 'approved', is_active = 1 WHERE id = %s", (user_id,), commit=True)
    
    # Get institute name
    institute = query_db("SELECT institute_name FROM institutes WHERE id = %s", (institute_id,), one=True)
    institute_name = institute['institute_name'] if institute else 'the Institute'
    
    # Send approval email
    send_approval_email(user['email'], user['full_name'], institute_name)
    
    # Add notification for the approved user
    query_db("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", 
             (user_id, f"✅ Your registration request has been approved! You can now log in and access all courses."), commit=True)
              
    flash(f"✅ Successfully approved registration for {user['full_name']}. Approval email sent.", 'success')
    return redirect(url_for('institute_approvals'))

@app.route('/institute/reject/<int:user_id>', methods=['POST'])
@role_required('institute')
def institute_reject_user(user_id):
    institute_id = session.get('role_id')
    rejection_reason = request.form.get('rejection_reason', '').strip()
    
    # Verify the user exists and is pending for this institute
    user = query_db("SELECT id, role, full_name, email FROM users WHERE id = %s AND approval_status = 'pending'", (user_id,), one=True)
    if not user:
        flash('Pending user not found.', 'danger')
        return redirect(url_for('institute_approvals'))
        
    # Check if they belong to this institute
    belongs = False
    if user['role'] == 'student':
        check = query_db("SELECT id FROM students WHERE user_id = %s AND institute_id = %s", (user_id, institute_id), one=True)
        if check: belongs = True
    elif user['role'] == 'trainer':
        check = query_db("SELECT id FROM trainers WHERE user_id = %s AND institute_id = %s", (user_id, institute_id), one=True)
        if check: belongs = True
        
    if not belongs:
        flash('Access denied.', 'danger')
        return redirect(url_for('institute_approvals'))
        
    # Update user status to rejected
    query_db("UPDATE users SET approval_status = 'rejected', is_active = 0, approval_message = %s WHERE id = %s", 
             (rejection_reason, user_id), commit=True)
    
    # Get institute name
    institute = query_db("SELECT institute_name FROM institutes WHERE id = %s", (institute_id,), one=True)
    institute_name = institute['institute_name'] if institute else 'the Institute'
    
    # Send rejection email
    send_rejection_email(user['email'], user['full_name'], institute_name, rejection_reason)
    
    # Add notification for the rejected user
    query_db("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", 
             (user_id, f"❌ Your registration request has been reviewed. Unfortunately, it was not approved at this time."), commit=True)
    
    flash(f"❌ Rejected registration request for {user['full_name']}. Rejection email sent.", 'warning')
    return redirect(url_for('institute_approvals'))

# ══════════════════════════════════════════════
#  API ROUTES (for AJAX calls)
# ══════════════════════════════════════════════

@app.route('/api/mark-notification-read/<int:notif_id>', methods=['POST'])
@login_required
def mark_notif_read(notif_id):
    query_db("UPDATE notifications SET is_read = 1 WHERE id = %s AND user_id = %s",
             (notif_id, session['user_id']), commit=True)
    return jsonify({'status': 'ok'})

@app.route('/api/notifications')
@login_required
def get_notifications():
    notifs = query_db("""
        SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 10
    """, (session['user_id'],))
    return jsonify(notifs)

# ─────────────────────────────────────────────
# PROFILE UPDATE
# ─────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = query_db("SELECT * FROM users WHERE id = %s", (session['user_id'],), one=True)
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        query_db("UPDATE users SET full_name = %s, phone = %s WHERE id = %s",
                 (full_name, phone, session['user_id']), commit=True)
        session['user_name'] = full_name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

# ─────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ─────────────────────────────────────────────
# TEMPLATE FILTERS
# ─────────────────────────────────────────────
@app.template_filter('timeago')
def timeago_filter(dt):
    if not dt:
        return ''
    now = datetime.datetime.now()
    diff = now - dt
    if diff.days > 365:
        return f"{diff.days // 365}y ago"
    elif diff.days > 30:
        return f"{diff.days // 30}mo ago"
    elif diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}h ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}m ago"
    else:
        return "just now"

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("   EduVerse LMS Starting...")
    print("   URL: http://localhost:5000")
    print("   DB:  localhost:3306 | lms_db")
    print("=" * 60)
    app.run(debug=True, port=5000)
