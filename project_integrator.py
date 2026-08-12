"""
Project Integrator Module
Links websites and games to databases and handles overall project management
"""

import json
import os
from pathlib import Path
from datetime import datetime
import shutil

class ProjectIntegrator:
    def __init__(self):
        self.projects_dir = Path("projects")
        self.projects_dir.mkdir(exist_ok=True)
        self.integrations_file = self.projects_dir / 'integrations.json'
        self._load_integrations()

    def _load_integrations(self):
        """Load existing integrations"""
        if self.integrations_file.exists():
            with open(self.integrations_file, 'r') as f:
                self.integrations = json.load(f)
        else:
            self.integrations = {}

    def _save_integrations(self):
        """Save integrations to file"""
        with open(self.integrations_file, 'w') as f:
            json.dump(self.integrations, f, indent=2)

    def get_all_projects(self):
        """Get all projects (websites and games)"""
        projects = []
        
        # Get websites
        websites_dir = self.projects_dir / 'websites'
        if websites_dir.exists():
            for project_dir in websites_dir.glob('*/'):
                config_file = project_dir / 'config.json'
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    config['type'] = 'website'
                    config['linked_database'] = self.integrations.get(config['id'], {}).get('database_id')
                    projects.append(config)
        
        # Get games
        games_dir = self.projects_dir / 'games'
        if games_dir.exists():
            for project_dir in games_dir.glob('*/'):
                config_file = project_dir / 'config.json'
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    config['type'] = 'game'
                    config['linked_database'] = self.integrations.get(config['id'], {}).get('database_id')
                    projects.append(config)
        
        return projects

    def link_project_to_database(self, project_id, project_type, database_id, endpoints=None):
        """
        Link a website or game to a database
        endpoints: {
            'api_base': '/api',
            'get_endpoint': '/api/data',
            'post_endpoint': '/api/data'
        }
        """
        integration_config = {
            'project_id': project_id,
            'project_type': project_type,
            'database_id': database_id,
            'endpoints': endpoints or {},
            'linked_at': datetime.now().isoformat()
        }
        
        self.integrations[project_id] = integration_config
        self._save_integrations()
        
        # Update project config with database info
        self._update_project_with_db_config(project_id, project_type, database_id, endpoints)
        
        return f"Successfully linked {project_type} '{project_id}' to database '{database_id}'"

    def _update_project_with_db_config(self, project_id, project_type, database_id, endpoints):
        """Update project configuration with database integration details"""
        
        if project_type == 'website':
            project_dir = self.projects_dir / 'websites' / project_id
        else:  # game
            project_dir = self.projects_dir / 'games' / project_id
        
        config_file = project_dir / 'config.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            config['database'] = {
                'id': database_id,
                'endpoints': endpoints or {}
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Create/update API helper file
        if project_type == 'website':
            self._create_website_api_helper(project_dir, database_id, endpoints)
        elif project_type == 'game':
            self._create_game_api_helper(project_dir, database_id, endpoints)

    def _create_website_api_helper(self, project_dir, database_id, endpoints):
        """Create API helper JavaScript file for website"""
        api_base = endpoints.get('api_base', '/api') if endpoints else '/api'
        
        api_code = f"""// Database Integration Helper
// Database ID: {database_id}

const DATABASE_API = '{api_base}';

class DatabaseAPI {{
    static async query(endpoint, method = 'GET', data = null) {{
        try {{
            const options = {{
                method: method,
                headers: {{'Content-Type': 'application/json'}}
            }};
            
            if (data && method !== 'GET') {{
                options.body = JSON.stringify(data);
            }}
            
            const response = await fetch(DATABASE_API + endpoint, options);
            
            if (!response.ok) {{
                throw new Error(`HTTP error! status: ${{response.status}}`);
            }}
            
            return await response.json();
        }} catch (error) {{
            console.error('Database API Error:', error);
            return null;
        }}
    }}
    
    static async getData(endpoint) {{
        return this.query(endpoint, 'GET');
    }}
    
    static async postData(endpoint, data) {{
        return this.query(endpoint, 'POST', data);
    }}
    
    static async updateData(endpoint, data) {{
        return this.query(endpoint, 'PUT', data);
    }}
    
    static async deleteData(endpoint) {{
        return this.query(endpoint, 'DELETE');
    }}
}}

// Example usage:
// const data = await DatabaseAPI.getData('/tables/users');
// const result = await DatabaseAPI.postData('/tables/users', {{ name: 'John' }});
"""
        
        with open(project_dir / 'database-api.js', 'w') as f:
            f.write(api_code)

    def _create_game_api_helper(self, project_dir, database_id, endpoints):
        """Create API helper for game (Python or JavaScript)"""
        
        # Check what type of game (Pygame = Python, others = JavaScript)
        config_file = project_dir / 'config.json'
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        framework = config.get('framework', 'phaser')
        
        if framework == 'pygame':
            self._create_python_api_helper(project_dir, database_id, endpoints)
        else:
            self._create_javascript_api_helper(project_dir, database_id, endpoints)

    def _create_javascript_api_helper(self, project_dir, database_id, endpoints):
        """Create API helper for JavaScript-based games"""
        api_base = endpoints.get('api_base', 'http://localhost:5000/api') if endpoints else 'http://localhost:5000/api'
        
        api_code = f"""// Game Database Integration
// Database ID: {database_id}

class GameDatabaseAPI {{
    constructor(baseURL = '{api_base}') {{
        this.baseURL = baseURL;
    }}
    
    async request(endpoint, method = 'GET', data = null) {{
        try {{
            const options = {{
                method: method,
                headers: {{'Content-Type': 'application/json'}}
            }};
            
            if (data && method !== 'GET') {{
                options.body = JSON.stringify(data);
            }}
            
            const response = await fetch(this.baseURL + endpoint, options);
            
            if (!response.ok) {{
                throw new Error(`API error: ${{response.status}}`);
            }}
            
            return await response.json();
        }} catch (error) {{
            console.error('Game API Error:', error);
            throw error;
        }}
    }}
    
    async getTableData(tableName) {{
        return this.request(`/databases/{database_id}/tables/${{tableName}}/data`);
    }}
    
    async insertData(tableName, data) {{
        return this.request(`/databases/{database_id}/tables/${{tableName}}/data`, 'POST', data);
    }}
    
    async updateHighScore(playerName, score) {{
        return this.request('/databases/{database_id}/tables/scores/data', 'POST', {{
            player: playerName,
            score: score,
            timestamp: new Date().toISOString()
        }});
    }}
    
    async getHighScores(limit = 10) {{
        return this.request(`/databases/{database_id}/tables/scores/data?limit=${{limit}}`);
    }}
}}

// Usage in game:
// const gameDB = new GameDatabaseAPI();
// gameDB.updateHighScore('Player1', 1000);
"""
        
        with open(project_dir / 'game-database-api.js', 'w') as f:
            f.write(api_code)

    def _create_python_api_helper(self, project_dir, database_id, endpoints):
        """Create API helper for Python-based games"""
        api_base = endpoints.get('api_base', 'http://localhost:5000/api') if endpoints else 'http://localhost:5000/api'
        
        py_code = f"""# Game Database Integration
# Database ID: {database_id}

import requests
import json
from typing import Dict, Any, List

class GameDatabaseAPI:
    def __init__(self, base_url='{api_base}'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({{'Content-Type': 'application/json'}})
    
    def _request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict:
        try:
            url = self.base_url + endpoint
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Game API Error: {{e}}')
            return None
    
    def get_table_data(self, table_name: str) -> List[Dict]:
        return self._request('GET', f'/databases/{database_id}/tables/{{table_name}}/data')
    
    def insert_data(self, table_name: str, data: Dict) -> Dict:
        return self._request('POST', f'/databases/{database_id}/tables/{{table_name}}/data', data)
    
    def update_high_score(self, player_name: str, score: int) -> Dict:
        data = {{
            'player': player_name,
            'score': score,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }}
        return self.insert_data('scores', data)
    
    def get_high_scores(self, limit: int = 10) -> List[Dict]:
        return self.get_table_data('scores')

# Usage:
# game_db = GameDatabaseAPI()
# game_db.update_high_score('Player1', 1000)
# scores = game_db.get_high_scores()
"""
        
        with open(project_dir / 'game_database_api.py', 'w') as f:
            f.write(py_code)

    def get_project_config(self, project_id):
        """Get complete project configuration"""
        # Try to find project in websites or games
        websites_dir = self.projects_dir / 'websites' / project_id
        games_dir = self.projects_dir / 'games' / project_id
        
        config_file = None
        if websites_dir.exists():
            config_file = websites_dir / 'config.json'
        elif games_dir.exists():
            config_file = games_dir / 'config.json'
        
        if config_file and config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Add integration info
            if project_id in self.integrations:
                config['integration'] = self.integrations[project_id]
            
            return config
        
        raise ValueError(f"Project {project_id} not found")

    def update_project_config(self, project_id, updates):
        """Update project configuration"""
        config = self.get_project_config(project_id)
        
        # Merge updates
        config.update(updates)
        
        # Find and update config file
        websites_dir = self.projects_dir / 'websites' / project_id
        games_dir = self.projects_dir / 'games' / project_id
        
        config_file = None
        if websites_dir.exists():
            config_file = websites_dir / 'config.json'
        elif games_dir.exists():
            config_file = games_dir / 'config.json'
        
        if config_file:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return "Project configuration updated successfully"
        
        raise ValueError(f"Project {project_id} not found")

    def generate_complete_project(self, project_id):
        """Generate complete project code with all integrations"""
        config = self.get_project_config(project_id)
        project_type = config.get('type', 'unknown')
        
        if project_type == 'website':
            return self._generate_website_complete(project_id, config)
        elif project_type == 'game':
            return self._generate_game_complete(project_id, config)
        
        raise ValueError(f"Unknown project type: {project_type}")

    def _generate_website_complete(self, project_id, config):
        """Generate complete website code"""
        project_dir = self.projects_dir / 'websites' / project_id
        
        files = {}
        for file_path in project_dir.glob('*'):
            if file_path.is_file() and file_path.suffix in ['.html', '.css', '.js', '.json']:
                with open(file_path, 'r') as f:
                    files[file_path.name] = f.read()
        
        return {
            'project_id': project_id,
            'name': config['name'],
            'type': 'website',
            'files': files,
            'database_integration': config.get('database', {})
        }

    def _generate_game_complete(self, project_id, config):
        """Generate complete game code"""
        project_dir = self.projects_dir / 'games' / project_id
        
        files = {}
        framework = config.get('framework')
        
        if framework == 'pygame':
            extensions = ['.py', '.txt', '.json']
        else:
            extensions = ['.html', '.js', '.json', '.css']
        
        for file_path in project_dir.glob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                with open(file_path, 'r') as f:
                    files[file_path.name] = f.read()
        
        return {
            'project_id': project_id,
            'name': config['name'],
            'type': 'game',
            'framework': framework,
            'files': files,
            'database_integration': config.get('database', {})
        }

    def deploy_project(self, project_id):
        """Deploy project (create deployment directory)"""
        config = self.get_project_config(project_id)
        project_type = config.get('type', 'unknown')
        
        # Create deployment directory
        deploy_dir = self.projects_dir / 'deployments' / project_id
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all project files
        if project_type == 'website':
            src_dir = self.projects_dir / 'websites' / project_id
        elif project_type == 'game':
            src_dir = self.projects_dir / 'games' / project_id
        else:
            raise ValueError(f"Unknown project type: {project_type}")
        
        # Copy files
        for file_path in src_dir.glob('*'):
            if file_path.is_file():
                shutil.copy2(file_path, deploy_dir / file_path.name)
        
        # Create deployment info
        deployment_info = {
            'project_id': project_id,
            'project_name': config['name'],
            'project_type': project_type,
            'deployed_at': datetime.now().isoformat(),
            'deployment_path': str(deploy_dir),
            'database_integration': config.get('database', {}),
            'status': 'deployed'
        }
        
        info_file = deploy_dir / 'deployment-info.json'
        with open(info_file, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        return str(deploy_dir)
