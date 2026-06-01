import math

from sqlalchemy import func, or_

from models.user.user import User


class UserRepository:

    def create(self, db, user) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def search(self, db, page: int, size: int, query: str):
        pattern = f"%{query}%" if query else "%"

        base_query = db.query(User).filter(
            or_(
                User.email.ilike(pattern),
                User.firstName.ilike(pattern),
                User.lastName.ilike(pattern),
                User.username.ilike(pattern),
            )
        )

        total = base_query.with_entities(func.count(User.id)).scalar()

        users = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size)

        return users, total_pages, total

    def find_by_id(self, db, user_id):
        return db.query(User).filter(User.id == user_id).first()
