from schemas.module.module_request import ModuleRequestDTO
from schemas.module.module_response import ModuleResponseDTO
from models.module.module import Module
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto


def to_dto(module: Module) -> ModuleResponseDTO:
    dto = ModuleResponseDTO()
    dto.moduleId = module.id
    dto.realmId = module.realmId
    dto.applicationId = module.applicationId
    dto.moduleName = module.moduleName
    dto.active = module.active
    dto.realm = to_realm_dto(module.realm) if module.realm else None
    dto.application = (
        to_application_dto(module.application) if module.application else None
    )
    return dto


def to_dto_list(modules) -> list[ModuleResponseDTO]:
    return [to_dto(module) for module in modules]


def to_model(module: Module, module_request: ModuleRequestDTO) -> Module:
    module.realmId = module_request.realmId
    module.applicationId = module_request.applicationId
    module.moduleName = module_request.moduleName
    module.active = module_request.active
    return module
