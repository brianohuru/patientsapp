

from models import Patient, SubCounty, MaritalStatus, Gender

patientsNrBefore = len(Patient().filter())

patient = Patient()
patient.firstName = "James"
patient.lastName = "Mwanza"
patient.subCounty = SubCounty().get(id=1)
patient.maritalStatus = MaritalStatus().get(id=1)
patient.email = "james@yahoo.com"
patient.address = "P.O Box 1"
patient.telephone = "123456789"
patient.gender = Gender().get(id=1)
patient.birthDate = "2000-01-01"
patient.create()

patientsNrAfter = len(Patient().filter())

print(patientsNrBefore + 1 == patientsNrAfter)
