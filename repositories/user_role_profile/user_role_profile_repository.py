from models.user_role_has_modules_has_api_permission.user_role_has_modules_has_api_permission import UserRoleHasModulesHasApiPermission
from models.user_role_has_modules_has_ui_permission.user_role_has_modules_has_ui_permission import UserRoleHasModulesHasUiPermission


class UserRoleProfileRepository:

    # --- API Permission Mapping Repository Methods ---

    def create_api(self, db, mapping) -> UserRoleHasModulesHasApiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_api_by_id(self, db, mapping_id: int) -> UserRoleHasModulesHasApiPermission:
        return (
            db.query(UserRoleHasModulesHasApiPermission)
            .filter(UserRoleHasModulesHasApiPermission.id == mapping_id)
            .first()
        )

    def find_api_by_composite(
        self,
        db,
        realm_id: int,
        application_id: int,
        role_id: int,
        module_id: int = None,
        api_permission_id: int = None,
    ) -> UserRoleHasModulesHasApiPermission:
        return (
            db.query(UserRoleHasModulesHasApiPermission)
            .filter(
                UserRoleHasModulesHasApiPermission.realmId == realm_id,
                UserRoleHasModulesHasApiPermission.applicationId == application_id,
                UserRoleHasModulesHasApiPermission.userRoleId == role_id,
                UserRoleHasModulesHasApiPermission.moduleId == module_id,
                UserRoleHasModulesHasApiPermission.apiPermissionId == api_permission_id,
            )
            .first()
        )

    def delete_api(self, db, mapping) -> bool:
        db.delete(mapping)
        db.commit()
        return True

    def search_api_assigned(self, db, realm_id: int = None, application_id: int = None, user_role_id: int = None, module_id: int = None) -> list[UserRoleHasModulesHasApiPermission]:
        query = db.query(UserRoleHasModulesHasApiPermission)
        if realm_id is not None:
            query = query.filter(UserRoleHasModulesHasApiPermission.realmId == realm_id)
        if application_id is not None:
            query = query.filter(UserRoleHasModulesHasApiPermission.applicationId == application_id)
        if user_role_id is not None:
            query = query.filter(UserRoleHasModulesHasApiPermission.userRoleId == user_role_id)
        if module_id is not None:
            if module_id == 0:
                query = query.filter(UserRoleHasModulesHasApiPermission.moduleId.is_(None))
            else:
                query = query.filter(UserRoleHasModulesHasApiPermission.moduleId == module_id)
        return query.order_by(UserRoleHasModulesHasApiPermission.id.desc()).all()

    # --- UI Permission Mapping Repository Methods ---

    def create_ui(self, db, mapping) -> UserRoleHasModulesHasUiPermission:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_ui_by_id(self, db, mapping_id: int) -> UserRoleHasModulesHasUiPermission:
        return (
            db.query(UserRoleHasModulesHasUiPermission)
            .filter(UserRoleHasModulesHasUiPermission.id == mapping_id)
            .first()
        )

    def find_ui_by_composite(
        self,
        db,
        realm_id: int,
        application_id: int,
        role_id: int,
        module_id: int = None,
        ui_permission_id: int = None,
    ) -> UserRoleHasModulesHasUiPermission:
        return (
            db.query(UserRoleHasModulesHasUiPermission)
            .filter(
                UserRoleHasModulesHasUiPermission.realmId == realm_id,
                UserRoleHasModulesHasUiPermission.applicationId == application_id,
                UserRoleHasModulesHasUiPermission.userRoleId == role_id,
                UserRoleHasModulesHasUiPermission.moduleId == module_id,
                UserRoleHasModulesHasUiPermission.uiPermissionId == ui_permission_id,
            )
            .first()
        )

    def delete_ui(self, db, mapping) -> bool:
        db.delete(mapping)
        db.commit()
        return True

    def search_ui_assigned(self, db, realm_id: int = None, application_id: int = None, user_role_id: int = None, module_id: int = None) -> list[UserRoleHasModulesHasUiPermission]:
        query = db.query(UserRoleHasModulesHasUiPermission)
        if realm_id is not None:
            query = query.filter(UserRoleHasModulesHasUiPermission.realmId == realm_id)
        if application_id is not None:
            query = query.filter(UserRoleHasModulesHasUiPermission.applicationId == application_id)
        if user_role_id is not None:
            query = query.filter(UserRoleHasModulesHasUiPermission.userRoleId == user_role_id)
        if module_id is not None:
            if module_id == 0:
                query = query.filter(UserRoleHasModulesHasUiPermission.moduleId.is_(None))
            else:
                query = query.filter(UserRoleHasModulesHasUiPermission.moduleId == module_id)
        return query.order_by(UserRoleHasModulesHasUiPermission.id.desc()).all()

    def delete_all_by_role(self, db, realm_id: int, application_id: int, role_id: int) -> None:
        db.query(UserRoleHasModulesHasApiPermission).filter(
            UserRoleHasModulesHasApiPermission.realmId == realm_id,
            UserRoleHasModulesHasApiPermission.applicationId == application_id,
            UserRoleHasModulesHasApiPermission.userRoleId == role_id
        ).delete(synchronize_session=False)

        db.query(UserRoleHasModulesHasUiPermission).filter(
            UserRoleHasModulesHasUiPermission.realmId == realm_id,
            UserRoleHasModulesHasUiPermission.applicationId == application_id,
            UserRoleHasModulesHasUiPermission.userRoleId == role_id
        ).delete(synchronize_session=False)
        db.commit()
