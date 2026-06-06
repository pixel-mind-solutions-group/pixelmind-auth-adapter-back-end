from models.application_has_api_permission.application_has_api_permission import (
    ApplicationHasApiPermission,
)


class ApplicationHasApiPermissionRepository:

    def create(self, db, mapping) -> ApplicationHasApiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_by_id(self, db, mapping_id: int):
        return (
            db.query(ApplicationHasApiPermission)
            .filter(ApplicationHasApiPermission.id == mapping_id)
            .first()
        )

    def find_by_realm_app_and_permission(
        self, db, realm_id: int, application_id: int, api_permission_id: int
    ):
        return (
            db.query(ApplicationHasApiPermission)
            .filter(
                ApplicationHasApiPermission.realmId == realm_id,
                ApplicationHasApiPermission.applicationId == application_id,
                ApplicationHasApiPermission.apiPermissionId == api_permission_id,
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
        api_permission_name: str = None,
    ):
        from models.api_permission.api_permission import ApiPermission

        query = db.query(ApplicationHasApiPermission)

        if realm_id is not None:
            query = query.filter(ApplicationHasApiPermission.realmId == realm_id)
        if application_id is not None:
            query = query.filter(
                ApplicationHasApiPermission.applicationId == application_id
            )
        if api_permission_name:
            query = query.join(ApiPermission).filter(
                ApiPermission.apiPermissionName.ilike(f"%{api_permission_name}%")
            )

        return query.order_by(ApplicationHasApiPermission.id.desc()).all()
