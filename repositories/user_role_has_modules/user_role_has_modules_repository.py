from models.user_role_has_modules.user_role_has_modules import UserRoleHasModules


class UserRoleHasModulesRepository:

    def create(self, db, mapping) -> UserRoleHasModules:
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        return mapping

    def find_by_id(self, db, mapping_id: int):
        return db.query(UserRoleHasModules).filter(UserRoleHasModules.id == mapping_id).first()

    def find_by_realm_app_role_and_module(
        self, db, realm_id: int, application_id: int, role_id: int, module_id: int = None
    ):
        return (
            db.query(UserRoleHasModules)
            .filter(
                UserRoleHasModules.realmId == realm_id,
                UserRoleHasModules.applicationId == application_id,
                UserRoleHasModules.userRoleId == role_id,
                UserRoleHasModules.moduleId == module_id,
            )
            .first()
        )

    def delete(self, db, mapping):
        db.delete(mapping)
        db.commit()
        return True

    def search_assigned(self, db, realm_id: int = None, application_id: int = None):
        query = db.query(UserRoleHasModules)

        if realm_id is not None:
            query = query.filter(UserRoleHasModules.realmId == realm_id)
        if application_id is not None:
            query = query.filter(UserRoleHasModules.applicationId == application_id)

        return query.order_by(UserRoleHasModules.id.desc()).all()
