from services.user.user_service import UserService
from services.application.application_service import ApplicationService
from services.realm.realm_service import RealmService
from services.module.module_service import ModuleService
from services.api_permission.api_permission_service import ApiPermissionService
from services.application_has_api_permission.application_has_api_permission_service import (
    ApplicationHasApiPermissionService,
)
from services.ui_permission.ui_permission_service import UiPermissionService
from services.application_has_ui_permission.application_has_ui_permission_service import (
    ApplicationHasUiPermissionService,
)
from services.module_has_api_permission.module_has_api_permission_service import (
    ModuleHasApiPermissionService,
)
from services.module_has_ui_permission.module_has_ui_permission_service import (
    ModuleHasUiPermissionService,
)
from services.user_role.user_role_service import UserRoleService
from services.user_role_profile.user_role_profile_service import (
    UserRoleProfileService,
)
from services.impl.user_role_profile.user_role_profile_service_impl import (
    UserRoleProfileServiceImpl,
)
from services.impl.user.user_service_impl import UserServiceImpl
from services.impl.application.application_service_impl import ApplicationServiceImpl
from services.impl.realm.realm_service_impl import RealmServiceImpl
from services.impl.module.module_service_impl import ModuleServiceImpl
from services.impl.api_permission.api_permission_service_impl import ApiPermissionServiceImpl
from services.impl.application_has_api_permission.application_has_api_permission_service_impl import (
    ApplicationHasApiPermissionServiceImpl,
)
from services.impl.ui_permission.ui_permission_service_impl import UiPermissionServiceImpl
from services.impl.application_has_ui_permission.application_has_ui_permission_service_impl import (
    ApplicationHasUiPermissionServiceImpl,
)
from services.impl.module_has_api_permission.module_has_api_permission_service_impl import (
    ModuleHasApiPermissionServiceImpl,
)
from services.impl.module_has_ui_permission.module_has_ui_permission_service_impl import (
    ModuleHasUiPermissionServiceImpl,
)
from services.impl.user_role.user_role_service_impl import UserRoleServiceImpl


def get_user_service() -> UserService:
    return UserServiceImpl()


def get_application_service() -> ApplicationService:
    return ApplicationServiceImpl()


def get_realm_service() -> RealmService:
    return RealmServiceImpl()


def get_module_service() -> ModuleService:
    return ModuleServiceImpl()


def get_api_permission_service() -> ApiPermissionService:
    return ApiPermissionServiceImpl()


def get_application_has_api_permission_service() -> ApplicationHasApiPermissionService:
    return ApplicationHasApiPermissionServiceImpl()


def get_ui_permission_service() -> UiPermissionService:
    return UiPermissionServiceImpl()


def get_application_has_ui_permission_service() -> ApplicationHasUiPermissionService:
    return ApplicationHasUiPermissionServiceImpl()


def get_module_has_api_permission_service() -> ModuleHasApiPermissionService:
    return ModuleHasApiPermissionServiceImpl()


def get_module_has_ui_permission_service() -> ModuleHasUiPermissionService:
    return ModuleHasUiPermissionServiceImpl()


def get_user_role_service() -> UserRoleService:
    return UserRoleServiceImpl()


def get_user_role_profile_service() -> UserRoleProfileService:
    return UserRoleProfileServiceImpl()


