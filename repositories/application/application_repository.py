import math

from sqlalchemy import func, or_

from models.application.application import Application


class ApplicationRepository:

    def get_all(self, db):
        return db.query(Application).all()

    def search(self, db, page: int, size: int, query: str):
        pattern = f"%{query}%" if query else "%"

        base_query = db.query(Application).filter(
            or_(
                Application.applicationName.ilike(pattern),
                Application.realm.ilike(pattern),
                Application.uuid.ilike(pattern),
            )
        )

        total = base_query.with_entities(func.count(Application.id)).scalar() or 0

        applications = base_query.offset(page * size).limit(size).all()

        total_pages = math.ceil(total / size) if size > 0 else 1

        return applications, total_pages, total
