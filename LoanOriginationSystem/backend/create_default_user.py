from utils.db import get_db

def create_default_user():
    """Create default user if it doesn't exist."""
    db = get_db()
    
    # Check if user already exists
    user = db.users.find_one({'username': 'user1'})
    
    if not user:
        # Create default user
        user_data = {
            'username': 'user1',
            'password': 'test123',  # In a real app, hash the password
            'firstName': 'Default',
            'lastName': 'User',
            'email': 'user1@example.com',
            'role': 'Sales'
        }
        
        # Insert the user into the database
        result = db.users.insert_one(user_data)
        print(f"Created default user with ID: {result.inserted_id}")
    else:
        print("Default user already exists")

if __name__ == '__main__':
    create_default_user()