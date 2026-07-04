import math
from sqlalchemy import func, or_
from models.ui_permission.ui_permission import UiPermission


class UiPermissionRepository:

    def create(self, db, perm) -> UiPermission:
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
        base_query = db.query(UiPermission)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    UiPermission.uiPermissionName.ilike(pattern),
                    UiPermission.description.ilike(pattern),
                )
            )

        if active is not None:
            base_query = base_query.filter(UiPermission.active == active)

        total = base_query.with_entities(func.count(UiPermission.id)).scalar() or 0

        perms = base_query.order_by(UiPermission.id.desc()).offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return perms, total_pages, total

    def find_by_id(self, db, perm_id: int):
        return db.query(UiPermission).filter(UiPermission.id == perm_id).first()

    def get_all_active_permissions(
        self, db, realm_id: int, application_id: int, ui_permission_name: str = None
    ):
        from models.application_has_ui_permission.application_has_ui_permission import (
            ApplicationHasUiPermission,
        )

        assigned_query = db.query(ApplicationHasUiPermission.uiPermissionId).filter(
            ApplicationHasUiPermission.realmId == realm_id,
            ApplicationHasUiPermission.applicationId == application_id,
        )

        query = db.query(UiPermission).filter(
            UiPermission.active == True,
            ~UiPermission.id.in_(assigned_query),
        )

        if ui_permission_name:
            query = query.filter(UiPermission.uiPermissionName == ui_permission_name)

        return query.order_by(UiPermission.id.desc()).all()

    def find_by_name(self, db, name: str):
        return (
            db.query(UiPermission)
            .filter(UiPermission.uiPermissionName == name)
            .first()
        )

    def delete(self, db, perm):
        db.delete(perm)
        db.commit()
        return True
