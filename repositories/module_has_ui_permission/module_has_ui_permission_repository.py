from models.module_has_ui_permission.module_has_ui_permission import (
    ModuleHasUiPermission,
)
from models.module.module import Module


class ModuleHasUiPermissionRepository:

    def create(self, db, mapping) -> ModuleHasUiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_by_id(self, db, mapping_id: int):
        return (
            db.query(ModuleHasUiPermission)
            .filter(ModuleHasUiPermission.id == mapping_id)
            .first()
        )

    def find_by_module_and_permission(self, db, module_id: int, ui_permission_id: int):
        return (
            db.query(ModuleHasUiPermission)
            .filter(
                ModuleHasUiPermission.moduleId == module_id,
                ModuleHasUiPermission.uiPermissionId == ui_permission_id,
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
        query_str: str = None,
    ):
        from models.ui_permission.ui_permission import UiPermission

        db_query = db.query(ModuleHasUiPermission)

        if realm_id is not None or application_id is not None or module_id is not None:
            db_query = db_query.join(Module)
            if realm_id is not None:
                db_query = db_query.filter(Module.realmId == realm_id)
            if application_id is not None:
                db_query = db_query.filter(Module.applicationId == application_id)
            if module_id is not None:
                db_query = db_query.filter(Module.id == module_id)
        if query_str:
            db_query = db_query.join(UiPermission).filter(
                UiPermission.uiPermissionName.ilike(f"%{query_str}%")
            )

        return db_query.order_by(ModuleHasUiPermission.id.desc()).all()
