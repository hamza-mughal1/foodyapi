import enum

# Enum for User Types
class UserRole(enum.Enum):
    user = "user"
    vendor = "vendor"
    
# Enum for Order Progress Status
class OrderStatus(enum.Enum):
    in_progress = "in_progress"
    done = "done"
    
# Enum for Order Acceptance Status by Restaurant
class AcceptanceStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"