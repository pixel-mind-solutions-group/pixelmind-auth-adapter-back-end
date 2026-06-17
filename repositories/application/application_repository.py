import math
from sqlalchemy import func, or_
from models.application.application import Application
from models.realm.realm import Realm
from models.realms_has_applications.realms_has_applications import RealmsHasApplications


class ApplicationRepository:

    def get_all_active_applications(self, db):
        return (
            db.query(RealmsHasApplications)
            .join(Application, RealmsHasApplications.application_id == Application.id)
            .filter(Application.active == True)
            .order_by(RealmsHasApplications.id.desc())
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
        base_query = db.query(RealmsHasApplications).join(
            Application, RealmsHasApplications.application_id == Application.id
        ).join(
            Realm, RealmsHasApplications.realm_id == Realm.id
        )

        if realm_id is not None and realm_id != -1:
            base_query = base_query.filter(RealmsHasApplications.realm_id == realm_id)

        if application_id is not None and application_id != -1:
            base_query = base_query.filter(RealmsHasApplications.application_id == application_id)

        if query:
            pattern = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    Application.clientId.ilike(pattern),
                    RealmsHasApplications.uuid.ilike(pattern),
                    RealmsHasApplications.internal_application_uuid.ilike(pattern),
                    Realm.realm.ilike(pattern),
                )
            )

        total = base_query.with_entities(func.count(RealmsHasApplications.id)).scalar() or 0

        applications = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return applications, total_pages, total
