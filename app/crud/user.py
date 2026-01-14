from typing import Any
from sqlalchemy.orm import Session


from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate





class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Any:
        return db.query(self.model).filter(self.model.email == email).first()

user = CRUDUser(User)