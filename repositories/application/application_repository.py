from models.application.application import Application


class ApplicationRepository:

    def get_all(self, db):
        return db.query(Application).all()
