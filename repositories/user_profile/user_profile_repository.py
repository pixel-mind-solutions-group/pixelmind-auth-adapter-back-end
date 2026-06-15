import math
from sqlalchemy import func, or_
from models.user_profile.user_profile import UserProfile
from models.user.user import User
from models.user_role.user_role import UserRole


class UserProfileRepository:

    def create(self, db, profile: UserProfile) -> UserProfile:
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    def find_by_id(self, db, profile_id: int) -> UserProfile:
        return db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    def find_by_composite(self, db, user_id: int, realm_id: int, application_id: int, role_id: int) -> UserProfile:
        return (
            db.query(UserProfile)
            .filter(
                UserProfile.userId == user_id,
                UserProfile.realmId == realm_id,
                UserProfile.applicationId == application_id,
                UserProfile.userRoleId == role_id,
            )
            .first()
        )

    def delete(self, db, profile: UserProfile) -> bool:
        db.delete(profile)
        db.commit()
        return True

    def search(
        self,
        db,
        page: int,
        size: int,
        realm_id: int = None,
        application_id: int = None,
        user_id: int = None,
        user_role_id: int = None,
        search_query: str = None,
    ) -> tuple[list[UserProfile], int, int]:
        query = db.query(UserProfile)

        if realm_id is not None:
            query = query.filter(UserProfile.realmId == realm_id)
        if application_id is not None:
            query = query.filter(UserProfile.applicationId == application_id)
        if user_id is not None:
            query = query.filter(UserProfile.userId == user_id)
        if user_role_id is not None:
            query = query.filter(UserProfile.userRoleId == user_role_id)

        if search_query:
            query = query.join(UserProfile.user).join(UserProfile.user_role).filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    User.email.ilike(f"%{search_query}%"),
                    User.firstName.ilike(f"%{search_query}%"),
                    User.lastName.ilike(f"%{search_query}%"),
                    UserRole.roleName.ilike(f"%{search_query}%"),
                )
            )

        total = query.with_entities(func.count(UserProfile.id)).scalar() or 0
        total_pages = math.ceil(total / size) if size > 0 else 0

        offset = page * size
        profiles = query.order_by(UserProfile.id.desc()).offset(offset).limit(size).all()

        return profiles, total_pages, total
