import math
from sqlalchemy import func, or_
from models.application.application import Application
from models.realm.realm import Realm


class ApplicationRepository:

    def get_all_active_applications(self, db):
        return (
            db.query(Application)
            .filter(Application.active == True)
            .order_by(Application.id.desc())
            .all()
        )

    def search(
        self,
        db,
        page: int,
        size: int,
        query: str = None,
        realm_id: int = None,
        application_id: int = None,
    ):
        base_query = db.query(Application)

        if realm_id is not None and realm_id != -1:
            base_query = base_query.filter(Application.realmId == realm_id)

        if application_id is not None and application_id != -1:
            base_query = base_query.filter(Application.id == application_id)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.join(Realm, Application.realmId == Realm.id).filter(
                or_(
                    Application.applicationName.ilike(pattern),
                    Application.uuid.ilike(pattern),
                    Realm.realm.ilike(pattern),
                )
            )

        total = base_query.with_entities(func.count(Application.id)).scalar() or 0

        applications = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return applications, total_pages, total
