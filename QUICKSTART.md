# 🚀 Quick Start Guide

Get up and running with the Multi-Purpose Development Agent in 5 minutes!

## Prerequisites

Make sure you have installed:
- Python 3.8+
- Node.js 14+
- npm

### ⚠️ Important for Windows Users

If you're using **PowerShell** and npm/node commands don't work after installation, run this command first:
```powershell
$env:Path = "C:\Program Files\nodejs;$env:Path"
```

Then verify:
```powershell
node --version
npm --version
```

Both should show version numbers. If they still don't work, see the troubleshooting section below.

## 1️⃣ Start the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The backend will start on `http://localhost:5000`

You should see:
```
 * Running on http://127.0.0.1:5000
```

## 2️⃣ Start the Frontend (In a new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will automatically open at `http://localhost:3000`

## 3️⃣ First Steps in the App

### Step 1: Create Your First Website
1. Click on **🌐 Websites** tab
2. Enter name: "My First Website"
3. Select template: "Basic"
4. Click **✨ Create Website**
5. Your website is created! 🎉

### Step 2: Set Up a Database
1. Click on **🗄️ Databases** tab
2. Click **➕ New Connection**
3. Keep "SQLite" selected
4. File path: `./demo.db`
5. Click **Connect Database**
6. Your database is connected! 💾

### Step 3: Create a Table
1. Click **View Tables** on your database
2. Click **➕ Create Table**
3. Table Name: `users`
4. Columns:
   - `id` (INTEGER, Primary Key)
   - `name` (VARCHAR(255))
   - `email` (VARCHAR(255))
5. Click **Create Table** ✨

### Step 4: Link Website to Database
1. Click on **🔗 Integration** tab
2. Select Project: Your "My First Website"
3. Select Database: Your SQLite database
4. Click **🔗 Link Components**
5. Integration complete! 🔗

### Step 5: Deploy
1. Still in Integration tab
2. Find your linked project in "Active Integrations"
3. Click **📦 Deploy**
4. Your project is deployed! 📤

## 📚 What Happened?

You just:
1. ✅ Created a website with template code
2. ✅ Set up a database
3. ✅ Created a table for data storage
4. ✅ Linked the website to the database
5. ✅ Generated API helper code
6. ✅ Deployed everything

All the generated files are in the `backend/projects/` directory!

## 🎮 Try Creating a Game

Repeat the process but with a game:
1. Click **🎮 Games** tab
2. Name: "My First Game"
3. Select type: "Puzzle"
4. Select framework: "Phaser"
5. Create and integrate just like the website!

## 📁 Where Are My Files?

Your projects are stored in:
```
backend/projects/
├── websites/      # Your website projects
├── games/         # Your game projects
└── deployments/   # Deployed projects
```

Each project contains:
- HTML/CSS/JS files (for websites and web games)
- Python files (for Pygame)
- Configuration files
- Generated API helpers

## 🔧 Customizing

### Edit Generated Code
All files are in `backend/projects/[type]/[project-id]/`
- Edit HTML, CSS, JS directly
- Files are ready to run!

### Modify Database
Go to Database tab:
- Add more columns
- Create more tables
- Insert sample data

### Update Integration
In Integration tab:
- Modify API endpoints
- Reconfigure database links
- Redeploy projects

## 🐛 Troubleshooting

### npm/node not recognized on Windows PowerShell?

This is a PATH issue. In your PowerShell terminal, run:
```powershell
$env:Path = "C:\Program Files\nodejs;$env:Path"
```

Then verify:
```powershell
node --version
npm --version
```

For a permanent fix:
1. Press **Win + X** and search for **"Environment Variables"**
2. Click **"Edit the system environment variables"**
3. Click **"Environment Variables..."** button
4. Under "User variables", click **"New"**
5. Variable name: `Path`
6. Variable value: `C:\Program Files\nodejs`
7. Click **OK** on all dialogs
8. **Restart PowerShell**

### Dependency version errors during pip install?

**Error examples:**
```
ERROR: Could not find a version that satisfies Flask==2.3.0
ERROR: No matching distribution found for SQLAlchemy==2.0.0
ERROR: Could not find a version that satisfies PyMySQL==1.1.0
```

**Solution**: These versions don't exist on PyPI. The project uses stable versions instead:

**Correct versions in requirements.txt:**
```
Flask==2.0.3
Flask-CORS==3.0.10
SQLAlchemy==1.4.46
PyMySQL==1.0.2
psycopg2-binary==2.9.3
python-dotenv==0.19.0
```

**If you still have errors, try:**
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Then install with force-reinstall
pip install -r requirements.txt --force-reinstall

# Or install manually with correct versions
pip install Flask==2.0.3 SQLAlchemy==1.4.46 Flask-CORS==3.0.10 PyMySQL==1.0.2 psycopg2-binary==2.9.3 python-dotenv==0.19.0
```

**Backend won't start?**
```bash
# Make sure port 5000 is free
# Or change port in backend/app.py
```

**Frontend won't connect to backend?**
- Check if backend is running on `http://localhost:5000`
- Check browser console for errors
- Try refreshing the page

**Database connection failed?**
- For SQLite: ensure the directory exists
- For MySQL/PostgreSQL: check credentials
- Verify database server is running

**Port 3000 already in use?**
```bash
# Set a different port
PORT=3001 npm start
```

## 📚 Learn More

Check the full [README.md](../README.md) for:
- Detailed API documentation
- Advanced features
- More examples
- Architecture details

## 🎯 Next Steps

1. **Explore all templates** - Try different website and game templates
2. **Experiment with databases** - Create different table structures
3. **Build integrations** - Link multiple projects to one database
4. **Deploy projects** - Get your projects ready for production
5. **Customize code** - Modify generated code to add features
6. **Read the docs** - Learn about all available APIs

## 💡 Tips

- **Save early**: Database changes are immediate
- **Test locally**: Use SQLite for development
- **Backup projects**: The `deployments` folder has backups
- **Share projects**: Export the project folder to share
- **Version control**: Use Git to track changes

---

**You're all set! Happy building! 🚀**

Need help? Check the full documentation in the main README.md
