import os
from datetime import datetime

from config import db
from models import Applicant, Application, LegalDocs

# Delete database file if it exists currently
if os.path.exists("people.db"):
    os.remove("people.db")


# Create the database
db.create_all()

application1 = Application(
    channel = "directMail",
    type = "Credit",
    offerId = "ASBNU2314",
    ipAddress = "11.32.44.55",
    neuroIdIdentifier = "3aqw-234rasdf-324qvxc-2345q",
    threatmetrixSessionId = "sfdfgtw435tgdxsfgqe4rwaqes",
    applicationAgreements = True,
    cardholderAgreements = True,
    electronicCommunication = True,
    privacyPolicy = True,
    termsOfService = True,
    disclosureHtml = "gcs://somebucket/somesnapshot",
    reviewPageHtml = "gcs://somebucket/somesnapshot",
)
db.session.add(application1)

applicant1 = Applicant(
    firstName = "First 1",
    middleName = "Middle 1",
    lastName = "Last 1",
    birthDate = "01/01/1980",
    ssn = "123-321-4321",
    phoneNumber = "321-321-4321",
    emailAddress = "testuser@gmail.com",
    addressLine1 = "123 Mission St",
    addressLine2 = "apt 1111",
    city = "San Francisco",
    state = "CA",
    zip = "94104-4321"

)
db.session.add(applicant1)
applicant1.applications.append(application1)


legalDocs1 = LegalDocs(
    link = "gcs://somebucket/somefolder/somedoc",
    type = "CAG"
)
db.session.add(legalDocs1)
application1.legalDocs.append(legalDocs1)

db.session.commit()

