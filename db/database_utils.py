"""
Database Query Utilities and Data Access Layer
This file provides utility functions for querying and manipulating the Pratibimb database
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import os

# Get database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'pratibimb.db')

class DatabaseManager:
    """Database manager class for handling all database operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    # ==========================================
    # CAROUSEL / NEWS QUERIES
    # ==========================================
    
    def get_carousel_slides(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get carousel slides for homepage"""
        query = """
        SELECT * FROM carousel_slides 
        WHERE is_active = 1 
        ORDER BY sort_order ASC, created_at DESC
        """ if active_only else """
        SELECT * FROM carousel_slides 
        ORDER BY sort_order ASC, created_at DESC
        """
        return self.execute_query(query)
    
    # ==========================================
    # MARKETPLACE QUERIES
    # ==========================================
    
    def get_product_categories(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all product categories"""
        query = """
        SELECT * FROM product_categories 
        WHERE is_active = 1 
        ORDER BY sort_order ASC, name ASC
        """ if active_only else """
        SELECT * FROM product_categories 
        ORDER BY sort_order ASC, name ASC
        """
        return self.execute_query(query)
    
    def get_products(self, 
                    category_id: Optional[int] = None, 
                    featured_only: bool = False,
                    active_only: bool = True,
                    limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get products with optional filtering"""
        conditions = []
        params = []
        
        if active_only:
            conditions.append("p.is_active = 1")
        
        if featured_only:
            conditions.append("p.is_featured = 1")
        
        if category_id:
            conditions.append("p.category_id = ?")
            params.append(category_id)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        query = f"""
        SELECT p.*, pc.name as category_name, pc.slug as category_slug
        FROM products p
        LEFT JOIN product_categories pc ON p.category_id = pc.id
        {where_clause}
        ORDER BY p.is_featured DESC, p.rating DESC, p.created_at DESC
        {limit_clause}
        """
        
        return self.execute_query(query, tuple(params))
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get single product with category info"""
        query = """
        SELECT p.*, pc.name as category_name, pc.slug as category_slug
        FROM products p
        LEFT JOIN product_categories pc ON p.category_id = pc.id
        WHERE p.id = ?
        """
        results = self.execute_query(query, (product_id,))
        return results[0] if results else None
    
    def get_product_features(self, product_id: int) -> List[Dict[str, Any]]:
        """Get features for a specific product"""
        query = """
        SELECT * FROM product_features 
        WHERE product_id = ? 
        ORDER BY sort_order ASC
        """
        return self.execute_query(query, (product_id,))
    
    # ==========================================
    # FORUM QUERIES
    # ==========================================
    
    def get_forum_posts(self, 
                       category_id: Optional[int] = None,
                       post_type: Optional[str] = None,
                       answered_only: bool = False,
                       limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get forum posts with author and category info"""
        conditions = []
        params = []
        
        if category_id:
            conditions.append("fp.category_id = ?")
            params.append(category_id)
        
        if post_type:
            conditions.append("fp.post_type = ?")
            params.append(post_type)
        
        if answered_only:
            conditions.append("fp.is_answered = 1")
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        query = f"""
        SELECT fp.*, u.username as author_username, u.full_name as author_name,
               fc.name as category_name
        FROM forum_posts fp
        LEFT JOIN users u ON fp.author_id = u.id
        LEFT JOIN forum_categories fc ON fp.category_id = fc.id
        {where_clause}
        ORDER BY fp.is_pinned DESC, fp.created_at DESC
        {limit_clause}
        """
        
        return self.execute_query(query, tuple(params))
    
    def get_forum_categories(self) -> List[Dict[str, Any]]:
        """Get all forum categories"""
        query = """
        SELECT * FROM forum_categories 
        WHERE is_active = 1 
        ORDER BY sort_order ASC, name ASC
        """
        return self.execute_query(query)
    
    # ==========================================
    # COMMUNITY QUERIES
    # ==========================================
    
    def get_community_features(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get community features"""
        query = """
        SELECT * FROM community_features 
        WHERE is_active = 1 
        ORDER BY sort_order ASC
        """ if active_only else """
        SELECT * FROM community_features 
        ORDER BY sort_order ASC
        """
        return self.execute_query(query)
    
    def get_diy_projects(self, featured_only: bool = False, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get DIY projects with author info"""
        conditions = ["dp.is_active = 1"]
        
        if featured_only:
            conditions.append("dp.is_featured = 1")
        
        where_clause = "WHERE " + " AND ".join(conditions)
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        query = f"""
        SELECT dp.*, u.username as author_username, u.full_name as author_name
        FROM diy_projects dp
        LEFT JOIN users u ON dp.author_id = u.id
        {where_clause}
        ORDER BY dp.is_featured DESC, dp.created_at DESC
        {limit_clause}
        """
        
        return self.execute_query(query)
    
    # ==========================================
    # LEARNING CENTER QUERIES
    # ==========================================
    
    def get_learning_tools(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get learning tools"""
        query = """
        SELECT * FROM learning_tools 
        WHERE is_active = 1 
        ORDER BY sort_order ASC, name ASC
        """ if active_only else """
        SELECT * FROM learning_tools 
        ORDER BY sort_order ASC, name ASC
        """
        return self.execute_query(query)
    
    def get_learning_tool_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get learning tool by slug"""
        query = "SELECT * FROM learning_tools WHERE slug = ? AND is_active = 1"
        results = self.execute_query(query, (slug,))
        return results[0] if results else None
    
    # ==========================================
    # ACTIVITY & UPDATES QUERIES
    # ==========================================
    
    def get_recent_activities(self, 
                             user_id: Optional[int] = None,
                             public_only: bool = True,
                             limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities with user info"""
        conditions = []
        params = []
        
        if public_only:
            conditions.append("ra.is_public = 1")
        
        if user_id:
            conditions.append("ra.user_id = ?")
            params.append(user_id)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
        SELECT ra.*, u.username, u.full_name
        FROM recent_activities ra
        LEFT JOIN users u ON ra.user_id = u.id
        {where_clause}
        ORDER BY ra.created_at DESC
        LIMIT {limit}
        """
        
        return self.execute_query(query, tuple(params))
    
    def get_latest_updates(self, featured_only: bool = False, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest platform updates"""
        conditions = []
        
        if featured_only:
            conditions.append("is_featured = 1")
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
        SELECT * FROM latest_updates 
        {where_clause}
        ORDER BY publish_date DESC, created_at DESC
        LIMIT {limit}
        """
        
        return self.execute_query(query)
    
    # ==========================================
    # NAVIGATION QUERIES
    # ==========================================
    
    def get_quick_links(self, category: Optional[str] = None, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get quick navigation links"""
        conditions = []
        params = []
        
        if active_only:
            conditions.append("is_active = 1")
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
        SELECT * FROM quick_links 
        {where_clause}
        ORDER BY sort_order ASC, title ASC
        """
        
        return self.execute_query(query, tuple(params))
    
    # ==========================================
    # USER QUERIES
    # ==========================================
    
    def get_users(self, role: Optional[str] = None, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get users with optional role filtering"""
        conditions = []
        params = []
        
        if active_only:
            conditions.append("is_active = 1")
        
        if role:
            conditions.append("role = ?")
            params.append(role)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
        SELECT id, username, email, full_name, avatar_url, role, is_active, created_at
        FROM users 
        {where_clause}
        ORDER BY created_at DESC
        """
        
        return self.execute_query(query, tuple(params))
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = """
        SELECT id, username, email, full_name, avatar_url, role, is_active, created_at
        FROM users WHERE id = ?
        """
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    # ==========================================
    # SETTINGS QUERIES
    # ==========================================
    
    def get_site_settings(self, public_only: bool = True) -> Dict[str, Any]:
        """Get site settings as key-value pairs"""
        query = """
        SELECT setting_key, setting_value, setting_type 
        FROM site_settings
        WHERE is_public = 1
        """ if public_only else """
        SELECT setting_key, setting_value, setting_type 
        FROM site_settings
        """
        
        results = self.execute_query(query)
        settings = {}
        
        for row in results:
            key = row['setting_key']
            value = row['setting_value']
            setting_type = row['setting_type']
            
            # Convert value based on type
            if setting_type == 'boolean':
                settings[key] = value.lower() == 'true'
            elif setting_type == 'integer':
                settings[key] = int(value)
            elif setting_type == 'float':
                settings[key] = float(value)
            else:
                settings[key] = value
        
        return settings

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    db = DatabaseManager()
    
    tables = [
        'users', 'carousel_slides', 'products', 'product_categories',
        'forum_posts', 'forum_categories', 'community_features',
        'diy_projects', 'learning_tools', 'recent_activities',
        'latest_updates', 'quick_links', 'site_settings'
    ]
    
    stats = {}
    
    for table in tables:
        query = f"SELECT COUNT(*) as count FROM {table}"
        result = db.execute_query(query)
        stats[table] = result[0]['count'] if result else 0
    
    return stats

def export_data_to_json(output_file: str = None) -> str:
    """Export all data to JSON format"""
    db = DatabaseManager()
    
    if not output_file:
        output_file = os.path.join(os.path.dirname(__file__), 'pratibimb_data_export.json')
    
    data = {
        'exported_at': datetime.now().isoformat(),
        'carousel_slides': db.get_carousel_slides(active_only=False),
        'products': db.get_products(active_only=False),
        'product_categories': db.get_product_categories(active_only=False),
        'forum_posts': db.get_forum_posts(),
        'forum_categories': db.get_forum_categories(),
        'community_features': db.get_community_features(active_only=False),
        'diy_projects': db.get_diy_projects(),
        'learning_tools': db.get_learning_tools(active_only=False),
        'recent_activities': db.get_recent_activities(public_only=False, limit=100),
        'latest_updates': db.get_latest_updates(limit=100),
        'quick_links': db.get_quick_links(active_only=False),
        'users': db.get_users(active_only=False),
        'site_settings': db.get_site_settings(public_only=False)
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    return output_file

# ==========================================
# SAMPLE USAGE EXAMPLES
# ==========================================

def demo_queries():
    """Demonstrate various database queries"""
    db = DatabaseManager()
    
    print("🎠 CAROUSEL SLIDES:")
    slides = db.get_carousel_slides()
    for slide in slides[:2]:
        print(f"  • {slide['title']} ({slide['slide_type']})")
    
    print(f"\n🛒 FEATURED PRODUCTS:")
    products = db.get_products(featured_only=True, limit=3)
    for product in products:
        print(f"  • {product['title']} - {product['currency']} {product['price']}")
    
    print(f"\n💬 RECENT FORUM POSTS:")
    posts = db.get_forum_posts(limit=3)
    for post in posts:
        print(f"  • {post['title']} by @{post['author_username']}")
    
    print(f"\n🔗 QUICK LINKS:")
    links = db.get_quick_links()
    for link in links[:5]:
        print(f"  • {link['title']} ({link['category']})")
    
    print(f"\n📊 DATABASE STATISTICS:")
    stats = get_database_stats()
    for table, count in stats.items():
        print(f"  • {table}: {count} records")

if __name__ == "__main__":
    # Run demo if script is executed directly
    if os.path.exists(DB_PATH):
        demo_queries()
    else:
        print(f"❌ Database not found at {DB_PATH}")
        print("Run create_database.py first to create the database.")
