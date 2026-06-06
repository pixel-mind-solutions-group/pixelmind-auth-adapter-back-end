from services.user.user_service import UserService
from services.application.application_service import ApplicationService
from services.realm.realm_service import RealmService
from services.module.module_service import ModuleService
from services.api_permission.api_permission_service import ApiPermissionService
from services.impl.user.user_service_impl import UserServiceImpl
from services.impl.application.application_service_impl import ApplicationServiceImpl
from services.impl.realm.realm_service_impl import RealmServiceImpl
from services.impl.module.module_service_impl import ModuleServiceImpl
from services.impl.api_permission.api_permission_service_impl import ApiPermissionServiceImpl


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
