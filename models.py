from datetime import datetime

from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

class Application(db.Model):
    __tablename__ = "application"

    applicationId           = db.Column(db.Integer, primary_key=True)
    applicantId             = db.Column(db.Integer, db.ForeignKey('applicant.applicantId'))
    channel                 = db.Column(db.String(80), nullable=False)
    type                    = db.Column(db.String(80), nullable=False)
    offerId                 = db.Column(db.String(80), nullable=False)
    ipAddress               = db.Column(db.String(80), nullable=False)
    neuroIdIdentifier       = db.Column(db.String(80), nullable=False)
    threatmetrixSessionId   = db.Column(db.String(80), nullable=False)
    applicationAgreements   = db.Column(db.String(80), nullable=False)
    cardholderAgreements    = db.Column(db.String(80), nullable=False)
    electronicCommunication = db.Column(db.String(80), nullable=False)
    privacyPolicy           = db.Column(db.String(80), nullable=False)
    termsOfService          = db.Column(db.String(80), nullable=False)
    disclosureHtml          = db.Column(db.String(80), nullable=False)
    reviewPageHtml          = db.Column(db.String(80), nullable=False)
    timestamp               = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    legalDocs = db.relationship(
        'LegalDocs',
        backref='applications',
        cascade="all, delete, delete-orphan",
        single_parent=True,
        )

class LegalDocs(db.Model):
    __tablename__ = "legaldoc"

    legalDocId              = db.Column(db.Integer, primary_key=True)
    applicationId           = db.Column(db.Integer, db.ForeignKey('application.applicationId'))
    link                    = db.Column(db.String(80), nullable=False)
    type                    = db.Column(db.String(80), nullable=False)
    timestamp               = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class Applicant(db.Model):
    __tablename__ = "applicant"

    applicantId  = db.Column(db.Integer, primary_key=True)
    firstName    = db.Column(db.String(80), nullable=False)
    middleName   = db.Column(db.String(80), nullable=False)
    lastName     = db.Column(db.String(80), nullable=False)
    birthDate    = db.Column(db.String(80), nullable=False)
    ssn          = db.Column(db.Integer, nullable=False)
    phoneNumber  = db.Column(db.String(80), nullable=False)
    emailAddress = db.Column(db.String(80), nullable=False)
    addressLine1 = db.Column(db.String(80), nullable=False)
    addressLine2 = db.Column(db.String(80), nullable=False)
    city         = db.Column(db.String(80), nullable=False)
    state        = db.Column(db.String(80), nullable=False)
    zip          = db.Column(db.String(80), nullable=False)
    timestamp    = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    applications = db.relationship(
        'Application',
        backref="applicant",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        )


class ApplicantSchema(SQLAlchemyAutoSchema):  # noqa
    class Meta:
        model = Applicant
        load_instance = True


class ApplicationLegalDocsSchema(SQLAlchemyAutoSchema): # noqa
    legalDocId = fields.Int()
    applicationId = fields.Int()
    link = fields.Str()
    type = fields.Str()
    timestamp = fields.Str() 

class ApplicationSchema(SQLAlchemyAutoSchema):  # noqa
    class Meta:
        model = Application
        include_relationships = True

    legalDocs = fields.Nested("ApplicationLegalDocsSchema", default=[], many=True)    

