from sqlalchemy.orm import Session
from auth_app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, username: str, password_hash: str, is_admin: bool = False) -> User:
        user = User(username=username, password_hash=password_hash, is_admin=is_admin)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user