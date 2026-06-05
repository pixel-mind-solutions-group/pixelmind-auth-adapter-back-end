from services.user.user_service import UserService
from services.application.application_service import ApplicationService
from services.realm.realm_service import RealmService
from services.impl.user.user_service_impl import UserServiceImpl
from services.impl.application.application_service_impl import ApplicationServiceImpl
from services.impl.realm.realm_service_impl import RealmServiceImpl


def get_user_service() -> UserService:
    return UserServiceImpl()


def get_application_service() -> ApplicationService:
    return ApplicationServiceImpl()


def get_realm_service() -> RealmService:
    return RealmServiceImpl()
