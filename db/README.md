# Pratibimb Database

This folder contains the complete SQLite database setup for the Pratibimb accessibility platform, including all content from the UI pages.

## Files

- **`create_database.py`** - Main script to create the database schema and populate with sample data
- **`models.py`** - Database models and schema documentation
- **`database_utils.py`** - Query utilities and data access layer
- **`pratibimb.db`** - SQLite database file (created after running create_database.py)

## Database Schema

The database contains the following main tables:

### Core System Tables
- **`users`** - User accounts and authentication
- **`categories`** - General categorization system
- **`site_settings`** - Application configuration

### Content Tables
- **`carousel_slides`** - Homepage news carousel content
- **`products`** - Marketplace products and services
- **`product_categories`** - Product categorization
- **`product_features`** - Product feature details

### Community Tables
- **`forum_posts`** - Q&A forum posts
- **`forum_categories`** - Forum categorization
- **`forum_replies`** - Forum post replies
- **`community_features`** - Community tools and features
- **`diy_projects`** - DIY project guides
- **`diy_project_steps`** - Step-by-step instructions

### Learning Center Tables
- **`learning_tools`** - Available learning tools
- **`learning_content`** - Educational content and tutorials

### Activity Tables
- **`recent_activities`** - User activities and system events
- **`latest_updates`** - Platform updates and announcements
- **`quick_links`** - Navigation quick access links

## Content Sources

The database is populated with all content from the UI pages:

### From `index.html`:
- 5 carousel news slides
- 4 Q&A forum posts with author details
- 6 recent activity items
- 4 latest platform updates
- 7 quick access links

### From `marketplace.html`:
- 6 product categories (Services, Hardware, Software, Education, Mobility)
- 6+ featured products with pricing, ratings, and vendor info
- Product features and specifications

### From `community.html`:
- 4 community features (Volunteer, Beta Testing, Expert Connect, DIY)
- 2+ DIY projects with difficulty levels and materials
- Project step-by-step instructions

### From `learn.html`:
- 6 learning tools (YouTube to Braille, Braille Art Editor, etc.)
- Educational content and tutorials

## Usage

### 1. Create the Database

```bash
cd db
python create_database.py
```

This will:
- Create `pratibimb.db` SQLite file
- Set up all tables with proper schema
- Populate with sample data from UI pages
- Create necessary indexes for performance

### 2. Query the Database

```python
from database_utils import DatabaseManager

db = DatabaseManager()

# Get carousel slides
slides = db.get_carousel_slides()

# Get featured products
products = db.get_products(featured_only=True)

# Get forum posts
posts = db.get_forum_posts(limit=10)

# Get recent activities
activities = db.get_recent_activities()
```

### 3. Export Data

```python
from database_utils import export_data_to_json

# Export all data to JSON
output_file = export_data_to_json()
print(f"Data exported to {output_file}")
```

## Database Statistics

After running `create_database.py`, the database contains:

- **11 users** (including admin, educators, developers, students)
- **5 carousel slides** (news and announcements)
- **6 products** across different categories
- **4 forum posts** with realistic Q&A content
- **6 learning tools** for accessibility education
- **6 recent activities** showing community engagement
- **4 latest updates** about platform features
- **7 quick links** for easy navigation

## API Integration Ready

The database schema is designed to work seamlessly with FastAPI:

- Normalized structure with proper foreign key relationships
- Comprehensive indexing for performance
- JSON-friendly data types
- Clear separation of concerns
- Ready for REST API endpoints

## Future FastAPI Integration

Suggested API endpoints that can use this database:

```
GET /api/carousel - Homepage carousel slides
GET /api/products - Marketplace products
GET /api/products/{id} - Product details
GET /api/forum/posts - Forum posts
GET /api/activities - Recent activities
GET /api/learning/tools - Learning tools
GET /api/quick-links - Navigation links
```

## Sample Queries

The `database_utils.py` file includes comprehensive query methods:

- Content filtering (active/inactive, featured/all)
- Pagination support
- Category-based filtering
- User role-based queries
- Statistics and analytics
- Data export capabilities

## Development Notes

- All timestamps use ISO format
- Boolean fields use 1/0 for SQLite compatibility
- Foreign key constraints are enabled
- Indexes are created for performance optimization
- Sample data includes realistic user interactions
- Content matches exactly what's shown in UI pages
