from user_system import User, Admin

def verify_system():
    # 1. Create a list for users
    user_list = []
    print("--- User Management Verification ---\n")

    # 2. Create regular users
    user1 = User(1, "Alice")
    user2 = User(2, "Bob")
    print(f"Created users: {user1}, {user2}")

    # 3. Create an admin
    admin = Admin(99, "SuperAdmin")
    print(f"Created admin: {admin}")

    # 4. Admin adds users
    print("\n--- Testing Admin Add User ---")
    admin.add_user(user_list, user1)
    admin.add_user(user_list, user2)
    print(f"User list after adds: {user_list}")

    # 5. Admin removes a user
    print("\n--- Testing Admin Remove User ---")
    admin.remove_user(user_list, user1)
    print(f"User list after removal of Alice: {user_list}")

    # 6. Verify Access Levels and Encapsulation
    print("\n--- Testing Encapsulation and Access Levels ---")
    print(f"User1 ID (via getter): {user1.get_user_id()}")
    print(f"User1 Name (via getter): {user1.get_name()}")
    print(f"User1 Access Level: {user1.get_access_level()}")
    print(f"Admin Access Level: {admin.get_access_level()}")

    # Try setting name
    print(f"Old Name: {user2.get_name()}")
    user2.set_name("Bobby")
    print(f"New Name: {user2.get_name()}")

    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_system()
