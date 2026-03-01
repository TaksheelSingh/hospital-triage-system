from sqlalchemy.orm import Session
from models import PatientVisit


def create_visit(db: Session, data: dict, label, prob, override):

    visit = PatientVisit(
        AGE=data["AGE"],
        SEX=data["SEX"],
        TEMPF=data["TEMPF"],
        PULSE=data["PULSE"],
        RESPR=data["RESPR"],
        BPSYS=data["BPSYS"],
        BPDIAS=data["BPDIAS"],
        PAINSCALE=data["PAINSCALE"],
        ARREMS=data["ARREMS"],
        AMBTRANSFER=data["AMBTRANSFER"],
        INJURY=data["INJURY"],
        RFV1=data["RFV1"],
        RFV2=data["RFV2"],
        RFV3=data["RFV3"],
        RFV_TEXT_ALL=data["RFV_TEXT_ALL"],
        classification=label,
        risk_probability=prob,
        override_triggered=override,
        status="OPEN"
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    return visit