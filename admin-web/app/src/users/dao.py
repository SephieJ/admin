# -*- coding: utf-8 -*-

from models import User
from app.src.utils.database import SessionDB


def get(user_id):
    db_session = SessionDB()
    try:
        results = db_session.query(User).filter(User.id == user_id).first()
    except:
        db_session.rollback()
    finally:
        db_session.close()
    return results


def add(user):
    db_session = SessionDB()
    try:
        db_session.add(user)
        db_session.commit()
        db_session.close()
        return True
    except:
        db_session.rollback()
        db_session.close()
        return False


def update(user):
    db_session = SessionDB()
    try:
        updated_user = (
            db_session.query(User)
            .filter(User.id == user.id)
            .filter(User.deleted_date.is_(None))
            .first()
        )
        updated_user.user_id = user.user_id
        updated_user.first_name = user.first_name
        updated_user.last_name = user.last_name
        updated_user.username = user.username
        updated_user.email = user.email
        updated_user.birth_date = user.birth_date
        updated_user.landline_number = user.landline_number
        updated_user.mobile_number = user.mobile_number
        updated_user.image_url = user.image_url
        updated_user.status = user.status
        db_session.commit()
        db_session.close()
        return True
    except:
        db_session.rollback()
        db_session.close()
