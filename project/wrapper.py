from functools import wraps

from flask import session, flash, redirect, url_for

def admin_required(func):
    """Decorator to check if the user is an admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user']['user_id'] == 0:
            flash('Please log in before moving on.', 'error')
            return redirect(url_for('main.login'))
        if not session['user']['is_admin']:
            flash('You do not have permission to view admin page.', 'error')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper