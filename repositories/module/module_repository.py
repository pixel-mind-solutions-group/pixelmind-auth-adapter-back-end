import math
from sqlalchemy import func, or_
from models.module.module import Module


class ModuleRepository:

    def create(self, db, module) -> Module:
        db.add(module)
        db.commit()
        db.refresh(module)
        return module

    def search(
        self,
        db,
        page: int,
        size: int,
        query: str = None,
        realm_id: int = None,
        application_id: int = None,
        active: bool = None,
    ):
        base_query = db.query(Module)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.filter(Module.moduleName.ilike(pattern))

        if realm_id is not None and realm_id != -1:
            base_query = base_query.filter(Module.realmId == realm_id)

        if application_id is not None and application_id != -1:
            base_query = base_query.filter(Module.applicationId == application_id)

        if active is not None:
            base_query = base_query.filter(Module.active == active)

        total = base_query.with_entities(func.count(Module.id)).scalar() or 0

        modules = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return modules, total_pages, total

    def find_by_id(self, db, module_id: int):
        return db.query(Module).filter(Module.id == module_id).first()

    def get_all_active_modules(self, db):
        return (
            db.query(Module)
            .filter(Module.active == True)
            .order_by(Module.id.desc())
            .all()
        )

    def find_by_name(self, db, name: str):
        return db.query(Module).filter(Module.moduleName == name).first()

    def delete(self, db, module):
        db.delete(module)
        db.commit()
        return True
