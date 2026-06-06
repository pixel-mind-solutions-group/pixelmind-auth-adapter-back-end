import math
from sqlalchemy import func, or_
from models.api_permission.api_permission import ApiPermission


class ApiPermissionRepository:

    def create(self, db, perm) -> ApiPermission:
        db.add(perm)
        db.commit()
        db.refresh(perm)
        return perm

    def search(
        self,
        db,
        page: int,
        size: int,
        query: str = None,
        active: bool = None,
    ):
        base_query = db.query(ApiPermission)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    ApiPermission.apiPermissionName.ilike(pattern),
                    ApiPermission.description.ilike(pattern),
                )
            )

        if active is not None:
            base_query = base_query.filter(ApiPermission.active == active)

        total = base_query.with_entities(func.count(ApiPermission.id)).scalar() or 0

        perms = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return perms, total_pages, total

    def find_by_id(self, db, perm_id: int):
        return db.query(ApiPermission).filter(ApiPermission.id == perm_id).first()

    def get_all_active_permissions(self, db):
        return (
            db.query(ApiPermission)
            .filter(ApiPermission.active == True)
            .order_by(ApiPermission.id.desc())
            .all()
        )

    def find_by_name(self, db, name: str):
        return (
            db.query(ApiPermission)
            .filter(ApiPermission.apiPermissionName == name)
            .first()
        )

    def delete(self, db, perm):
        db.delete(perm)
        db.commit()
        return True
