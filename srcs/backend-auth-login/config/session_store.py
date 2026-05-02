from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from connect_db import SessionDB
from uuid import uuid4

import json

def create_session(db: Session, user_id: int, data: Optional[Dict[str, Any]] = None, ttl_seconds: int = 7 * 24 * 3600) -> str:
    """Create a session row and return the session id (uuid string)."""
    session_id = str(uuid4())
    # now = datetime.utcnow()
    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=ttl_seconds)
    row = SessionDB(id=session_id, user_id=user_id, data=data, expires_at=expires, created_at=now)
    db.add(row)
    db.commit()
    return session_id


def get_session(db: Session, session_id: str):
    """Return the session row if exists and not expired, else None."""
    row = db.query(SessionDB).filter(SessionDB.id == session_id).first()
    if not row:
        return None
    if row.expires_at < datetime.now():
        try:
            db.delete(row)
            db.commit()
        except Exception:
            db.rollback()
        return None
    return row


def delete_session(db: Session, session_id: str) -> None:
    try:
        db.query(SessionDB).filter(SessionDB.id == session_id).delete()
        db.commit()
    except Exception:
        db.rollback()

