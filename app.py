"""
Multi-Purpose Development Agent - Backend
Handles website creation, game generation, database management, and integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, inspect
import json
import os
from pathlib import Path
import subprocess
import sys

from database_manager import DatabaseManager
from website_generator import WebsiteGenerator
from game_generator import GameGenerator
from project_integrator import ProjectIntegrator

app = Flask(__name__)
CORS(app)

# Initialize managers
db_manager = DatabaseManager()
website_gen = WebsiteGenerator()
game_gen = GameGenerator()
integrator = ProjectIntegrator()

# Configuration
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

# ============= DATABASE ENDPOINTS =============

@app.route('/api/databases', methods=['GET'])
def get_databases():
    """Get list of all configured databases"""
    return jsonify(db_manager.get_all_databases())

@app.route('/api/databases/connect', methods=['POST'])
def connect_database():
    """Connect to a database"""
    data = request.json
    try:
        result = db_manager.connect_database(
            db_type=data['db_type'],
            host=data.get('host'),
            port=data.get('port'),
            username=data.get('username'),
            password=data.get('password'),
            database=data.get('database'),
            file_path=data.get('file_path')  # For SQLite
        )
        return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/databases/<db_id>/tables', methods=['GET'])
def get_tables(db_id):
    """Get all tables in a database"""
    try:
        tables = db_manager.get_tables(db_id)
        return jsonify({'success': True, 'tables': tables})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/databases/<db_id>/tables/create', methods=['POST'])
def create_table(db_id):
    """Create a new table"""
    data = request.json
    try:
        result = db_manager.create_table(db_id, data)
        return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/databases/<db_id>/tables/<table_name>', methods=['GET', 'DELETE'])
def manage_table(db_id, table_name):
    """Get table schema or delete table"""
    try:
        if request.method == 'GET':
            schema = db_manager.get_table_schema(db_id, table_name)
            return jsonify({'success': True, 'schema': schema})
        else:  # DELETE
            result = db_manager.delete_table(db_id, table_name)
            return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/databases/<db_id>/tables/<table_name>/columns/add', methods=['POST'])
def add_column(db_id, table_name):
    """Add a column to a table"""
    data = request.json
    try:
        result = db_manager.add_column(db_id, table_name, data)
        return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/databases/<db_id>/tables/<table_name>/data', methods=['GET', 'POST'])
def manage_table_data(db_id, table_name):
    """Get or insert data in a table"""
    try:
        if request.method == 'GET':
            data = db_manager.get_table_data(db_id, table_name)
            return jsonify({'success': True, 'data': data})
        else:  # POST
            result = db_manager.insert_data(db_id, table_name, request.json)
            return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= WEBSITE ENDPOINTS =============

@app.route('/api/websites', methods=['GET'])
def list_websites():
    """List all created websites"""
    websites = website_gen.list_websites()
    return jsonify({'success': True, 'websites': websites})

@app.route('/api/websites/create', methods=['POST'])
def create_website():
    """Create a new website"""
    data = request.json
    try:
        project_id = website_gen.create_website(
            name=data['name'],
            description=data.get('description'),
            template=data.get('template', 'basic'),
            pages=data.get('pages', []),
            style=data.get('style', {})
        )
        return jsonify({'success': True, 'project_id': project_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/websites/<project_id>/pages/add', methods=['POST'])
def add_website_page(project_id):
    """Add a page to a website"""
    data = request.json
    try:
        result = website_gen.add_page(project_id, data)
        return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= GAME ENDPOINTS =============

@app.route('/api/games', methods=['GET'])
def list_games():
    """List all created games"""
    games = game_gen.list_games()
    return jsonify({'success': True, 'games': games})

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Create a new game"""
    data = request.json
    try:
        project_id = game_gen.create_game(
            name=data['name'],
            description=data.get('description'),
            game_type=data.get('game_type', 'puzzle'),
            framework=data.get('framework', 'phaser'),
            features=data.get('features', [])
        )
        return jsonify({'success': True, 'project_id': project_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= INTEGRATION ENDPOINTS =============

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects (websites, games, databases)"""
    projects = integrator.get_all_projects()
    return jsonify({'success': True, 'projects': projects})

@app.route('/api/projects/link', methods=['POST'])
def link_components():
    """Link a website/game to a database"""
    data = request.json
    try:
        result = integrator.link_project_to_database(
            project_id=data['project_id'],
            project_type=data['project_type'],  # 'website' or 'game'
            database_id=data['database_id'],
            endpoints=data.get('endpoints', {})
        )
        return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/projects/<project_id>/config', methods=['GET', 'POST'])
def manage_project_config(project_id):
    """Get or update project configuration"""
    try:
        if request.method == 'GET':
            config = integrator.get_project_config(project_id)
            return jsonify({'success': True, 'config': config})
        else:  # POST
            result = integrator.update_project_config(project_id, request.json)
            return jsonify({'success': True, 'message': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/projects/<project_id>/generate-code', methods=['GET'])
def generate_project_code(project_id):
    """Generate complete project code (website/game with database integration)"""
    try:
        code = integrator.generate_complete_project(project_id)
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/projects/<project_id>/deploy', methods=['POST'])
def deploy_project(project_id):
    """Deploy project (generate files and optionally start server)"""
    try:
        result = integrator.deploy_project(project_id)
        return jsonify({'success': True, 'message': result, 'location': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= UTILITY ENDPOINTS =============

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available templates for websites and games"""
    return jsonify({
        'website_templates': website_gen.get_templates(),
        'game_types': game_gen.get_game_types(),
        'frameworks': game_gen.get_frameworks()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
