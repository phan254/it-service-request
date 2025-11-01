import json
import os
import requests
from flask import Flask, render_template, redirect, url_for, flash, request as frequest, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from config import Config
from models import db, Request
from forms import RequestForm, LoginForm

# --------------------------------------------------
# Initialize Flask App
# --------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# --------------------------------------------------
# Flask-Login Setup
# --------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# --------------------------------------------------
# Admin User
# --------------------------------------------------
class AdminUser(UserMixin):
    id = 1
    username = app.config['ADMIN_USERNAME']


@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:
        return AdminUser()
    return None


# --------------------------------------------------
# Load Departments from JSON or API
# --------------------------------------------------
def get_departments():
    """
    Returns a list of departments from an external URL or from local departments.json.
    Falls back to default list if unavailable.
    """
    url = app.config.get('DEPARTMENTS_URL', '').strip()

    # 1️⃣ Try fetching from API if configured
    if url:
        try:
            resp = requests.get(url, timeout=4)
            if resp.ok:
                data = resp.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'departments' in data:
                    return data['departments']
        except Exception as e:
            print(f"⚠️ Failed to fetch departments from URL: {e}")

    # 2️⃣ Fallback to local departments.json
    local_file = os.path.join(os.path.dirname(__file__), 'departments.json')
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"⚠️ Could not load departments.json: {e}")

    # 3️⃣ Default fallback
    return ["IT", "Human Resources", "Finance"]


# --------------------------------------------------
# Public: Submit Request
# --------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    """Main IT Service Request form."""
    form = RequestForm()

    # Always reload departments each time the form loads
    departments = get_departments()
    form.department.choices = [(d, d) for d in departments]

    if form.validate_on_submit():
        new_request = Request(
            requester_name=form.requester_name.data,
            department=form.department.data,
            category=form.category.data,
            description=form.description.data,
            status='Pending'
        )
        db.session.add(new_request)
        db.session.commit()
        flash('✅ Request submitted successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


# --------------------------------------------------
# Admin Login
# --------------------------------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.username.data == app.config['ADMIN_USERNAME'] and
                form.password.data == app.config['ADMIN_PASSWORD']):
            login_user(AdminUser())
            flash('Logged in as admin.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


# --------------------------------------------------
# Admin Logout
# --------------------------------------------------
@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --------------------------------------------------
# Admin Dashboard
# --------------------------------------------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_requests = Request.query.count()
    pending_requests = Request.query.filter_by(status='Pending').count()
    resolved_requests = Request.query.filter_by(status='Resolved').count()
    return render_template(
        'dashboard.html',
        total_requests=total_requests,
        pending_requests=pending_requests,
        resolved_requests=resolved_requests
    )


# --------------------------------------------------
# Admin Requests List
# --------------------------------------------------
@app.route('/admin/requests')
@login_required
def admin_requests():
    status = frequest.args.get('status')
    q = Request.query.order_by(Request.created_at.desc())
    if status:
        q = q.filter_by(status=status)
    requests_list = q.all()
    return render_template('admin_requests.html', requests=requests_list)


# --------------------------------------------------
# View / Update Individual Request
# --------------------------------------------------
@app.route('/admin/requests/<int:request_id>', methods=['GET', 'POST'])
@login_required
def view_request(request_id):
    r = Request.query.get_or_404(request_id)
    if frequest.method == 'POST':
        action = frequest.form.get('action')
        if action == 'resolve' and r.status != 'Resolved':
            r.mark_resolved()
            db.session.commit()
            flash('Request marked as resolved.', 'success')
        elif action == 'set_pending':
            r.status = 'Pending'
            r.resolved_at = None
            db.session.commit()
            flash('Request set back to pending.', 'info')
        return redirect(url_for('view_request', request_id=request_id))
    return render_template('view_request.html', r=r)


# --------------------------------------------------
# Public API Endpoint
# --------------------------------------------------
@app.route('/api/requests')
def api_list_requests():
    """Return all service requests as JSON."""
    q = Request.query.order_by(Request.created_at.desc()).all()
    out = [
        {
            'id': r.id,
            'requester_name': r.requester_name,
            'department': r.department,
            'category': r.category,
            'description': r.description,
            'status': r.status,
            'created_at': r.created_at.isoformat(),
            'resolved_at': r.resolved_at.isoformat() if r.resolved_at else None
        }
        for r in q
    ]
    return jsonify(out)


# --------------------------------------------------
# Run Application
# --------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
