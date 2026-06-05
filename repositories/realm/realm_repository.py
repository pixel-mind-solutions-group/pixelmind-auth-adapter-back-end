from models.realm.realm import Realm


class RealmRepository:

    def get_all_active_realms(self, db) -> list[Realm]:
        return (
            db.query(Realm).filter(Realm.active == True).order_by(Realm.id.desc()).all()
        )
