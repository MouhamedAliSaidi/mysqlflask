from datetime import datetime

class User:
    users = []
    id_counter = 1

    @classmethod
    def create(cls, first_name, last_name, email):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = {
            'id': cls.id_counter,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'created_at': created_at,
            'updated_at': None
        }
        cls.users.append(user)
        cls.id_counter += 1

    @classmethod
    def get_all(cls):
        return cls.users

    @classmethod
    def get_by_id(cls, user_id):
        return next((user for user in cls.users if user['id'] == user_id), None)

    @classmethod
    def update(cls, user_id, first_name, last_name, email):
        user = cls.get_by_id(user_id)
        if user:
            user['first_name'] = first_name
            user['last_name'] = last_name
            user['email'] = email
            user['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def delete(cls, user_id):
        cls.users = [user for user in cls.users if user['id'] != user_id]
