from typing import Optional
from sqlalchemy.orm import Session
from models.realm.realm import Realm
from models.user_profile.user_profile import UserProfile
from models.user_role_has_modules_has_api_permission.user_role_has_modules_has_api_permission import (
    UserRoleHasModulesHasApiPermission,
)
from models.user_role_has_modules_has_ui_permission.user_role_has_modules_has_ui_permission import (
    UserRoleHasModulesHasUiPermission,
)
from models.user_role.user_role import UserRole
from models.application_has_api_permission.application_has_api_permission import (
    ApplicationHasApiPermission,
)
from models.application_has_ui_permission.application_has_ui_permission import (
    ApplicationHasUiPermission,
)
from models.module.module import Module
from models.module_has_api_permission.module_has_api_permission import (
    ModuleHasApiPermission,
)
from models.module_has_ui_permission.module_has_ui_permission import (
    ModuleHasUiPermission,
)
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from models.application.application import Application


class RealmRepository:

    def get_all_active_realms(self, db: Session, only_active: bool = True) -> list[Realm]:
        query = db.query(Realm)
        if only_active:
            query = query.filter(Realm.active == True)
        return query.order_by(Realm.id.desc()).all()

    def get_by_id(self, db: Session, realm_id: int) -> Optional[Realm]:
        return db.query(Realm).filter(Realm.id == realm_id).first()

    def delete_realm_and_related_data(self, db: Session, realm_id: int) -> None:
        # 1. Delete user profiles for this realm
        db.query(UserProfile).filter(UserProfile.realmId == realm_id).delete(
            synchronize_session=False
        )

        # 2. Delete user role module permissions for this realm
        db.query(UserRoleHasModulesHasApiPermission).filter(
            UserRoleHasModulesHasApiPermission.realmId == realm_id
        ).delete(synchronize_session=False)
        db.query(UserRoleHasModulesHasUiPermission).filter(
            UserRoleHasModulesHasUiPermission.realmId == realm_id
        ).delete(synchronize_session=False)

        # 3. Delete user roles for this realm
        db.query(UserRole).filter(UserRole.realmId == realm_id).delete(
            synchronize_session=False
        )

        # 4. Delete application permissions for this realm
        db.query(ApplicationHasApiPermission).filter(
            ApplicationHasApiPermission.realmId == realm_id
        ).delete(synchronize_session=False)
        db.query(ApplicationHasUiPermission).filter(
            ApplicationHasUiPermission.realmId == realm_id
        ).delete(synchronize_session=False)

        # 5. Delete module permissions for modules belonging to this realm
        module_ids = [
            m[0]
            for m in db.query(Module.id).filter(Module.realmId == realm_id).all()
        ]
        if module_ids:
            db.query(ModuleHasApiPermission).filter(
                ModuleHasApiPermission.moduleId.in_(module_ids)
            ).delete(synchronize_session=False)
            db.query(ModuleHasUiPermission).filter(
                ModuleHasUiPermission.moduleId.in_(module_ids)
            ).delete(synchronize_session=False)

        # 6. Delete modules for this realm
        db.query(Module).filter(Module.realmId == realm_id).delete(
            synchronize_session=False
        )

        # 7. Collect linked application IDs before deleting realms_has_applications
        app_ids = [
            r[0]
            for r in db.query(RealmsHasApplications.application_id)
            .filter(RealmsHasApplications.realm_id == realm_id)
            .all()
        ]

        # 8. Delete realms_has_applications mappings
        db.query(RealmsHasApplications).filter(
            RealmsHasApplications.realm_id == realm_id
        ).delete(synchronize_session=False)

        # 9. Delete realm itself
        db.query(Realm).filter(Realm.id == realm_id).delete(synchronize_session=False)

        # 10. Clean up orphaned applications that are no longer associated with any realm or other tables
        for app_id in app_ids:
            remaining_mappings = (
                db.query(RealmsHasApplications)
                .filter(RealmsHasApplications.application_id == app_id)
                .count()
            )
            if remaining_mappings == 0:
                in_modules = (
                    db.query(Module).filter(Module.applicationId == app_id).count()
                )
                in_roles = (
                    db.query(UserRole).filter(UserRole.applicationId == app_id).count()
                )
                in_profiles = (
                    db.query(UserProfile)
                    .filter(UserProfile.applicationId == app_id)
                    .count()
                )
                in_app_api = (
                    db.query(ApplicationHasApiPermission)
                    .filter(ApplicationHasApiPermission.applicationId == app_id)
                    .count()
                )
                in_app_ui = (
                    db.query(ApplicationHasUiPermission)
                    .filter(ApplicationHasUiPermission.applicationId == app_id)
                    .count()
                )
                if (
                    in_modules == 0
                    and in_roles == 0
                    and in_profiles == 0
                    and in_app_api == 0
                    and in_app_ui == 0
                ):
                    db.query(Application).filter(Application.id == app_id).delete(
                        synchronize_session=False
                    )

        db.flush()

    def delete_by_realm_and_application_data(
        self, db: Session, realm_id: int, application_id: int
    ) -> None:
        # 1. Delete user profiles for this realm and application
        db.query(UserProfile).filter(
            UserProfile.realmId == realm_id,
            UserProfile.applicationId == application_id,
        ).delete(synchronize_session=False)

        # 2. Delete user role module permissions for this realm and application
        db.query(UserRoleHasModulesHasApiPermission).filter(
            UserRoleHasModulesHasApiPermission.realmId == realm_id,
            UserRoleHasModulesHasApiPermission.applicationId == application_id,
        ).delete(synchronize_session=False)
        db.query(UserRoleHasModulesHasUiPermission).filter(
            UserRoleHasModulesHasUiPermission.realmId == realm_id,
            UserRoleHasModulesHasUiPermission.applicationId == application_id,
        ).delete(synchronize_session=False)

        # 3. Delete user roles for this realm and application
        db.query(UserRole).filter(
            UserRole.realmId == realm_id,
            UserRole.applicationId == application_id,
        ).delete(synchronize_session=False)

        # 4. Delete application permissions for this realm and application
        db.query(ApplicationHasApiPermission).filter(
            ApplicationHasApiPermission.realmId == realm_id,
            ApplicationHasApiPermission.applicationId == application_id,
        ).delete(synchronize_session=False)
        db.query(ApplicationHasUiPermission).filter(
            ApplicationHasUiPermission.realmId == realm_id,
            ApplicationHasUiPermission.applicationId == application_id,
        ).delete(synchronize_session=False)

        # 5. Delete module permissions for modules belonging to this realm and application
        module_ids = [
            m[0]
            for m in db.query(Module.id)
            .filter(
                Module.realmId == realm_id,
                Module.applicationId == application_id,
            )
            .all()
        ]
        if module_ids:
            db.query(ModuleHasApiPermission).filter(
                ModuleHasApiPermission.moduleId.in_(module_ids)
            ).delete(synchronize_session=False)
            db.query(ModuleHasUiPermission).filter(
                ModuleHasUiPermission.moduleId.in_(module_ids)
            ).delete(synchronize_session=False)

        # 6. Delete modules for this realm and application
        db.query(Module).filter(
            Module.realmId == realm_id,
            Module.applicationId == application_id,
        ).delete(synchronize_session=False)

        # 7. Delete realms_has_applications mapping for this realm and application
        db.query(RealmsHasApplications).filter(
            RealmsHasApplications.realm_id == realm_id,
            RealmsHasApplications.application_id == application_id,
        ).delete(synchronize_session=False)

        # 8. Clean up application if no other mappings exist
        remaining_mappings = (
            db.query(RealmsHasApplications)
            .filter(RealmsHasApplications.application_id == application_id)
            .count()
        )
        if remaining_mappings == 0:
            in_modules = (
                db.query(Module).filter(Module.applicationId == application_id).count()
            )
            in_roles = (
                db.query(UserRole).filter(UserRole.applicationId == application_id).count()
            )
            in_profiles = (
                db.query(UserProfile)
                .filter(UserProfile.applicationId == application_id)
                .count()
            )
            in_app_api = (
                db.query(ApplicationHasApiPermission)
                .filter(ApplicationHasApiPermission.applicationId == application_id)
                .count()
            )
            in_app_ui = (
                db.query(ApplicationHasUiPermission)
                .filter(ApplicationHasUiPermission.applicationId == application_id)
                .count()
            )
            if (
                in_modules == 0
                and in_roles == 0
                and in_profiles == 0
                and in_app_api == 0
                and in_app_ui == 0
            ):
                db.query(Application).filter(Application.id == application_id).delete(
                    synchronize_session=False
                )

        # 9. Clean up realm if no other applications or modules/roles/profiles remain
        realm_apps = (
            db.query(RealmsHasApplications)
            .filter(RealmsHasApplications.realm_id == realm_id)
            .count()
        )
        if realm_apps == 0:
            realm_modules = (
                db.query(Module).filter(Module.realmId == realm_id).count()
            )
            realm_roles = (
                db.query(UserRole).filter(UserRole.realmId == realm_id).count()
            )
            realm_profiles = (
                db.query(UserProfile).filter(UserProfile.realmId == realm_id).count()
            )
            if realm_modules == 0 and realm_roles == 0 and realm_profiles == 0:
                db.query(Realm).filter(Realm.id == realm_id).delete(
                    synchronize_session=False
                )

        db.flush()

