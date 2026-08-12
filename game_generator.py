"""
Game Generator Module
Handles game creation and code generation
"""

import json
import os
from pathlib import Path
from datetime import datetime
import uuid

class GameGenerator:
    def __init__(self):
        self.projects_dir = Path("projects/games")
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.projects = {}
        self.game_types = self._load_game_types()
        self.frameworks = self._load_frameworks()

    def _load_game_types(self):
        """Load available game types"""
        return {
            'puzzle': {
                'name': 'Puzzle Game',
                'description': 'Logic and problem-solving game',
                'examples': ['Match 3', 'Sudoku', 'Sliding Puzzle']
            },
            'action': {
                'name': 'Action Game',
                'description': 'Fast-paced action gameplay',
                'examples': ['Platformer', 'Shooter', 'Beat Em Up']
            },
            'strategy': {
                'name': 'Strategy Game',
                'description': 'Turn-based or real-time strategy',
                'examples': ['Tower Defense', 'Card Game', 'Turn-Based Strategy']
            },
            'rpg': {
                'name': 'RPG',
                'description': 'Role-Playing Game with progression',
                'examples': ['Text Adventure', 'Dungeon Crawler', 'Fantasy RPG']
            },
            'casual': {
                'name': 'Casual Game',
                'description': 'Casual and fun gameplay',
                'examples': ['Clicker', 'Idle Game', 'Minigame Collection']
            }
        }

    def _load_frameworks(self):
        """Load available game frameworks"""
        return {
            'phaser': {
                'name': 'Phaser 3',
                'type': 'JavaScript',
                'description': 'Popular 2D game framework',
                'website': 'https://phaser.io'
            },
            'babylon': {
                'name': 'Babylon.js',
                'type': 'JavaScript',
                'description': 'Powerful 3D game engine',
                'website': 'https://www.babylonjs.com'
            },
            'threejs': {
                'name': 'Three.js',
                'type': 'JavaScript',
                'description': 'WebGL 3D library',
                'website': 'https://threejs.org'
            },
            'pygame': {
                'name': 'Pygame',
                'type': 'Python',
                'description': 'Python game library',
                'website': 'https://www.pygame.org'
            },
            'godot': {
                'name': 'Godot',
                'type': 'GDScript',
                'description': 'Open-source game engine',
                'website': 'https://godotengine.org'
            }
        }

    def get_game_types(self):
        """Get available game types"""
        return self.game_types

    def get_frameworks(self):
        """Get available frameworks"""
        return self.frameworks

    def create_game(self, name, description, game_type='puzzle', framework='phaser', features=None):
        """Create a new game project"""
        project_id = str(uuid.uuid4())[:8]
        
        if game_type not in self.game_types:
            raise ValueError(f"Unknown game type: {game_type}")
        
        if framework not in self.frameworks:
            raise ValueError(f"Unknown framework: {framework}")
        
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        project_config = {
            'id': project_id,
            'name': name,
            'description': description,
            'game_type': game_type,
            'framework': framework,
            'created_at': datetime.now().isoformat(),
            'features': features or [],
            'files': {}
        }
        
        # Generate game files based on framework
        self._generate_game_files(project_dir, framework, game_type, project_config)
        
        # Save project config
        config_file = project_dir / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        self.projects[project_id] = project_config
        return project_id

    def _generate_game_files(self, project_dir, framework, game_type, config):
        """Generate game files based on framework"""
        
        if framework == 'phaser':
            self._generate_phaser_game(project_dir, game_type, config)
        elif framework == 'babylon':
            self._generate_babylon_game(project_dir, game_type, config)
        elif framework == 'threejs':
            self._generate_threejs_game(project_dir, game_type, config)
        elif framework == 'pygame':
            self._generate_pygame_game(project_dir, game_type, config)
        elif framework == 'godot':
            self._generate_godot_game(project_dir, game_type, config)

    def _generate_phaser_game(self, project_dir, game_type, config):
        """Generate a Phaser game"""
        
        # Create index.html
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['name']}</title>
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #222;
            font-family: Arial, sans-serif;
        }}
        #game {{
            border: 3px solid #333;
        }}
        #ui {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            z-index: 100;
        }}
    </style>
</head>
<body>
    <div id="ui">
        <h1>{config['name']}</h1>
        <p>{config['description']}</p>
    </div>
    <script src="game.js"></script>
</body>
</html>
"""
        
        # Create game.js
        js_content = f"""// {config['name']} - Phaser Game
// Type: {config['game_type']}

const config = {{
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {{
        default: 'arcade',
        arcade: {{
            gravity: {{ y: 300 }},
            debug: false
        }}
    }},
    scene: {{
        preload: preload,
        create: create,
        update: update
    }}
}};

const game = new Phaser.Game(config);

function preload() {{
    // Load game assets here
}}

function create() {{
    // Create game objects here
    const centerX = this.cameras.main.centerX;
    const centerY = this.cameras.main.centerY;
    
    // Create a background
    this.add.rectangle(400, 300, 800, 600, 0x1a1a1a);
    
    // Create title text
    this.add.text(centerX, 50, '{config['name']}', {{
        font: 'bold 32px Arial',
        fill: '#ffffff',
        align: 'center'
    }}).setOrigin(0.5);
    
    // Create player sprite placeholder
    const player = this.add.circle(centerX, centerY, 15, 0x00ff00);
    player.setBounce(0.2);
    player.setCollideWorldBounds(true);
    
    // Add physics to player
    this.physics.add.existing(player);
    
    // Create game instructions
    this.add.text(centerX, 500, 'Game Type: {config['game_type'].upper()}', {{
        font: '16px Arial',
        fill: '#ffffff',
        align: 'center'
    }}).setOrigin(0.5);
}}

function update() {{
    // Update game logic here
    // Handle input, check collisions, update game state
}}
"""
        
        # Create style.css
        css_content = """/* Game Styles */

body {
    font-family: Arial, sans-serif;
    background: #222;
    margin: 0;
    padding: 0;
}

canvas {
    border: 3px solid #333;
    display: block;
}

#ui {
    position: fixed;
    top: 20px;
    left: 20px;
    color: white;
    z-index: 1000;
}

#ui h1 {
    margin: 0;
    font-size: 24px;
}

#ui p {
    margin: 5px 0 0 0;
    color: #aaa;
}
"""
        
        # Create package.json
        package_json = {
            "name": config['name'].lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": config['description'],
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "dev": "python -m http.server 8000"
            },
            "dependencies": {
                "phaser": "^3.55.2"
            },
            "license": "MIT"
        }
        
        # Write files
        with open(project_dir / 'index.html', 'w') as f:
            f.write(html_content)
        
        with open(project_dir / 'game.js', 'w') as f:
            f.write(js_content)
        
        with open(project_dir / 'style.css', 'w') as f:
            f.write(css_content)
        
        with open(project_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

    def _generate_babylon_game(self, project_dir, game_type, config):
        """Generate a Babylon.js game"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config['name']}</title>
    <style>
        html, body {{
            overflow: hidden;
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        #renderCanvas {{
            width: 100%;
            height: 100%;
            touch-action: none;
        }}
    </style>
    <script src="https://www.babylonjs-playground.com/babylon.js"></script>
</head>
<body>
    <canvas id="renderCanvas"></canvas>
    <script src="game.js"></script>
</body>
</html>
"""
        
        js_content = f"""// {config['name']} - Babylon.js Game
const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true);

const scene = new BABYLON.Scene(engine);
scene.clearColor = new BABYLON.Color3(0, 0, 0);

// Create camera
const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(0, 0, -30));
camera.attachControl(canvas, true);

// Create light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0));
light.intensity = 0.7;

// Create a simple sphere
const sphere = BABYLON.MeshBuilder.CreateSphere("sphere", {{ diameter: 2 }}, scene);
sphere.position.y = 0;

// Render loop
engine.runRenderLoop(() => {{
    scene.render();
}});

// Handle window resize
window.addEventListener("resize", () => {{
    engine.resize();
}});
"""
        
        with open(project_dir / 'index.html', 'w') as f:
            f.write(html_content)
        
        with open(project_dir / 'game.js', 'w') as f:
            f.write(js_content)

    def _generate_threejs_game(self, project_dir, game_type, config):
        """Generate a Three.js game"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config['name']}</title>
    <style>
        body {{
            margin: 0;
            overflow: hidden;
        }}
        canvas {{
            display: block;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <script src="game.js"></script>
</body>
</html>
"""
        
        js_content = f"""// {config['name']} - Three.js Game

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create a box
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({{ color: 0x00ff00 }});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

// Animation loop
function animate() {{
    requestAnimationFrame(animate);
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera);
}}

animate();

// Handle window resize
window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}});
"""
        
        with open(project_dir / 'index.html', 'w') as f:
            f.write(html_content)
        
        with open(project_dir / 'game.js', 'w') as f:
            f.write(js_content)

    def _generate_pygame_game(self, project_dir, game_type, config):
        """Generate a Pygame game"""
        py_content = f"""#!/usr/bin/env python3
# {config['name']} - Pygame
# Type: {config['game_type']}

import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('{config['name']}')
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.running = True
        self.score = 0
        self.level = 1
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event.key)
    
    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
    
    def update(self):
        # Update game logic here
        pass
    
    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title_text = font.render('{config['name']}', True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        # Draw game info
        info_font = pygame.font.Font(None, 24)
        score_text = info_font.render(f"Score: {{self.score}}", True, WHITE)
        level_text = info_font.render(f"Level: {{self.level}}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
"""
        
        with open(project_dir / 'game.py', 'w') as f:
            f.write(py_content)
        
        # Create requirements.txt
        with open(project_dir / 'requirements.txt', 'w') as f:
            f.write("pygame>=2.0.0\n")

    def _generate_godot_game(self, project_dir, game_type, config):
        """Generate a Godot game project"""
        
        # Create project.godot
        project_godot = """[gd_resource type="Environment" load_steps=2 format=2]

[sub_resource type="ProceduralSky" id=1]
sky_type = 0
sun_angle_min = 1.0
sun_angle_max = 1.0
sun_curve = SubResource( "CurveTexture" )
sky_tone_curve = SubResource( "GradientTexture" )
sky_energy = 1.0
sky_cull_mask = 63

[resource]
ambient_light_enabled = true
ambient_light_source = 2
ambient_light_energy = 1.0
ambient_light_sky_contribution = 1.0
background_mode = 2
background_sky = SubResource( 1 )

[gd_scene load_steps=2 format=2]

[ext_resource type="Script" path="res://main.gd"]

[node name="Main" type="Node"]
script = ExtResource( 1 )
"""
        
        # Create main.gd
        gdscript_content = f"""# {config['name']} - Godot Game
extends Node

func _ready():
    pass # Replace with function body.

func _process(delta):
    pass # Replace with function body.
"""
        
        with open(project_dir / 'project.godot', 'w') as f:
            f.write(project_godot)
        
        with open(project_dir / 'main.gd', 'w') as f:
            f.write(gdscript_content)

    def list_games(self):
        """List all created games"""
        games = []
        for project_dir in self.projects_dir.glob('*/'):
            config_file = project_dir / 'config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                games.append(config)
        
        return games
