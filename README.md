# 🚀 Multi-Purpose Development Agent

A comprehensive web-based agent that empowers you to create websites, develop games, manage SQL databases, and seamlessly link them all together.

## 📋 Features

### 🌐 Website Builder
- **Multiple Templates**: Basic, Blog, E-Commerce, Portfolio, SaaS
- **Auto-generated Code**: HTML, CSS, JavaScript files ready to use
- **Customizable Design**: Modify colors, styles, and layouts
- **Page Management**: Add and organize multiple pages

### 🎮 Game Builder
- **Game Types**: Puzzle, Action, Strategy, RPG, Casual
- **Multiple Frameworks**: 
  - Phaser 3 (JavaScript/HTML5)
  - Babylon.js (3D)
  - Three.js (WebGL)
  - Pygame (Python)
  - Godot (GDScript)
- **Template Generation**: Pre-built game structures with starter code

### 🗄️ Database Manager
- **Multiple Database Support**:
  - SQLite (file-based)
  - MySQL (production)
  - PostgreSQL (production)
- **Table Management**: Create, edit, delete tables
- **Column Management**: Add columns with various data types
- **Data Operations**: View and insert data directly

### 🔗 Project Integration
- **Link Projects to Databases**: Connect any website or game to a database
- **Automatic API Generation**: Get ready-to-use API helper code
- **Multiple Integrations**: Link multiple projects to the same database
- **Deployment**: Generate and deploy complete projects with all integrations

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask + Flask-CORS
- **Database ORM**: SQLAlchemy
- **Database Support**: MySQL, PostgreSQL, SQLite
- **Language**: Python 3.8+

### Frontend
- **Framework**: React 18
- **Styling**: CSS3 with responsive design
- **API Communication**: Fetch API
- **Build Tool**: Create React App

### System Requirements
- **Python**: 3.8+ (download from https://www.python.org/)
- **Node.js**: 14+ LTS (download from https://nodejs.org/)
- **npm**: Comes with Node.js
- **OS**: Windows, macOS, or Linux

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## 🚀 Usage

### Creating a Website

1. Go to the **🌐 Websites** tab
2. Enter your website name and description
3. Select a template (Basic, Blog, E-Commerce, Portfolio, SaaS)
4. Click **✨ Create Website**
5. Your website files are generated and ready to use!

### Creating a Game

1. Go to the **🎮 Games** tab
2. Enter your game name and description
3. Select a game type (Puzzle, Action, Strategy, RPG, Casual)
4. Choose a framework (Phaser, Babylon.js, Three.js, Pygame, Godot)
5. Click **✨ Create Game**
6. Start developing with the generated starter code!

### Setting Up a Database

1. Go to the **🗄️ Databases** tab
2. Click **➕ New Connection**
3. Select your database type (SQLite, MySQL, PostgreSQL)
4. Enter connection details
5. Click **Connect Database**
6. Click **View Tables** to manage your database
7. Create tables with custom columns and data types

### Linking Projects to Databases

1. Go to the **🔗 Integration** tab
2. Select a project (website or game) that isn't yet linked
3. Select a database
4. Optionally customize API endpoints
5. Click **🔗 Link Components**
6. API helper code is automatically generated!
7. Deploy your integrated project with **📦 Deploy**

### Using Generated API Helpers

#### For Websites (JavaScript)
```javascript
// Include in your HTML
<script src="database-api.js"></script>

// Use in your code
const data = await DatabaseAPI.getData('/tables/users');
const result = await DatabaseAPI.postData('/tables/users', { name: 'John' });
```

#### For Games (JavaScript)
```javascript
const gameDB = new GameDatabaseAPI();

// Get high scores
const scores = await gameDB.getHighScores();

// Update high score
await gameDB.updateHighScore('Player1', 1000);
```

#### For Games (Python)
```python
from game_database_api import GameDatabaseAPI

game_db = GameDatabaseAPI()
game_db.update_high_score('Player1', 1000)
scores = game_db.get_high_scores()
```

## 📁 Project Structure

```
Demo/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── database_manager.py       # Database operations
│   ├── website_generator.py      # Website creation logic
│   ├── game_generator.py         # Game creation logic
│   ├── project_integrator.py     # Project linking and integration
│   ├── requirements.txt          # Python dependencies
│   └── projects/                 # Generated projects directory
│       ├── websites/             # Website projects
│       ├── games/                # Game projects
│       ├── deployments/          # Deployed projects
│       └── integrations.json     # Integration configurations
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── App.js                # Main app component
    │   ├── App.css               # Main styles
    │   ├── components/
    │   │   ├── DatabaseManager.js
    │   │   ├── WebsiteBuilder.js
    │   │   ├── GameBuilder.js
    │   │   ├── ProjectIntegration.js
    │   │   └── ProjectList.js
    │   ├── styles/
    │   │   ├── DatabaseManager.css
    │   │   ├── WebsiteBuilder.css
    │   │   ├── GameBuilder.css
    │   │   ├── ProjectIntegration.css
    │   │   └── ProjectList.css
    │   └── index.js
    ├── package.json
    └── README.md
```

## 🔌 API Endpoints

### Databases
- `GET /api/databases` - List all databases
- `POST /api/databases/connect` - Connect to a database
- `GET /api/databases/<id>/tables` - Get tables in database
- `POST /api/databases/<id>/tables/create` - Create a table
- `GET /api/databases/<id>/tables/<name>` - Get table schema
- `POST /api/databases/<id>/tables/<name>/columns/add` - Add column
- `GET /api/databases/<id>/tables/<name>/data` - Get table data
- `POST /api/databases/<id>/tables/<name>/data` - Insert data

### Websites
- `GET /api/websites` - List websites
- `POST /api/websites/create` - Create website
- `POST /api/websites/<id>/pages/add` - Add page to website

### Games
- `GET /api/games` - List games
- `POST /api/games/create` - Create game

### Projects & Integration
- `GET /api/projects` - List all projects
- `POST /api/projects/link` - Link project to database
- `GET /api/projects/<id>/config` - Get project config
- `GET /api/projects/<id>/generate-code` - Generate complete project code
- `POST /api/projects/<id>/deploy` - Deploy project

## 📚 Examples

### Example 1: Create a Blog with Database Integration

1. Create a website using the Blog template
2. Connect to a PostgreSQL database
3. Create a `posts` table with columns: `id`, `title`, `content`, `author`, `created_at`
4. Link the website to the database
5. Use the generated `database-api.js` to fetch and display posts

### Example 2: Build a Highscore Tracking Game

1. Create a game using Phaser framework
2. Connect to SQLite database
3. Create a `scores` table with columns: `id`, `player`, `score`, `timestamp`
4. Link the game to the database
5. Use `GameDatabaseAPI` to save and retrieve high scores
6. Deploy the complete game with database integration

### Example 3: E-Commerce Site with Product Database

1. Create an E-Commerce website
2. Connect to MySQL database
3. Create `products` table with: `id`, `name`, `description`, `price`, `image_url`
4. Create `orders` table with: `id`, `user_id`, `product_id`, `quantity`, `created_at`
5. Link website to database
6. Display products dynamically from the database
7. Handle orders through the integrated API

## 🐛 Troubleshooting

### npm/node Not Found on Windows PowerShell

**Problem**: `npm : The term 'npm' is not recognized...`

**Quick Fix** (temporary - works for current terminal):
```powershell
$env:Path = "C:\Program Files\nodejs;$env:Path"
node --version  # Should work now
npm --version
```

**Permanent Fix** (works for all future terminals):
1. Press **Win + R** and type `sysdm.cpl`
2. Click **"Environment Variables"** button
3. Under "User variables", click **"New"**
4. Variable name: `Path`
5. Variable value: `C:\Program Files\nodejs`
6. Click **OK** on all dialogs
7. **Restart all PowerShell windows**
8. Verify: `npm --version`

### Dependency Version Not Found During `pip install`

**Problem**: 
```
ERROR: Could not find a version that satisfies the requirement Flask==2.3.0
ERROR: No matching distribution found for SQLAlchemy==2.0.0
```

**Cause**: The requirements.txt may specify versions that don't exist or are incompatible.

**Solution**: The project uses tested, stable versions:
- Flask==2.0.3 (not 2.3.0)
- SQLAlchemy==1.4.46 (not 2.0.0)
- PyMySQL==1.0.2 (not 1.1.0)
- Flask-CORS==3.0.10 (not 4.0.0)
- python-dotenv==0.19.0 (not 1.0.0)

If you still get errors, try:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --force-reinstall
```

Or manually install compatible versions:
```bash
pip install Flask==2.0.3 SQLAlchemy==1.4.46 Flask-CORS==3.0.10 PyMySQL==1.0.2 psycopg2-binary==2.9.3 python-dotenv==0.19.0
```

### Database Connection Issues
- Ensure the database server is running
- Check connection credentials
- Verify firewall settings allow the connection
- For MySQL/PostgreSQL, ensure the database exists

### API Errors
- Check browser console for detailed error messages
- Verify backend server is running on port 5000
- Check CORS settings in Flask app
- Ensure database is connected before linking projects

### Port Already in Use
- Backend: Change port in `app.py` (default 5000)
- Frontend: Set `PORT` environment variable (default 3000)

### Python Virtual Environment Issues
- Make sure you're activating the venv in the correct directory
- Try removing the `venv` folder and creating it again
- On PowerShell, use: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 📝 Configuration

### Backend Configuration
Edit `app.py` to modify:
- Flask port and debug mode
- CORS settings
- Project directory paths

### Frontend Configuration
Edit `.env` file (create if doesn't exist):
```
REACT_APP_API_URL=http://localhost:5000
```

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for personal and commercial purposes.

## 🎯 Future Features

- [ ] User authentication and authorization
- [ ] Project templates marketplace
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Mobile app generation
- [ ] AI-powered code suggestions
- [ ] Version control integration
- [ ] Live preview for websites
- [ ] In-browser game testing
- [ ] Automated deployment to cloud platforms

## 💬 Support

For issues, questions, or suggestions:
- Create an issue on the GitHub repository
- Contact: support@multiagent.dev

## 🙏 Acknowledgments

Built with ❤️ using:
- Flask - Web framework
- React - UI framework
- SQLAlchemy - ORM
- Phaser - Game framework

---

**Happy Building! 🚀**
