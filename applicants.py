from sre_parse import State
from stat import SF_SNAPSHOT
from flask import make_response, abort
from config import db
from models import Applicant, ApplicantSchema, Application


def read_all():
    """
    This function responds to a request for /applicant
    with the complete lists of applicants

    :return:        json string of list of applicants
    """
    # Create the list of people from our data
    applicant = Applicant.query.order_by(Applicant.lastName).all()

    # Serialize the data for the response
    applicant_schema = ApplicantSchema(many=True)
    data = applicant_schema.dump(applicant)
    return data


def read_one(applicant_id):
    """
    This function responds to a request for /applican/{applicant_id}
    with one matching applicant

    :param applicant_id:    Id of applicant to find
    :return:                applicant matching id
    """
    # Build the initial query
    applicant = (
        Applicant.query.filter(Applicant.applicantId == applicant_id)
    )

    # Did we find a applicant ?
    if applicant is not None:

        # Serialize the data for the response
        applicant_schema = ApplicantSchema()
        data = applicant_schema.dump(applicant)
        return data

    # Otherwise, nope, didn't find that applicant 
    else:
        abort(404, f"Applicant not found for Id: {applicant_id}")


def create(applicant):
    """
    This function creates a new applicant
    based on the passed in applicant data

    :param applicant:   applicant to create
    :return:            201 on success, 406 on applicant exists
    """
    firstName = applicant.get("firstName")
    lastName = applicant.get("lastName")
    middleName = applicant.get("middleName")
    birthDate = applicant.get("birthDate")
    ssn = applicant.get("ssn")
    phoneNumber = applicant.get("phoneNumber")
    emailAddress = applicant.get("emailAddress")
    addressLine1 = applicant.get("addressLine1")
    addressLine2 = applicant.get("addressLine2")
    city = applicant.get("city")
    state = applicant.get("state")
    zip = applicant.get("zip")

    existing_applicant = (
        Applicant.query.filter(
            Applicant.firstName == firstName
            # Applicant.lastName == lastName,
            # Applicant.middleName == middleName,
            # Applicant.birthDate == birthDate,
            # Applicant.ssn == ssn,
            # Applicant.phoneNumber == phoneNumber,
            # Applicant.emailAddress == emailAddress,
            # Applicant.addressLine1 == addressLine1,
            # Applicant.addressLine2 == addressLine2,
            # Applicant.city == city,
            # Applicant.state == state,
            # Applicant.zip == zip,
            )
        .filter(Applicant.lastName == lastName)
        .one_or_none()
    )

    # Can we insert this applicant ?
    if existing_applicant is None:

        # Create a applicant instance using the schema and the passed in applicant 
        schema = ApplicantSchema()
        new_applicant = schema.load(applicant, session=db.session)

        # Add the applicant to the database
        db.session.add(new_applicant)
        db.session.commit()

        # Serialize and return the newly created applicant in the response
        data = schema.dump(new_applicant)

        return data, 201

    # Otherwise, nope, applicant exists already
    else:
        abort(409, f"Applicant {firstName} {lastName} exists already")


def update(applicant_id, applicant):
    """
    This function updates an existing applicant

    :param applicant_id:    Id of the applicant to update
    :param applicant:       applicant to update
    :return:                updated applicant
    """
    # Get the applicant requested from the db into session
    update_applicant = Applicant.query.filter(
        Applicant.applicantId == applicant_id
    ).one_or_none()

    # Did we find an existing applicant ?
    if update_applicant is not None:

        # turn the passed in applicant into a db object
        schema = ApplicantSchema()
        update = schema.load(applicant, session=db.session)

        # Set the id to the applicant we want to update
        update.applicantId = update_applicant.applicantId

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated applicant in the response
        data = schema.dump(update_applicant)

        return data, 200

    # Otherwise, nope, didn't find that applicant 
    else:
        abort(404, f"applicant not found for Id: {applicant_id}")


def delete(applicant_id):
    """
    This function deletes a applicant

    :param applicant_id:    Id of the applicant to delete
    :return:                200 on successful delete, 404 if not found
    """
    # Get the applicant requested
    applicant = Applicant.query.filter(Applicant.applicantId == applicant_id).one_or_none()

    # Did we find a applicant ?
    if applicant is not None:
        db.session.delete(applicant)
        db.session.commit()
        return make_response(f"Applicant {applicant_id} deleted", 200)

    # Otherwise, nope, didn't find that applicant 
    else:
        abort(404, f"Applicant not found for Id: {applicant_id}")
