from models.application_has_ui_permission.application_has_ui_permission import (
    ApplicationHasUiPermission,
)


class ApplicationHasUiPermissionRepository:

    def create(self, db, mapping) -> ApplicationHasUiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_by_id(self, db, mapping_id: int):
        return (
            db.query(ApplicationHasUiPermission)
            .filter(ApplicationHasUiPermission.id == mapping_id)
            .first()
        )

    def find_by_realm_app_and_permission(
        self, db, realm_id: int, application_id: int, ui_permission_id: int
    ):
        return (
            db.query(ApplicationHasUiPermission)
            .filter(
                ApplicationHasUiPermission.realmId == realm_id,
                ApplicationHasUiPermission.applicationId == application_id,
                ApplicationHasUiPermission.uiPermissionId == ui_permission_id,
            )
            .first()
        )

    def delete(self, db, mapping):
        db.delete(mapping)
        db.commit()
        return True

    def search_assigned(
        self,
        db,
        realm_id: int = None,
        application_id: int = None,
        ui_permission_name: str = None,
    ):
        from models.ui_permission.ui_permission import UiPermission

        query = db.query(ApplicationHasUiPermission)

        if realm_id is not None:
            query = query.filter(ApplicationHasUiPermission.realmId == realm_id)
        if application_id is not None:
            query = query.filter(
                ApplicationHasUiPermission.applicationId == application_id
            )
        if ui_permission_name:
            query = query.join(UiPermission).filter(
                UiPermission.uiPermissionName.ilike(f"%{ui_permission_name}%")
            )

        return query.order_by(ApplicationHasUiPermission.id.desc()).all()
