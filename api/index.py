from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

# Initialize Supabase
try:
    supabase: Client = create_client(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY')
    )
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise

@app.route('/')
def index():
    # Fetch all tasks
    response = supabase.table('tasks').select("*").execute()
    tasks = response.data
    return render_template('tasks.html', tasks=tasks)

@app.route('/task/add', methods=['POST'])
def add_task():
    try:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'due_date': request.form['due_date'],
            'priority': request.form['priority'],
            'created_at': datetime.now().isoformat()
        }
        
        # Validate form data
        if not data['name'] or not data['due_date']:
            flash('Name and due date are required!', 'error')
            return redirect(url_for('index'))
            
        supabase.table('tasks').insert(data).execute()
        flash('Task added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding task: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/task/update/<id>', methods=['POST'])
def update_task(id):
    try:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'due_date': request.form['due_date'],
            'priority': request.form['priority']
        }
        
        # Validate form data
        if not data['name'] or not data['due_date']:
            flash('Name and due date are required!', 'error')
            return redirect(url_for('index'))
            
        supabase.table('tasks').update(data).eq('id', id).execute()
        flash('Task updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating task: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/task/delete/<id>')
def delete_task(id):
    try:
        supabase.table('tasks').delete().eq('id', id).execute()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting task: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 