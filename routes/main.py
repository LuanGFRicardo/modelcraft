from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# Criar um Blueprint com o nome 'main'
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return redirect(url_for('auth.login'))

@bp.route('/home')
@login_required
def home():
    return render_template('home.html')
