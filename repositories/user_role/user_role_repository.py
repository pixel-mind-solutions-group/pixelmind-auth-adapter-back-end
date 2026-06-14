import math
from sqlalchemy import func, or_
from models.user_role.user_role import UserRole


class UserRoleRepository:

    def create(self, db, role) -> UserRole:
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def find_by_id(self, db, role_id: int):
        return db.query(UserRole).filter(UserRole.id == role_id).first()

    def find_by_name_realm_app(self, db, name: str, realm_id: int, application_id: int):
        return (
            db.query(UserRole)
            .filter(
                UserRole.roleName == name,
                UserRole.realmId == realm_id,
                UserRole.applicationId == application_id,
            )
            .first()
        )

    def delete(self, db, role):
        db.delete(role)
        db.commit()
        return True

    def search(
        self,
        db,
        page: int,
        size: int,
        query: str = None,
        active: bool = None,
        realm_id: int = None,
        application_id: int = None,
    ):
        base_query = db.query(UserRole)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    UserRole.roleName.ilike(pattern),
                    UserRole.description.ilike(pattern)
                )
            )

        if active is not None:
            base_query = base_query.filter(UserRole.active == active)

        if realm_id is not None:
            base_query = base_query.filter(UserRole.realmId == realm_id)

        if application_id is not None:
            base_query = base_query.filter(UserRole.applicationId == application_id)

        total = base_query.with_entities(func.count(UserRole.id)).scalar() or 0
        roles = base_query.order_by(UserRole.id.desc()).offset(page * size).limit(size).all()
        total_pages = math.ceil(total / size) if size > 0 else 1

        return roles, total_pages, total

    def get_all_active(self, db, realm_id: int = None, application_id: int = None):
        query = db.query(UserRole).filter(UserRole.active == True)
        if realm_id is not None:
            query = query.filter(UserRole.realmId == realm_id)
        if application_id is not None:
            query = query.filter(UserRole.applicationId == application_id)
        return query.order_by(UserRole.roleName.asc()).all()
