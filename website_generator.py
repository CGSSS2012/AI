"""
Website Generator Module
Handles website creation and code generation
"""

import json
import os
from pathlib import Path
from datetime import datetime
import uuid

class WebsiteGenerator:
    def __init__(self):
        self.projects_dir = Path("projects/websites")
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.projects = {}
        self.templates = self._load_templates()

    def _load_templates(self):
        """Load available website templates"""
        return {
            'basic': {
                'name': 'Basic HTML Site',
                'description': 'Simple static HTML website',
                'files': ['index.html', 'style.css', 'script.js']
            },
            'blog': {
                'name': 'Blog Platform',
                'description': 'Blog with posts and categories',
                'files': ['index.html', 'blog.html', 'post.html', 'style.css', 'script.js']
            },
            'ecommerce': {
                'name': 'E-Commerce Site',
                'description': 'Product catalog with shopping cart',
                'files': ['index.html', 'products.html', 'product-detail.html', 'cart.html', 'checkout.html', 'style.css', 'script.js']
            },
            'portfolio': {
                'name': 'Portfolio Website',
                'description': 'Personal portfolio showcase',
                'files': ['index.html', 'about.html', 'projects.html', 'contact.html', 'style.css', 'script.js']
            },
            'saas': {
                'name': 'SaaS Landing Page',
                'description': 'Software as a Service landing page',
                'files': ['index.html', 'features.html', 'pricing.html', 'docs.html', 'style.css', 'script.js']
            }
        }

    def get_templates(self):
        """Get available website templates"""
        return self.templates

    def create_website(self, name, description, template='basic', pages=None, style=None):
        """Create a new website project"""
        project_id = str(uuid.uuid4())[:8]
        
        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}")
        
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        project_config = {
            'id': project_id,
            'name': name,
            'description': description,
            'template': template,
            'created_at': datetime.now().isoformat(),
            'pages': pages or [],
            'style': style or {},
            'files': {}
        }
        
        # Generate basic files
        self._generate_template_files(project_dir, template, project_config)
        
        # Save project config
        config_file = project_dir / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        self.projects[project_id] = project_config
        return project_id

    def _generate_template_files(self, project_dir, template, config):
        """Generate template files for the website"""
        
        # Generate HTML files
        if template == 'basic':
            self._create_basic_html(project_dir / 'index.html', config)
        elif template == 'blog':
            self._create_blog_structure(project_dir, config)
        elif template == 'ecommerce':
            self._create_ecommerce_structure(project_dir, config)
        elif template == 'portfolio':
            self._create_portfolio_structure(project_dir, config)
        elif template == 'saas':
            self._create_saas_structure(project_dir, config)
        
        # Generate CSS
        self._create_stylesheet(project_dir / 'style.css', config.get('style', {}))
        
        # Generate JavaScript
        self._create_script(project_dir / 'script.js', config)
        
        # Generate package.json for dependencies
        self._create_package_json(project_dir, config)

    def _create_basic_html(self, filepath, config):
        """Create basic HTML file"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['name']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{config['name']}</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="home" class="hero">
            <h2>Welcome to {config['name']}</h2>
            <p>{config['description']}</p>
        </section>

        <section id="about" class="content">
            <h2>About Us</h2>
            <p>Learn more about our amazing project.</p>
        </section>

        <section id="services" class="content">
            <h2>Services</h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3>Service 1</h3>
                    <p>Description of service 1</p>
                </div>
                <div class="service-card">
                    <h3>Service 2</h3>
                    <p>Description of service 2</p>
                </div>
                <div class="service-card">
                    <h3>Service 3</h3>
                    <p>Description of service 3</p>
                </div>
            </div>
        </section>

        <section id="contact" class="content">
            <h2>Get in Touch</h2>
            <form id="contact-form">
                <input type="text" placeholder="Your Name" required>
                <input type="email" placeholder="Your Email" required>
                <textarea placeholder="Your Message" required></textarea>
                <button type="submit">Send Message</button>
            </form>
        </section>
    </main>

    <footer>
        <p>&copy; {datetime.now().year} {config['name']}. All rights reserved.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""
        with open(filepath, 'w') as f:
            f.write(html_content)

    def _create_blog_structure(self, project_dir, config):
        """Create blog structure"""
        files = {
            'index.html': '<!-- Blog Homepage -->',
            'blog.html': '<!-- Blog Listing -->',
            'post.html': '<!-- Individual Post -->',
        }
        for filename, content in files.items():
            with open(project_dir / filename, 'w') as f:
                f.write(f"{content}\n<!-- Auto-generated by Agent -->")

    def _create_ecommerce_structure(self, project_dir, config):
        """Create e-commerce structure"""
        files = {
            'index.html': '<!-- E-Commerce Homepage -->',
            'products.html': '<!-- Product Listing -->',
            'product-detail.html': '<!-- Product Detail -->',
            'cart.html': '<!-- Shopping Cart -->',
            'checkout.html': '<!-- Checkout -->',
        }
        for filename, content in files.items():
            with open(project_dir / filename, 'w') as f:
                f.write(f"{content}\n<!-- Auto-generated by Agent -->")

    def _create_portfolio_structure(self, project_dir, config):
        """Create portfolio structure"""
        files = {
            'index.html': '<!-- Portfolio Homepage -->',
            'about.html': '<!-- About Page -->',
            'projects.html': '<!-- Projects Showcase -->',
            'contact.html': '<!-- Contact Page -->',
        }
        for filename, content in files.items():
            with open(project_dir / filename, 'w') as f:
                f.write(f"{content}\n<!-- Auto-generated by Agent -->")

    def _create_saas_structure(self, project_dir, config):
        """Create SaaS structure"""
        files = {
            'index.html': '<!-- SaaS Landing Page -->',
            'features.html': '<!-- Features Page -->',
            'pricing.html': '<!-- Pricing Page -->',
            'docs.html': '<!-- Documentation -->',
        }
        for filename, content in files.items():
            with open(project_dir / filename, 'w') as f:
                f.write(f"{content}\n<!-- Auto-generated by Agent -->")

    def _create_stylesheet(self, filepath, style_config):
        """Create CSS file"""
        css_content = f"""/* {style_config.get('name', 'Website')} Stylesheet */

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: {style_config.get('text_color', '#333')};
    background-color: {style_config.get('bg_color', '#f4f4f4')};
}}

header {{
    background-color: {style_config.get('header_color', '#333')};
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}}

header h1 {{
    text-align: center;
    margin-bottom: 1rem;
}}

nav ul {{
    list-style: none;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
}}

nav ul li {{
    margin: 0 1.5rem;
}}

nav ul li a {{
    color: white;
    text-decoration: none;
    transition: color 0.3s ease;
}}

nav ul li a:hover {{
    color: #ffd700;
}}

main {{
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}}

.hero {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}}

.hero h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.content {{
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 1rem;
}}

.service-card {{
    background: #f9f9f9;
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    transition: transform 0.3s ease;
}}

.service-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}

form {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 500px;
    margin: 1rem auto;
}}

form input, form textarea {{
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}}

form button {{
    padding: 0.75rem;
    background-color: #667eea;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}}

form button:hover {{
    background-color: #764ba2;
}}

footer {{
    background-color: #333;
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
}}

@media (max-width: 768px) {{
    nav ul {{
        flex-direction: column;
        gap: 0.5rem;
    }}
    
    nav ul li {{
        margin: 0.5rem 0;
    }}
    
    .hero h2 {{
        font-size: 1.8rem;
    }}
}}
"""
        with open(filepath, 'w') as f:
            f.write(css_content)

    def _create_script(self, filepath, config):
        """Create JavaScript file"""
        js_content = """// Website Script

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Form submission handler
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        });
    }

    // Add animation to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const elements = document.querySelectorAll('.content, .service-card');
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Utility function to fetch API data
async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Utility function to post data
async function postData(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('Error posting data:', error);
    }
}
"""
        with open(filepath, 'w') as f:
            f.write(js_content)

    def _create_package_json(self, project_dir, config):
        """Create package.json for the project"""
        package_json = {
            "name": config['name'].lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": config['description'],
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "build": "echo 'No build needed for static website'"
            },
            "keywords": ["website", "web"],
            "author": "",
            "license": "MIT"
        }
        
        with open(project_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

    def add_page(self, project_id, page_config):
        """Add a new page to the website"""
        project_dir = self.projects_dir / project_id
        
        if not project_dir.exists():
            raise ValueError(f"Project {project_id} not found")
        
        page_name = page_config['name'].lower().replace(' ', '-')
        page_file = project_dir / f"{page_name}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_config['name']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="content">
        <h2>{page_config['name']}</h2>
        <p>{page_config.get('description', '')}</p>
    </main>
    <script src="script.js"></script>
</body>
</html>
"""
        
        with open(page_file, 'w') as f:
            f.write(html_content)
        
        # Update project config
        config_file = project_dir / 'config.json'
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config['pages'].append({'name': page_config['name'], 'file': f"{page_name}.html"})
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return f"Page '{page_config['name']}' added successfully"

    def list_websites(self):
        """List all created websites"""
        websites = []
        for project_dir in self.projects_dir.glob('*/'):
            config_file = project_dir / 'config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                websites.append(config)
        
        return websites
