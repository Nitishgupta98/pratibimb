"""
Database Test Script
This script runs comprehensive tests to verify the database integrity and content
"""

import os
import sqlite3
from database_utils import DatabaseManager, get_database_stats

def test_database_structure():
    """Test if all tables exist and have the expected structure"""
    print("🔍 Testing database structure...")
    
    db = DatabaseManager()
    
    # Expected tables
    expected_tables = [
        'users', 'categories', 'carousel_slides', 'product_categories', 
        'products', 'product_features', 'community_features', 'diy_projects',
        'diy_project_steps', 'forum_categories', 'forum_posts', 'forum_replies',
        'learning_tools', 'learning_content', 'recent_activities', 'latest_updates',
        'quick_links', 'site_settings'
    ]
    
    # Get actual tables
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    actual_tables = [row['name'] for row in db.execute_query(query)]
    
    # Check if all expected tables exist
    missing_tables = set(expected_tables) - set(actual_tables)
    if missing_tables:
        print(f"❌ Missing tables: {missing_tables}")
        return False
    
    print(f"✅ All {len(expected_tables)} tables exist")
    return True

def test_sample_data():
    """Test if sample data was inserted correctly"""
    print("\n📊 Testing sample data...")
    
    db = DatabaseManager()
    stats = get_database_stats()
    
    # Expected minimum record counts
    expected_counts = {
        'users': 10,  # At least 10 users
        'carousel_slides': 5,  # 5 news slides
        'products': 6,  # 6 products
        'product_categories': 6,  # 6 categories
        'forum_posts': 4,  # 4 forum posts
        'learning_tools': 6,  # 6 learning tools
        'quick_links': 7,  # 7 quick links
        'recent_activities': 6,  # 6 activities
        'latest_updates': 4,  # 4 updates
    }
    
    success = True
    for table, expected_min in expected_counts.items():
        actual = stats.get(table, 0)
        if actual < expected_min:
            print(f"❌ {table}: expected ≥{expected_min}, got {actual}")
            success = False
        else:
            print(f"✅ {table}: {actual} records")
    
    return success

def test_data_relationships():
    """Test foreign key relationships"""
    print("\n🔗 Testing data relationships...")
    
    db = DatabaseManager()
    
    # Test product-category relationships
    products_with_categories = db.execute_query("""
        SELECT p.title, pc.name as category_name
        FROM products p
        JOIN product_categories pc ON p.category_id = pc.id
        LIMIT 3
    """)
    
    if len(products_with_categories) < 3:
        print("❌ Product-category relationships not working")
        return False
    
    print(f"✅ Product-category relationships: {len(products_with_categories)} verified")
    
    # Test forum post-user relationships
    posts_with_authors = db.execute_query("""
        SELECT fp.title, u.username
        FROM forum_posts fp
        JOIN users u ON fp.author_id = u.id
        LIMIT 3
    """)
    
    if len(posts_with_authors) < 3:
        print("❌ Forum post-user relationships not working")
        return False
    
    print(f"✅ Forum post-user relationships: {len(posts_with_authors)} verified")
    
    return True

def test_ui_content_mapping():
    """Test if UI content is properly mapped to database"""
    print("\n🎨 Testing UI content mapping...")
    
    db = DatabaseManager()
    
    # Test carousel content from index.html
    slides = db.get_carousel_slides()
    expected_slide_titles = [
        "Revolutionary AI-Powered Braille Display Launched",
        "Delhi Accessibility Summit 2025 - Register Now!",
        "Microsoft Releases Enhanced Screen Reader with GPT Integration"
    ]
    
    slide_titles = [slide['title'] for slide in slides]
    
    for expected_title in expected_slide_titles:
        if expected_title not in slide_titles:
            print(f"❌ Missing carousel slide: {expected_title}")
            return False
    
    print(f"✅ Carousel content mapped: {len(slides)} slides")
    
    # Test forum posts from index.html
    posts = db.get_forum_posts()
    expected_post_titles = [
        "How to optimize Braille art for different embosser models?",
        "Image preprocessing best practices for tactile graphics"
    ]
    
    post_titles = [post['title'] for post in posts]
    
    for expected_title in expected_post_titles:
        if expected_title not in post_titles:
            print(f"❌ Missing forum post: {expected_title}")
            return False
    
    print(f"✅ Forum content mapped: {len(posts)} posts")
    
    # Test marketplace products
    products = db.get_products()
    expected_product_titles = [
        "BraaS - Braille as a Service",
        "Advanced Screen Reader Pro",
        "Smart Braille Display 40-Cell"
    ]
    
    product_titles = [product['title'] for product in products]
    
    for expected_title in expected_product_titles:
        if expected_title not in product_titles:
            print(f"❌ Missing product: {expected_title}")
            return False
    
    print(f"✅ Marketplace content mapped: {len(products)} products")
    
    return True

def test_query_performance():
    """Test query performance and functionality"""
    print("\n⚡ Testing query performance...")
    
    db = DatabaseManager()
    
    # Test complex queries
    try:
        # Test featured products query
        featured_products = db.get_products(featured_only=True)
        print(f"✅ Featured products query: {len(featured_products)} results")
        
        # Test forum posts with categories
        posts_with_cats = db.get_forum_posts()
        print(f"✅ Forum posts with categories: {len(posts_with_cats)} results")
        
        # Test recent activities
        activities = db.get_recent_activities(limit=5)
        print(f"✅ Recent activities query: {len(activities)} results")
        
        # Test site settings
        settings = db.get_site_settings()
        print(f"✅ Site settings query: {len(settings)} settings")
        
        return True
        
    except Exception as e:
        print(f"❌ Query error: {str(e)}")
        return False

def run_all_tests():
    """Run all database tests"""
    print("🚀 Starting Pratibimb Database Tests")
    print("=" * 50)
    
    tests = [
        ("Database Structure", test_database_structure),
        ("Sample Data", test_sample_data),
        ("Data Relationships", test_data_relationships),
        ("UI Content Mapping", test_ui_content_mapping),
        ("Query Performance", test_query_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📋 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Database is ready for FastAPI integration.")
    else:
        print("⚠️  Some tests failed. Please review the database setup.")
    
    return passed == total

if __name__ == "__main__":
    # Check if database exists
    db_path = os.path.join(os.path.dirname(__file__), 'pratibimb.db')
    if not os.path.exists(db_path):
        print("❌ Database not found. Run create_database.py first.")
        exit(1)
    
    # Run tests
    success = run_all_tests()
    exit(0 if success else 1)
