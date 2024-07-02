from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app import db, bcrypt
from app.models import User, Competition, Submission
from app.utils import allowed_file, process_file, calculate_score
import os

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if user is None:
            flash('Username not found', 'danger')
        elif not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect password', 'danger')
        else:
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def home():
    competitions = Competition.query.all()
    return render_template('competition.html', competitions=competitions)

@main.route('/competition/<int:competition_id>', methods=['GET', 'POST'])
@login_required
def competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            if os.path.getsize(filepath) > 5 * 1024 * 1024:
                flash('File too large', 'danger')
                os.remove(filepath)
                return redirect(request.url)
            try:
                if process_file(filepath, competition):
                    score = calculate_score(filepath, competition)
                    submission = Submission(user_id=current_user.id, competition_id=competition.id, score=score)
                    db.session.add(submission)
                    db.session.commit()
                    flash('File successfully uploaded and scored', 'success')
                    return redirect(url_for('main.leaderboard', competition_id=competition.id))
                else:
                    flash('Invalid file format or contents', 'danger')
                    os.remove(filepath)
            except ValueError as e:
                flash(str(e), 'danger')
                os.remove(filepath)
    submissions = Submission.query.filter_by(competition_id=competition.id).order_by(Submission.score.desc()).all()
    return render_template('leaderboard.html', submissions=submissions, competition=competition)

@main.route('/leaderboard/<int:competition_id>')
@login_required
def leaderboard(competition_id):
    return redirect(url_for('main.competition', competition_id=competition_id))