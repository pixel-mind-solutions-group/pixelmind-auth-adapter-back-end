from models.realm.realm import Realm


class RealmRepository:

    def get_all_active_realms(self, db, only_active: bool = True) -> list[Realm]:
        query = db.query(Realm)
        if only_active:
            query = query.filter(Realm.active == True)
        return query.order_by(Realm.id.desc()).all()
