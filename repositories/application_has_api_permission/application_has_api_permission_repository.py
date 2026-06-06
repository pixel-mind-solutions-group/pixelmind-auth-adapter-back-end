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
