from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound, Conflict
import logging
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

class UserService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self):
        try:
            users = self.user_repository.get_all()
            return [user.as_dict() for user in users]
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            raise BadRequest(f"Error retrieving users: {str(e)}")

    def get_user_by_id(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFound(f"User with ID {user_id} not found")
        return user.as_dict()

    def create_user(self, username, email, password, role='customer', phone=None, address=None, created_by=None):
        user = User(username, email, password, role, phone, address, created_by)
        new_user = self.user_repository.create(user)
        return new_user.as_dict()

    def update_user(self, user_id, **kwargs):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFound(f"User with ID {user_id} not found")
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.user_repository.update()
        return user.as_dict()

    def delete_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFound(f"User with ID {user_id} not found")
        self.user_repository.delete(user)
        return {"message": f"User with ID {user_id} deleted"}
