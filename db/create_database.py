"""
Pratibimb Database Schema and Data Migration Script
This script creates a comprehensive SQLite database with all content from the UI pages
"""

import sqlite3
import json
from datetime import datetime, timedelta
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'pratibimb.db')

def create_database():
    """Create the SQLite database with comprehensive schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # ==========================================
    # CORE SYSTEM TABLES
    # ==========================================
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        avatar_url VARCHAR(500),
        role VARCHAR(50) DEFAULT 'user',
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Categories table (for various content categorization)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        slug VARCHAR(100) UNIQUE NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        parent_id INTEGER REFERENCES categories(id),
        sort_order INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # NEWS & CAROUSEL CONTENT
    # ==========================================
    
    # News/Carousel slides
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carousel_slides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        image_url VARCHAR(500),
        background_gradient VARCHAR(255),
        slide_type VARCHAR(50) DEFAULT 'news',
        link_url VARCHAR(500),
        is_active BOOLEAN DEFAULT 1,
        sort_order INTEGER DEFAULT 0,
        publish_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # MARKETPLACE/STORE CONTENT
    # ==========================================
    
    # Product categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        slug VARCHAR(100) UNIQUE NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        is_active BOOLEAN DEFAULT 1,
        sort_order INTEGER DEFAULT 0
    )
    """)
    
    # Products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        short_description VARCHAR(500),
        category_id INTEGER REFERENCES product_categories(id),
        price DECIMAL(10,2),
        currency VARCHAR(10) DEFAULT 'INR',
        price_unit VARCHAR(50),
        location VARCHAR(100),
        rating DECIMAL(3,2) DEFAULT 0.0,
        rating_count INTEGER DEFAULT 0,
        image_url VARCHAR(500),
        vendor_name VARCHAR(255),
        is_featured BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        stock_status VARCHAR(50) DEFAULT 'in_stock',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Product features
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        feature_name VARCHAR(255) NOT NULL,
        feature_value TEXT,
        sort_order INTEGER DEFAULT 0
    )
    """)
    
    # ==========================================
    # COMMUNITY CONTENT
    # ==========================================
    
    # Community features/tools
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        action_type VARCHAR(100),
        action_target VARCHAR(255),
        is_active BOOLEAN DEFAULT 1,
        sort_order INTEGER DEFAULT 0
    )
    """)
    
    # DIY Projects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diy_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        difficulty_level VARCHAR(50),
        estimated_time VARCHAR(100),
        materials_needed TEXT,
        step_count INTEGER,
        category VARCHAR(100),
        author_id INTEGER REFERENCES users(id),
        is_featured BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # DIY Project steps
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diy_project_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER REFERENCES diy_projects(id) ON DELETE CASCADE,
        step_number INTEGER NOT NULL,
        title VARCHAR(255),
        description TEXT NOT NULL,
        image_url VARCHAR(500),
        estimated_time VARCHAR(50)
    )
    """)
    
    # ==========================================
    # FORUM/Q&A CONTENT
    # ==========================================
    
    # Forum categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        sort_order INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1
    )
    """)
    
    # Forum posts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        preview TEXT,
        author_id INTEGER REFERENCES users(id),
        category_id INTEGER REFERENCES forum_categories(id),
        post_type VARCHAR(50) DEFAULT 'question',
        status VARCHAR(50) DEFAULT 'open',
        is_pinned BOOLEAN DEFAULT 0,
        is_answered BOOLEAN DEFAULT 0,
        view_count INTEGER DEFAULT 0,
        like_count INTEGER DEFAULT 0,
        reply_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Forum replies
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER REFERENCES forum_posts(id) ON DELETE CASCADE,
        content TEXT NOT NULL,
        author_id INTEGER REFERENCES users(id),
        parent_reply_id INTEGER REFERENCES forum_replies(id),
        is_accepted BOOLEAN DEFAULT 0,
        like_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # LEARNING CENTER CONTENT
    # ==========================================
    
    # Learning tools/services
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        slug VARCHAR(255) UNIQUE NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        tool_type VARCHAR(100),
        is_active BOOLEAN DEFAULT 1,
        sort_order INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Learning content/tutorials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_id INTEGER REFERENCES learning_tools(id),
        title VARCHAR(255) NOT NULL,
        content TEXT,
        content_type VARCHAR(50),
        difficulty_level VARCHAR(50),
        estimated_duration VARCHAR(100),
        prerequisites TEXT,
        is_featured BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # ACTIVITY & UPDATES
    # ==========================================
    
    # Recent activity/updates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recent_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        activity_type VARCHAR(100) NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        related_id INTEGER,
        related_type VARCHAR(100),
        is_public BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Latest updates (for sidebar)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS latest_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        update_type VARCHAR(100),
        link_url VARCHAR(500),
        is_featured BOOLEAN DEFAULT 0,
        publish_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # QUICK LINKS & NAVIGATION
    # ==========================================
    
    # Quick access links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quick_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        icon VARCHAR(100),
        link_url VARCHAR(500) NOT NULL,
        category VARCHAR(100),
        is_active BOOLEAN DEFAULT 1,
        sort_order INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==========================================
    # SYSTEM SETTINGS & METADATA
    # ==========================================
    
    # Site settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key VARCHAR(255) UNIQUE NOT NULL,
        setting_value TEXT,
        setting_type VARCHAR(50) DEFAULT 'string',
        description TEXT,
        is_public BOOLEAN DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_forum_posts_author ON forum_posts(author_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_forum_posts_category ON forum_posts(category_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_forum_posts_created ON forum_posts(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recent_activities_user ON recent_activities(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recent_activities_created ON recent_activities(created_at)")
    
    conn.commit()
    return conn

def insert_sample_data(conn):
    """Insert all the sample data from UI pages"""
    cursor = conn.cursor()
    
    # ==========================================
    # INSERT USERS
    # ==========================================
    users_data = [
        ("bhupinder_chawla", "bhupinder.chawla@infosys.com", "Bhupinder Singh Chawla", None, "admin"),
        ("rahul_sharma", "rahul.sharma@example.com", "Rahul Sharma", None, "user"),
        ("priya_educator", "priya@example.com", "Priya Educator", None, "educator"),
        ("math_teacher_delhi", "math.teacher@example.com", "Math Teacher Delhi", None, "educator"),
        ("accessibility_dev", "dev@example.com", "Accessibility Developer", None, "developer"),
        ("expert_braille", "expert@example.com", "Expert Braille", None, "expert"),
        ("student_mumbai", "student@example.com", "Student Mumbai", None, "student"),
        ("pratibimb_team", "team@pratibimb.com", "Pratibimb Team", None, "admin"),
        ("researcher_iit", "researcher@iit.ac.in", "IIT Researcher", None, "researcher"),
        ("teacher_chennai", "teacher@example.com", "Teacher Chennai", None, "educator"),
        ("community_mod", "mod@pratibimb.com", "Community Moderator", None, "moderator")
    ]
    
    cursor.executemany("""
    INSERT INTO users (username, email, full_name, avatar_url, role) 
    VALUES (?, ?, ?, ?, ?)
    """, users_data)
    
    # ==========================================
    # INSERT CAROUSEL SLIDES
    # ==========================================
    carousel_data = [
        (
            "Revolutionary AI-Powered Braille Display Launched",
            "A groundbreaking 40-cell refreshable Braille display with AI integration has been unveiled, offering real-time content translation and haptic feedback for enhanced accessibility.",
            None,
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "Breaking News",
            "#",
            1,
            0,
            "2025-07-30"
        ),
        (
            "Delhi Accessibility Summit 2025 - Register Now!",
            "Join us at India Habitat Centre, Delhi on August 15th for the largest accessibility conference in India. Features workshops on Braille technology, assistive AI, and inclusive design.",
            None,
            "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "Local Event",
            "#",
            1,
            1,
            "2025-08-15"
        ),
        (
            "Microsoft Releases Enhanced Screen Reader with GPT Integration",
            "The new Narrator update includes intelligent image descriptions, context-aware reading, and natural language interaction powered by advanced AI models.",
            None,
            "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "Technology",
            "#",
            1,
            2,
            "2025-07-28"
        ),
        (
            "IIT Delhi Develops Smart Navigation System for Visually Impaired",
            "Researchers have created an innovative indoor navigation system using ultrasonic sensors and smartphone integration, tested successfully across major Indian cities.",
            None,
            "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
            "Research",
            "#",
            1,
            3,
            "2025-07-25"
        ),
        (
            "UN Launches Global Accessibility Standards Framework",
            "New international guidelines for digital accessibility released, including mandatory Braille support for all government websites by 2026.",
            None,
            "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)",
            "Global Initiative",
            "#",
            1,
            4,
            "2025-07-22"
        )
    ]
    
    cursor.executemany("""
    INSERT INTO carousel_slides (title, description, image_url, background_gradient, slide_type, link_url, is_active, sort_order, publish_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, carousel_data)
    
    # ==========================================
    # INSERT PRODUCT CATEGORIES
    # ==========================================
    product_categories_data = [
        ("All Products", "all", "All accessibility products and services", "fas fa-th-large"),
        ("Services", "services", "Professional accessibility services", "fas fa-cogs"),
        ("Hardware", "hardware", "Physical accessibility devices", "fas fa-microchip"),
        ("Software", "software", "Accessibility software solutions", "fas fa-desktop"),
        ("Education", "education", "Educational accessibility tools", "fas fa-graduation-cap"),
        ("Mobility", "mobility", "Mobility assistance products", "fas fa-wheelchair")
    ]
    
    cursor.executemany("""
    INSERT INTO product_categories (name, slug, description, icon)
    VALUES (?, ?, ?, ?)
    """, product_categories_data)
    
    # ==========================================
    # INSERT PRODUCTS
    # ==========================================
    products_data = [
        (
            "BraaS - Braille as a Service",
            "Professional Braille conversion service with fast turnaround time. Convert any document, image, or digital content to high-quality Braille format.",
            "Professional Braille conversion service",
            2,  # services category
            10.00,
            "INR",
            "per page",
            "Mysore",
            4.8,
            127,
            None,
            "Pratibimb Solutions",
            1,
            1,
            "in_stock"
        ),
        (
            "Advanced Screen Reader Pro",
            "State-of-the-art screen reading software with AI-powered natural language processing, multi-language support, and advanced navigation features.",
            "AI-powered screen reading software",
            4,  # software category
            1500.00,
            "INR",
            "one-time",
            "Bangalore",
            4.5,
            89,
            None,
            "AccessTech India",
            1,
            1,
            "in_stock"
        ),
        (
            "Smart Braille Display 40-Cell",
            "Latest generation refreshable Braille display with 40 cells, USB-C connectivity, and wireless Bluetooth support. Compatible with all major screen readers.",
            "40-cell refreshable Braille display",
            3,  # hardware category
            25000.00,
            "INR",
            "one-time",
            "Delhi",
            4.7,
            45,
            None,
            "BrailleTech Solutions",
            1,
            1,
            "in_stock"
        ),
        (
            "Voice Navigation Assistant",
            "Intelligent voice-controlled navigation system for indoor and outdoor mobility. Features GPS integration, obstacle detection, and route optimization.",
            "AI voice navigation system",
            6,  # mobility category
            8500.00,
            "INR",
            "one-time",
            "Chennai",
            4.6,
            67,
            None,
            "NaviAssist Technologies",
            0,
            1,
            "in_stock"
        ),
        (
            "Braille Learning Kit for Schools",
            "Comprehensive educational package including Braille books, tactile learning materials, and teacher training resources for inclusive classroom environments.",
            "Complete Braille education package",
            5,  # education category
            3500.00,
            "INR",
            "per kit",
            "Mumbai",
            4.9,
            156,
            None,
            "EduAccess India",
            1,
            1,
            "in_stock"
        ),
        (
            "Tactile Graphics Converter",
            "Professional software for converting images, charts, and diagrams into tactile graphics suitable for Braille embossing and 3D printing.",
            "Image to tactile graphics converter",
            4,  # software category
            2200.00,
            "INR",
            "one-time",
            "Pune",
            4.4,
            73,
            None,
            "TactileWorks",
            0,
            1,
            "in_stock"
        )
    ]
    
    cursor.executemany("""
    INSERT INTO products (title, description, short_description, category_id, price, currency, price_unit, location, rating, rating_count, image_url, vendor_name, is_featured, is_active, stock_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products_data)
    
    # ==========================================
    # INSERT COMMUNITY FEATURES
    # ==========================================
    community_features_data = [
        ("Join Volunteer Program", "Help make accessibility tools better for everyone", "fas fa-hands-helping", "volunteer", "volunteer-program"),
        ("Sign Up for Beta Testing", "Be among the first to test new features and tools", "fas fa-flask", "beta", "signup-form"),
        ("Connect with Experts", "Get guidance from accessibility professionals", "fas fa-user-tie", "connect", "expert-connect"),
        ("Explore DIY Projects", "Build your own accessibility solutions", "fas fa-tools", "diy", "diy-projects")
    ]
    
    cursor.executemany("""
    INSERT INTO community_features (title, description, icon, action_type, action_target)
    VALUES (?, ?, ?, ?, ?)
    """, community_features_data)
    
    # ==========================================
    # INSERT DIY PROJECTS
    # ==========================================
    diy_projects_data = [
        (
            "DIY Braille Keyboard",
            "Build your own tactile Braille keyboard using mechanical switches and 3D printed keycaps",
            "Intermediate",
            "4-6 hours",
            "Mechanical keyboard, 3D printer, PLA filament, soldering kit",
            8,
            "hardware",
            8,  # accessibility_dev user
            1,
            1
        ),
        (
            "Voice-Controlled Audio Book Reader",
            "Create a hands-free audio book reader with voice commands using Raspberry Pi",
            "Advanced",
            "6-8 hours",
            "Raspberry Pi 4, USB microphone, speakers, SD card",
            12,
            "software",
            8,  # accessibility_dev user
            1,
            1
        )
    ]
    
    cursor.executemany("""
    INSERT INTO diy_projects (title, description, difficulty_level, estimated_time, materials_needed, step_count, category, author_id, is_featured, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, diy_projects_data)
    
    # ==========================================
    # INSERT FORUM CATEGORIES
    # ==========================================
    forum_categories_data = [
        ("General Discussion", "General accessibility topics and discussions", "fas fa-comments"),
        ("Technical Support", "Get help with technical issues", "fas fa-life-ring"),
        ("Feature Requests", "Suggest new features and improvements", "fas fa-lightbulb"),
        ("Hardware", "Discuss accessibility hardware", "fas fa-microchip"),
        ("Software", "Software-related discussions", "fas fa-desktop"),
        ("Education", "Educational accessibility topics", "fas fa-graduation-cap")
    ]
    
    cursor.executemany("""
    INSERT INTO forum_categories (name, description, icon)
    VALUES (?, ?, ?)
    """, forum_categories_data)
    
    # ==========================================
    # INSERT FORUM POSTS
    # ==========================================
    forum_posts_data = [
        (
            "How to optimize Braille art for different embosser models?",
            "I'm having trouble getting consistent output across ViewPlus and Index embossers. The dot spacing seems different and some fine details are lost when switching between models. Has anyone found effective preprocessing techniques or settings that work well across different embosser types?",
            "I'm having trouble getting consistent output across ViewPlus and Index embossers. The dot spacing seems different...",
            2,  # rahul_sharma
            4,  # hardware category
            "question",
            "open",
            0,
            0,
            24,
            5,
            3
        ),
        (
            "Image preprocessing best practices for tactile graphics",
            "What's the optimal contrast and brightness settings for converting photographs to meaningful Braille patterns? I'm working on educational materials and want to ensure the tactile graphics convey the essential information effectively.",
            "What's the optimal contrast and brightness settings for converting photographs to meaningful Braille patterns?",
            3,  # priya_educator
            5,  # software category
            "question",
            "open",
            0,
            0,
            42,
            8,
            6
        ),
        (
            "Feature Request: Math equation support in Braille converter",
            "Would love to see support for LaTeX/MathML equations in the text-to-Braille converter. This would be huge for STEM education accessibility. Currently having to manually convert complex mathematical notation which is very time-consuming.",
            "Would love to see support for LaTeX/MathML equations in the text-to-Braille converter. This would be huge for STEM education...",
            4,  # math_teacher_delhi
            3,  # feature requests category
            "feature_request",
            "open",
            0,
            0,
            67,
            12,
            9
        ),
        (
            "Troubleshooting: Moon phases module not loading images",
            "The new moon phases educational module shows '[Error: Could not load image]' for all moon phase images. I've tried refreshing and clearing cache but the issue persists. Anyone else experiencing this?",
            "The new moon phases educational module shows '[Error: Could not load image]' for all moon phase images. Any solutions?",
            5,  # accessibility_dev
            2,  # technical support category
            "question",
            "open",
            0,
            0,
            18,
            2,
            4
        )
    ]
    
    cursor.executemany("""
    INSERT INTO forum_posts (title, content, preview, author_id, category_id, post_type, status, is_pinned, is_answered, view_count, like_count, reply_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, forum_posts_data)
    
    # ==========================================
    # INSERT LEARNING TOOLS
    # ==========================================
    learning_tools_data = [
        ("YouTube to Braille", "youtube-braille", "Convert YouTube videos to Braille text and audio descriptions", "fab fa-youtube", "converter"),
        ("Braille Art Editor", "braille-art", "Create and edit Braille art and tactile graphics", "fas fa-palette", "editor"),
        ("Learn Braille", "learn-braille", "Interactive Braille learning system with typing practice", "fas fa-book-open", "tutorial"),
        ("Text to Braille", "text-converter", "Convert text documents to Braille format", "fas fa-font", "converter"),
        ("Dhvani Assistant", "dhvani", "Voice-powered accessibility assistant", "fas fa-microphone", "assistant"),
        ("Braille as a Service", "braas", "Professional Braille conversion service", "fas fa-cloud", "service")
    ]
    
    cursor.executemany("""
    INSERT INTO learning_tools (name, slug, description, icon, tool_type)
    VALUES (?, ?, ?, ?, ?)
    """, learning_tools_data)
    
    # ==========================================
    # INSERT RECENT ACTIVITIES
    # ==========================================
    recent_activities_data = [
        (6, "answer", "answered \"Embosser calibration guide\"", "Provided detailed calibration steps for multiple embosser models", 1, "forum_post"),
        (7, "question", "asked \"Grade 2 Braille support timeline?\"", "Inquired about upcoming Grade 2 Braille features", 2, "forum_post"),
        (8, "update", "posted \"Weekly development update\"", "Shared progress on new accessibility features", None, "announcement"),
        (9, "research", "shared \"Tactile feedback study results\"", "Published findings from user experience research", None, "research"),
        (10, "activity", "liked \"Creating inclusive classroom materials\"", "Appreciated educational content", 3, "forum_post"),
        (11, "moderation", "pinned \"Community guidelines updated\"", "Highlighted important community updates", None, "announcement")
    ]
    
    # Calculate timestamps (recent activities)
    base_time = datetime.now()
    activity_times = [
        base_time - timedelta(minutes=2),
        base_time - timedelta(minutes=15),
        base_time - timedelta(hours=1),
        base_time - timedelta(hours=2),
        base_time - timedelta(hours=3),
        base_time - timedelta(hours=5)
    ]
    
    for i, (user_id, activity_type, title, description, related_id, related_type) in enumerate(recent_activities_data):
        cursor.execute("""
        INSERT INTO recent_activities (user_id, activity_type, title, description, related_id, related_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, activity_type, title, description, related_id, related_type, activity_times[i]))
    
    # ==========================================
    # INSERT LATEST UPDATES
    # ==========================================
    latest_updates_data = [
        (
            "Moon Phases Educational Module",
            "New tactile learning module with 8 moon phase images converted to Braille art",
            "feature",
            "#",
            1,
            "2025-07-30"
        ),
        (
            "DIY: Voice-Controlled Braille Printer",
            "Step-by-step guide to build a voice-activated Braille embosser using Raspberry Pi",
            "tutorial",
            "#",
            1,
            "2025-07-28"
        ),
        (
            "Hearing Impairment Support Beta",
            "Testing new sign language to Braille converter for dual accessibility support",
            "beta",
            "#",
            0,
            "2025-07-25"
        ),
        (
            "Community Workshop: Tactile Graphics",
            "Virtual workshop on creating educational tactile graphics using Pratibimb tools",
            "event",
            "#",
            0,
            "2025-08-05"
        )
    ]
    
    cursor.executemany("""
    INSERT INTO latest_updates (title, description, update_type, link_url, is_featured, publish_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, latest_updates_data)
    
    # ==========================================
    # INSERT QUICK LINKS
    # ==========================================
    quick_links_data = [
        ("YouTube to Braille Converter", "Convert YouTube videos to accessible Braille content", "fab fa-youtube", "learn.html#youtube-braille", "converter"),
        ("Dhvani (Voice Assistant)", "AI-powered voice assistant for accessibility", "fas fa-microphone", "dhvani.html", "assistant"),
        ("Braille Art Editor", "Create beautiful tactile art and graphics", "fas fa-palette", "learn.html#braille-art", "editor"),
        ("Learn Braille", "Interactive Braille learning system", "fas fa-book-open", "learn.html#learn-braille", "education"),
        ("Braille as a Service", "Professional Braille conversion service", "fas fa-cloud", "learn.html#braille-service", "service"),
        ("Text to Braille Converter", "Convert any text to Braille format", "fas fa-font", "learn.html#text-converter", "converter"),
        ("Community Hub", "Connect with accessibility community", "fas fa-globe", "community.html", "community")
    ]
    
    cursor.executemany("""
    INSERT INTO quick_links (title, description, icon, link_url, category)
    VALUES (?, ?, ?, ?, ?)
    """, quick_links_data)
    
    # ==========================================
    # INSERT SITE SETTINGS
    # ==========================================
    site_settings_data = [
        ("site_title", "Pratibimb", "string", "Main site title", 1),
        ("site_tagline", "True Reflection of Digital World!", "string", "Site tagline", 1),
        ("version", "v2.1", "string", "Application version", 1),
        ("company", "Infosys", "string", "Company name", 1),
        ("copyright_year", "2025", "string", "Copyright year", 1),
        ("default_language", "english", "string", "Default language", 0),
        ("maintenance_mode", "false", "boolean", "Maintenance mode status", 0)
    ]
    
    cursor.executemany("""
    INSERT INTO site_settings (setting_key, setting_value, setting_type, description, is_public)
    VALUES (?, ?, ?, ?, ?)
    """, site_settings_data)
    
    conn.commit()
    print("✅ Sample data inserted successfully!")

def main():
    """Main function to create database and populate with data"""
    print("🚀 Creating Pratibimb database...")
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Removed existing database")
    
    # Create new database with schema
    conn = create_database()
    print("✅ Database schema created successfully!")
    
    # Insert sample data
    insert_sample_data(conn)
    
    # Close connection
    conn.close()
    
    print(f"✅ Database created successfully at: {DB_PATH}")
    print("📊 Database contains:")
    print("   - Users and authentication data")
    print("   - Carousel slides and news content")
    print("   - Marketplace products and categories")
    print("   - Community features and DIY projects")
    print("   - Forum posts and Q&A content")
    print("   - Learning tools and educational content")
    print("   - Recent activities and updates")
    print("   - Quick links and navigation data")
    print("   - Site settings and configuration")

if __name__ == "__main__":
    main()
