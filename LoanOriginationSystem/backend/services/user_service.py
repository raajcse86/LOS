from models.user import User
from utils.db import get_db
from datetime import datetime
from bson.objectid import ObjectId

class UserService:
    def __init__(self):
        self.db = get_db()
        self.users_collection = self.db['users']
        
        # Ensure we have at least one user of each role at startup
        self._ensure_default_users()
    
    def get_all_users(self):
        """Get all users from database."""
        users = list(self.users_collection.find())
        # Convert ObjectId to string to make it JSON serializable
        for user in users:
            user['_id'] = str(user['_id'])
        return users
    
    def get_user_by_id(self, user_id):
        """Get a user by their ID."""
        try:
            user = self.users_collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    def get_users_by_role(self, role):
        """Get all users with a specific role."""
        try:
            users = list(self.users_collection.find({'role': role}))
            # Convert ObjectId to string to make it JSON serializable
            for user in users:
                user['_id'] = str(user['_id'])
            return users
        except Exception as e:
            print(f"Error fetching users by role: {e}")
            return []
    
    def create_user(self, user_data):
        """Create a new user."""
        try:
            # Add timestamps
            now = datetime.utcnow().isoformat()
            user_data['createdAt'] = now
            user_data['updatedAt'] = now
            
            # Insert into database
            result = self.users_collection.insert_one(user_data)
            
            # Return the created user with string ID
            created_user = self.get_user_by_id(result.inserted_id)
            return created_user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user(self, user_id, user_data):
        """Update a user."""
        try:
            # Update timestamp
            now = datetime.utcnow().isoformat()
            user_data['updatedAt'] = now
            
            # Remove _id if present
            if '_id' in user_data:
                del user_data['_id']
            
            # Update in database
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': user_data}
            )
            
            if result.modified_count > 0:
                return self.get_user_by_id(user_id)
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    def delete_user(self, user_id):
        """Delete a user."""
        try:
            result = self.users_collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def _ensure_default_users(self):
        """Create default users for each role if they don't exist."""
        roles = ['Sales', 'Processor', 'Underwriter', 'Closer', 'Manager']
        
        for role in roles:
            # Check if we have a user with this role
            existing_user = self.users_collection.find_one({'role': role})
            if not existing_user:
                # Create a default user for this role
                user_data = {
                    'username': role.lower(),
                    'firstName': role,
                    'lastName': 'User',
                    'email': f"{role.lower()}@loanorigination.com",
                    'role': role
                }
                self.create_user(user_data)
                print(f"Created default {role} user")
