from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Group, GroupMember, Message
from datetime import datetime

main = Blueprint('main', __name__)

# ====================== HOME ======================
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

# ====================== AUTH ======================
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('main.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please provide email and password', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


# ====================== DASHBOARD ======================
@main.route('/dashboard')
@login_required
def dashboard():
    user_groups = Group.query.join(GroupMember)\
                    .filter(GroupMember.user_id == current_user.id).all()
    
    created_groups = Group.query.filter_by(creator_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                           user_groups=user_groups, 
                           created_groups=created_groups)


# ====================== GROUPS ======================
@main.route('/groups', methods=['GET'])
@login_required
def groups():
    search = request.args.get('search', '').strip()
    subject = request.args.get('subject', '').strip()
    
    query = Group.query
    
    if search:
        query = query.filter(
            (Group.name.ilike(f'%{search}%')) | 
            (Group.description.ilike(f'%{search}%'))
        )
    if subject:
        query = query.filter_by(subject=subject)
    
    all_groups = query.order_by(Group.created_at.desc()).all()
    
    # Get unique subjects for filter dropdown
    subjects = [s[0] for s in db.session.query(Group.subject).distinct().all()]
    
    return render_template('groups.html', 
                           groups=all_groups, 
                           subjects=subjects, 
                           search=search)


# ====================== CREATE GROUP ======================
@main.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        subject = request.form.get('subject')
        max_members = int(request.form.get('max_members', 10))

        if not name or not description or not subject:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.create_group'))

        group = Group(
            name=name,
            description=description,
            subject=subject,
            max_members=max_members,
            creator_id=current_user.id
        )
        
        db.session.add(group)
        db.session.commit()

        # Auto join the creator
        membership = GroupMember(group_id=group.id, user_id=current_user.id)
        db.session.add(membership)
        db.session.commit()

        flash('Study group created successfully!', 'success')
        return redirect(url_for('main.group_detail', group_id=group.id))
    
    return render_template('create_group.html')


# ====================== GROUP DETAIL ======================
@main.route('/group/<int:group_id>')
@login_required
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    
    is_member = GroupMember.query.filter_by(
        group_id=group_id, 
        user_id=current_user.id
    ).first() is not None

    messages = Message.query.filter_by(group_id=group_id)\
                       .order_by(Message.timestamp.asc())\
                       .options(db.joinedload(Message.sender))\
                       .all()
    

    
    return render_template('group_detail.html', 
                           group=group, 
                           is_member=is_member, 
                           messages=messages)


# ====================== JOIN / LEAVE ======================
@main.route('/join_group/<int:group_id>')
@login_required
def join_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    if GroupMember.query.filter_by(group_id=group_id, user_id=current_user.id).first():
        flash('You are already a member of this group.', 'info')
        return redirect(url_for('main.group_detail', group_id=group_id))

    current_count = GroupMember.query.filter_by(group_id=group_id).count()
    if current_count >= group.max_members:
        flash('Sorry, this group has reached maximum capacity!', 'danger')
        return redirect(url_for('main.group_detail', group_id=group_id))

    membership = GroupMember(group_id=group_id, user_id=current_user.id)
    db.session.add(membership)
    db.session.commit()
    
    flash(f'Welcome to {group.name}!', 'success')
    return redirect(url_for('main.group_detail', group_id=group_id))


@main.route('/leave_group/<int:group_id>')
@login_required
def leave_group(group_id):
    membership = GroupMember.query.filter_by(
        group_id=group_id, 
        user_id=current_user.id
    ).first()
    
    if membership:
        db.session.delete(membership)
        db.session.commit()
        flash('You have left the group.', 'info')
    else:
        flash('You are not a member of this group.', 'warning')
    
    return redirect(url_for('main.dashboard'))


# ====================== SEND MESSAGE ======================
@main.route('/send_message/<int:group_id>', methods=['POST'])
@login_required
def send_message(group_id):
    group = Group.query.get_or_404(group_id)
    
    if not GroupMember.query.filter_by(group_id=group_id, user_id=current_user.id).first():
        flash('You must be a member to send messages.', 'danger')
        return redirect(url_for('main.group_detail', group_id=group_id))

    content = request.form.get('content', '').strip()
    if content:
        message = Message(
            group_id=group_id,
            sender_id=current_user.id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
    
    return redirect(url_for('main.group_detail', group_id=group_id))