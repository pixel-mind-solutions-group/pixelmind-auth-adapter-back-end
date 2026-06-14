from models.module_has_api_permission.module_has_api_permission import (
    ModuleHasApiPermission,
)
from models.module.module import Module


class ModuleHasApiPermissionRepository:

    def create(self, db, mapping) -> ModuleHasApiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_by_id(self, db, mapping_id: int):
        return (
            db.query(ModuleHasApiPermission)
            .filter(ModuleHasApiPermission.id == mapping_id)
            .first()
        )

    def find_by_module_and_permission(
        self, db, module_id: int, api_permission_id: int
    ):
        return (
            db.query(ModuleHasApiPermission)
            .filter(
                ModuleHasApiPermission.moduleId == module_id,
                ModuleHasApiPermission.apiPermissionId == api_permission_id,
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
        module_id: int = None,
        api_permission_name: str = None,
    ):
        from models.api_permission.api_permission import ApiPermission

        query = db.query(ModuleHasApiPermission)

        if realm_id is not None or application_id is not None:
            query = query.join(Module)
            if realm_id is not None:
                query = query.filter(Module.realmId == realm_id)
            if application_id is not None:
                query = query.filter(Module.applicationId == application_id)

        if module_id is not None:
            query = query.filter(
                ModuleHasApiPermission.moduleId == module_id
            )
        if api_permission_name:
            query = query.join(ApiPermission).filter(
                ApiPermission.apiPermissionName.ilike(f"%{api_permission_name}%")
            )

        return query.order_by(ModuleHasApiPermission.id.desc()).all()
