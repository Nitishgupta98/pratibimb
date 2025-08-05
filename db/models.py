"""
Database Models and Schema Documentation
This file contains the complete database schema documentation and model definitions
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

# ==========================================
# CORE MODELS
# ==========================================

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    full_name: str
    avatar_url: Optional[str]
    role: str = "user"
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Category:
    id: Optional[int]
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    parent_id: Optional[int]
    sort_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None

# ==========================================
# CONTENT MODELS
# ==========================================

@dataclass
class CarouselSlide:
    id: Optional[int]
    title: str
    description: Optional[str]
    image_url: Optional[str]
    background_gradient: Optional[str]
    slide_type: str = "news"
    link_url: Optional[str]
    is_active: bool = True
    sort_order: int = 0
    publish_date: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Product:
    id: Optional[int]
    title: str
    description: Optional[str]
    short_description: Optional[str]
    category_id: int
    price: Optional[float]
    currency: str = "INR"
    price_unit: Optional[str]
    location: Optional[str]
    rating: float = 0.0
    rating_count: int = 0
    image_url: Optional[str]
    vendor_name: Optional[str]
    is_featured: bool = False
    is_active: bool = True
    stock_status: str = "in_stock"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class ForumPost:
    id: Optional[int]
    title: str
    content: str
    preview: Optional[str]
    author_id: int
    category_id: int
    post_type: str = "question"
    status: str = "open"
    is_pinned: bool = False
    is_answered: bool = False
    view_count: int = 0
    like_count: int = 0
    reply_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class LearningTool:
    id: Optional[int]
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    tool_type: Optional[str]
    is_active: bool = True
    sort_order: int = 0
    created_at: Optional[datetime] = None

@dataclass
class QuickLink:
    id: Optional[int]
    title: str
    description: Optional[str]
    icon: Optional[str]
    link_url: str
    category: Optional[str]
    is_active: bool = True
    sort_order: int = 0
    created_at: Optional[datetime] = None

# ==========================================
# DATABASE SCHEMA DOCUMENTATION
# ==========================================

DATABASE_SCHEMA = {
    "description": "Pratibimb Accessibility Platform Database Schema",
    "version": "1.0",
    "created": "2025-08-02",
    "tables": {
        "users": {
            "description": "User accounts and authentication",
            "columns": {
                "id": "Primary key, auto-increment",
                "username": "Unique username, max 100 chars",
                "email": "Unique email address, max 255 chars",
                "full_name": "User's full name, max 255 chars",
                "avatar_url": "URL to user avatar image, max 500 chars",
                "role": "User role (user, admin, educator, developer, etc.)",
                "is_active": "Boolean, account active status",
                "created_at": "Account creation timestamp",
                "updated_at": "Last update timestamp"
            },
            "indexes": ["username", "email", "role"],
            "relationships": [
                "One-to-many with forum_posts",
                "One-to-many with recent_activities",
                "One-to-many with diy_projects"
            ]
        },
        
        "carousel_slides": {
            "description": "Homepage carousel/news content",
            "columns": {
                "id": "Primary key, auto-increment",
                "title": "Slide title, max 255 chars",
                "description": "Slide description text",
                "image_url": "Background image URL, max 500 chars",
                "background_gradient": "CSS gradient for background",
                "slide_type": "Type of slide (news, event, technology, etc.)",
                "link_url": "Target URL when slide clicked",
                "is_active": "Boolean, slide visibility",
                "sort_order": "Display order",
                "publish_date": "Publication date",
                "created_at": "Creation timestamp",
                "updated_at": "Last update timestamp"
            },
            "indexes": ["is_active", "sort_order", "publish_date"]
        },
        
        "products": {
            "description": "Marketplace products and services",
            "columns": {
                "id": "Primary key, auto-increment",
                "title": "Product name, max 255 chars",
                "description": "Full product description",
                "short_description": "Brief product summary, max 500 chars",
                "category_id": "Foreign key to product_categories",
                "price": "Product price, decimal(10,2)",
                "currency": "Price currency code (INR, USD, etc.)",
                "price_unit": "Price unit (one-time, per page, per month, etc.)",
                "location": "Product/service location",
                "rating": "Average rating, decimal(3,2)",
                "rating_count": "Number of ratings",
                "image_url": "Product image URL",
                "vendor_name": "Vendor/company name",
                "is_featured": "Boolean, featured product status",
                "is_active": "Boolean, product availability",
                "stock_status": "Stock status (in_stock, out_of_stock, etc.)",
                "created_at": "Creation timestamp",
                "updated_at": "Last update timestamp"
            },
            "indexes": ["category_id", "is_active", "is_featured", "rating"],
            "relationships": [
                "Many-to-one with product_categories",
                "One-to-many with product_features"
            ]
        },
        
        "forum_posts": {
            "description": "Community forum posts and questions",
            "columns": {
                "id": "Primary key, auto-increment",
                "title": "Post title, max 255 chars",
                "content": "Full post content",
                "preview": "Post preview text",
                "author_id": "Foreign key to users",
                "category_id": "Foreign key to forum_categories",
                "post_type": "Type (question, discussion, announcement)",
                "status": "Post status (open, closed, answered)",
                "is_pinned": "Boolean, pinned post status",
                "is_answered": "Boolean, question answered status",
                "view_count": "Number of views",
                "like_count": "Number of likes",
                "reply_count": "Number of replies",
                "created_at": "Creation timestamp",
                "updated_at": "Last update timestamp"
            },
            "indexes": ["author_id", "category_id", "created_at", "post_type"],
            "relationships": [
                "Many-to-one with users",
                "Many-to-one with forum_categories",
                "One-to-many with forum_replies"
            ]
        },
        
        "learning_tools": {
            "description": "Learning center tools and services",
            "columns": {
                "id": "Primary key, auto-increment",
                "name": "Tool name, max 255 chars",
                "slug": "URL-friendly identifier, unique",
                "description": "Tool description",
                "icon": "Icon class/identifier",
                "tool_type": "Type (converter, editor, tutorial, etc.)",
                "is_active": "Boolean, tool availability",
                "sort_order": "Display order",
                "created_at": "Creation timestamp"
            },
            "indexes": ["slug", "tool_type", "is_active"],
            "relationships": [
                "One-to-many with learning_content"
            ]
        },
        
        "quick_links": {
            "description": "Quick access navigation links",
            "columns": {
                "id": "Primary key, auto-increment",
                "title": "Link title, max 255 chars",
                "description": "Link description",
                "icon": "Icon class/identifier",
                "link_url": "Target URL, max 500 chars",
                "category": "Link category for grouping",
                "is_active": "Boolean, link visibility",
                "sort_order": "Display order",
                "created_at": "Creation timestamp"
            },
            "indexes": ["category", "is_active", "sort_order"]
        },
        
        "recent_activities": {
            "description": "User activities and system events",
            "columns": {
                "id": "Primary key, auto-increment",
                "user_id": "Foreign key to users",
                "activity_type": "Type of activity (answer, question, update, etc.)",
                "title": "Activity title/summary",
                "description": "Activity description",
                "related_id": "Related entity ID (post, product, etc.)",
                "related_type": "Related entity type",
                "is_public": "Boolean, public visibility",
                "created_at": "Activity timestamp"
            },
            "indexes": ["user_id", "created_at", "activity_type"],
            "relationships": [
                "Many-to-one with users"
            ]
        }
    },
    
    "data_sources": {
        "index.html": [
            "carousel_slides (5 news items)",
            "forum_posts (4 Q&A posts)",
            "recent_activities (6 activities)",
            "latest_updates (4 updates)",
            "quick_links (7 navigation items)"
        ],
        "marketplace.html": [
            "product_categories (6 categories)",
            "products (6+ products)",
            "product_features (multiple per product)"
        ],
        "community.html": [
            "community_features (4 features)",
            "diy_projects (2+ projects)",
            "diy_project_steps (multiple per project)"
        ],
        "learn.html": [
            "learning_tools (6 tools)",
            "learning_content (educational materials)"
        ]
    },
    
    "api_endpoints": {
        "suggested": [
            "GET /api/carousel - Get carousel slides",
            "GET /api/products - Get marketplace products",
            "GET /api/products/{id} - Get product details",
            "GET /api/forum/posts - Get forum posts",
            "GET /api/forum/posts/{id} - Get post details",
            "GET /api/activities - Get recent activities",
            "GET /api/quick-links - Get navigation links",
            "GET /api/learning/tools - Get learning tools",
            "GET /api/updates - Get latest updates"
        ]
    }
}

def print_schema_summary():
    """Print a summary of the database schema"""
    print("=" * 60)
    print("PRATIBIMB DATABASE SCHEMA SUMMARY")
    print("=" * 60)
    print(f"Version: {DATABASE_SCHEMA['version']}")
    print(f"Created: {DATABASE_SCHEMA['created']}")
    print(f"Description: {DATABASE_SCHEMA['description']}")
    print()
    
    print("TABLES:")
    print("-" * 40)
    for table_name, table_info in DATABASE_SCHEMA['tables'].items():
        print(f"📋 {table_name}")
        print(f"   {table_info['description']}")
        print(f"   Columns: {len(table_info['columns'])}")
        if 'relationships' in table_info:
            print(f"   Relationships: {len(table_info['relationships'])}")
        print()
    
    print("DATA SOURCES:")
    print("-" * 40)
    for source, tables in DATABASE_SCHEMA['data_sources'].items():
        print(f"📄 {source}")
        for table in tables:
            print(f"   • {table}")
        print()

if __name__ == "__main__":
    print_schema_summary()
