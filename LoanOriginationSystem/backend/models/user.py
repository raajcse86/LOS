class User:
    """
    User model representing the structure of user data.
    This is used for documentation and validation.
    """
    
    def __init__(
        self,
        username,
        first_name,
        last_name,
        email,
        role,
        created_at=None,
        updated_at=None
    ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "role": self.role,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user object from dictionary."""
        return cls(
            username=data.get("username"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("email"),
            role=data.get("role"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )
