"""
Database Management CLI Tool
This script provides command-line utilities for managing the Pratibimb database
"""

import argparse
import os
import json
from datetime import datetime
from database_utils import DatabaseManager, get_database_stats, export_data_to_json

def create_database():
    """Create fresh database with sample data"""
    print("🚀 Creating new database...")
    
    # Import and run create_database module
    import create_database as db_creator
    db_creator.main()
    
    print("✅ Database created successfully!")

def show_stats():
    """Show database statistics"""
    print("📊 Database Statistics")
    print("=" * 40)
    
    stats = get_database_stats()
    total_records = sum(stats.values())
    
    for table, count in sorted(stats.items()):
        percentage = (count / total_records * 100) if total_records > 0 else 0
        print(f"{table:<20} {count:>6} records ({percentage:>5.1f}%)")
    
    print("-" * 40)
    print(f"{'TOTAL':<20} {total_records:>6} records")

def export_data(output_file=None):
    """Export database to JSON"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"pratibimb_export_{timestamp}.json"
    
    print(f"📤 Exporting data to {output_file}...")
    
    exported_file = export_data_to_json(output_file)
    file_size = os.path.getsize(exported_file) / 1024  # KB
    
    print(f"✅ Export completed!")
    print(f"   File: {exported_file}")
    print(f"   Size: {file_size:.1f} KB")

def query_data(table, limit=10):
    """Query and display data from a specific table"""
    db = DatabaseManager()
    
    print(f"🔍 Querying {table} (limit: {limit})")
    print("=" * 60)
    
    # Define specific queries for each table
    queries = {
        'carousel_slides': lambda: db.get_carousel_slides(),
        'products': lambda: db.get_products(limit=limit),
        'forum_posts': lambda: db.get_forum_posts(limit=limit),
        'users': lambda: db.get_users(),
        'quick_links': lambda: db.get_quick_links(),
        'recent_activities': lambda: db.get_recent_activities(limit=limit),
        'latest_updates': lambda: db.get_latest_updates(limit=limit),
        'learning_tools': lambda: db.get_learning_tools(),
        'community_features': lambda: db.get_community_features(),
        'diy_projects': lambda: db.get_diy_projects(limit=limit)
    }
    
    if table in queries:
        try:
            results = queries[table]()
            
            if not results:
                print("No data found.")
                return
            
            # Display results
            for i, item in enumerate(results[:limit], 1):
                print(f"{i}. ", end="")
                
                # Show relevant fields based on table
                if table == 'carousel_slides':
                    print(f"{item['title']} ({item['slide_type']})")
                elif table == 'products':
                    print(f"{item['title']} - {item['currency']} {item['price']}")
                elif table == 'forum_posts':
                    print(f"{item['title']} by @{item.get('author_username', 'unknown')}")
                elif table == 'users':
                    print(f"@{item['username']} ({item['full_name']}) - {item['role']}")
                elif table == 'quick_links':
                    print(f"{item['title']} → {item['link_url']}")
                elif table == 'recent_activities':
                    print(f"{item['title']} by @{item.get('username', 'system')}")
                elif table == 'latest_updates':
                    print(f"{item['title']} ({item['update_type']})")
                elif table == 'learning_tools':
                    print(f"{item['name']} ({item['tool_type']})")
                elif table == 'community_features':
                    print(f"{item['title']} - {item['action_type']}")
                elif table == 'diy_projects':
                    print(f"{item['title']} ({item['difficulty_level']})")
                else:
                    print(str(item))
                    
        except Exception as e:
            print(f"❌ Error querying {table}: {str(e)}")
    else:
        print(f"❌ Unknown table: {table}")
        print(f"Available tables: {', '.join(queries.keys())}")

def test_database():
    """Run database tests"""
    print("🧪 Running database tests...")
    
    # Import and run test module
    import test_database as db_tester
    
    success = db_tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed!")

def reset_database():
    """Reset database (delete and recreate)"""
    db_path = os.path.join(os.path.dirname(__file__), 'pratibimb.db')
    
    if os.path.exists(db_path):
        response = input("⚠️  This will delete all data! Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled.")
            return
        
        os.remove(db_path)
        print("🗑️  Old database deleted.")
    
    create_database()

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Pratibimb Database Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_db.py create          # Create new database
  python manage_db.py stats           # Show statistics
  python manage_db.py export          # Export to JSON
  python manage_db.py query products  # Query products table
  python manage_db.py test            # Run tests
  python manage_db.py reset           # Reset database
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    subparsers.add_parser('create', help='Create new database with sample data')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export database to JSON')
    export_parser.add_argument('-o', '--output', help='Output file name')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query specific table')
    query_parser.add_argument('table', help='Table name to query')
    query_parser.add_argument('-l', '--limit', type=int, default=10, help='Limit results (default: 10)')
    
    # Test command
    subparsers.add_parser('test', help='Run database tests')
    
    # Reset command
    subparsers.add_parser('reset', help='Reset database (delete and recreate)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if database exists for commands that need it
    db_path = os.path.join(os.path.dirname(__file__), 'pratibimb.db')
    commands_needing_db = ['stats', 'export', 'query', 'test']
    
    if args.command in commands_needing_db and not os.path.exists(db_path):
        print("❌ Database not found. Run 'create' command first.")
        return
    
    # Execute commands
    if args.command == 'create':
        create_database()
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'export':
        export_data(args.output)
    elif args.command == 'query':
        query_data(args.table, args.limit)
    elif args.command == 'test':
        test_database()
    elif args.command == 'reset':
        reset_database()

if __name__ == "__main__":
    main()
