from email.mime import application
from sre_parse import State
from stat import SF_SNAPSHOT
from flask import make_response, abort
from config import db
from models import Applicant, ApplicantSchema, Application, ApplicationSchema


def read_all():
    """
    This function responds to a request for /applicant/{applicant_id}/application
    with the complete lists of applicants

    :return:        json string of list of applications
    """
    # Create the list of applications from our data
    applications = Application.query.order_by(Application.applicationId).all()

    # Serialize the data for the response
    applicant_schema = ApplicantSchema(many=True)
    data = applicant_schema.dump(applications)
    return data


def read_one(application_id):
    """
    This function responds to a request for /applicant/{applicant_id}/application/{application_id}
    with one matching applicantion

    :param application_id:    Id of applicantion to find
    :return:                  application info
    """
    # Build the initial query
    application = (
        Application.query.filter(Application.applicationId == application_id)
    )

    # Did we find an application?
    if application is not None:

        # Serialize the data for the response
        application_schema = ApplicationSchema()
        data = application_schema.dump(application)
        return data

    # Otherwise, nope, didn't find that application
    else:
        abort(404, f"Application not found for Id: {application_id}")


def create(application):
    """
    This function creates a new application
    based on the passed in applicant data

    :param application:     applicant to create
    :return:                201 on success, 406 on application exists
    """

    # Create a person instance using the schema and the passed in person
    schema = ApplicationSchema()
    new_application = schema.load(application, session=db.session)

    # Add the person to the database
    db.session.add(new_application)
    db.session.commit()

    # Serialize and return the newly created person in the response
    data = schema.dump(new_application)

    return data, 201


def update(application_id, application):
    """
    This function updates an existing application

    :param application_id:  Id of the application to update
    :param application:     applicant to update
    :return:                updated application
    """
    # Get the application requested from the db into session
    update_application = Application.query.filter(
        Applicant.applicantId == application_id
    ).one_or_none()

    # Did we find an existing application?
    if update_application is not None:

        # turn the passed in application into a db object
        schema = ApplicantSchema()
        update = schema.load(application, session=db.session)

        # Set the id to the application we want to update
        update.applicationId = update_application.applicationId

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated application in the response
        data = schema.dump(update_application)

        return data, 200

    # Otherwise, nope, didn't find that application
    else:
        abort(404, f"Application not found for Id: {application_id}")


def delete(application_id):
    """
    This function deletes an application

    :param application_id:    Id of the application to delete
    :return:                  200 on successful delete, 404 if not found
    """
    # Get the application requested
    application = Application.query.filter(Application.applicationId == application_id).one_or_none()

    # Did we find an application?
    if application is not None:
        db.session.delete(application)
        db.session.commit()
        return make_response(f"Applicant {application_id} deleted", 200)

    # Otherwise, nope, didn't find that application
    else:
        abort(404, f"Application not found for Id: {application_id}")
