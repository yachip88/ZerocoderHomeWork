class User:
    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name
        self._access_level = 'user'

    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def get_access_level(self):
        return self._access_level

    def __repr__(self):
        return f"User(id={self._user_id}, name='{self._name}', access='{self._access_level}')"


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self._access_level = 'admin'

    def add_user(self, user_list, user):
        if not isinstance(user, User):
            print("Error: Can only add User instances.")
            return
        user_list.append(user)
        print(f"User {user.get_name()} added successfully.")

    def remove_user(self, user_list, user):
        if user in user_list:
            user_list.remove(user)
            print(f"User {user.get_name()} removed successfully.")
        else:
            print(f"Error: User {user.get_name()} not found in the list.")

    def __repr__(self):
        return f"Admin(id={self._user_id}, name='{self._name}', access='{self._access_level}')"
