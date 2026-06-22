from security_models import SecurityLog
from sqlalchemy.orm import Session

def log_security_event(db: Session, event_type: str, entity: str, entity_id: int, severity: str, details: str):
    log = SecurityLog(
        event_type=event_type,
        entity=entity,
        entity_id=entity_id,
        severity=severity,
        details=details
    )
    db.add(log)
    db.commit()