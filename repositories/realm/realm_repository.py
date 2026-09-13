from models.realm.realm import Realm


class RealmRepository:

    def get_all_active_realms(self, db, only_active: bool = True) -> list[Realm]:
        query = db.query(Realm)
        if only_active:
            query = query.filter(Realm.active == True)
        return query.order_by(Realm.id.desc()).all()

    def get_by_id(self, db, realm_id: int) -> Optional[Realm]:
        return db.query(Realm).filter(Realm.id == realm_id).first()
