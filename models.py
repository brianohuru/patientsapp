from db import DbConnection


def stringify_kwargs(kwargs=None):
    if len(kwargs.items()) == 0:
        return ""
    where = []
    for key, val in kwargs.items():
        where.append(f"{key}='{val}'")
    if len(where) > 0:
        return "WHERE " + (" AND ".join(where))
    return "WHERE id = NULL "


class Gender:
    id = None
    name = None


    def get(self, id):
        query = f"Select id, name FROM gender WHERE id={id}"
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.name = row[1]
            return self

    def filter(self):
        query = f"Select id, name FROM gender"
        result = DbConnection.selectQuery(query)
        genders = []
        for row in result:
            gender = Gender()
            gender.id = row[0]
            gender.name = row[1]
            genders.append(gender)
        return genders


class MaritalStatus:
    id = None
    name = None

    def get(self, id):
        query = f"Select id, name FROM maritalstatus WHERE id={id}"
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.name = row[1]
            return self

    def filter(self):
        query = f"Select id, name FROM maritalstatus"
        result = DbConnection.selectQuery(query)
        statuses = []
        for row in result:
            status = MaritalStatus()
            status.id = row[0]
            status.name = row[1]
            statuses.append(status)
        return statuses


class Relationship:
    id = None
    name = None

    def get(self, id):
        query = f"Select id, name FROM relationship WHERE id={id}"
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.name = row[1]
            return self

    def filter(self):
        query = f"Select id, name FROM relationship"
        result = DbConnection.selectQuery(query)
        relations = []
        for row in result:
            relation = Relationship()
            relation.id = row[0]
            relation.name = row[1]
            relations.append(relation)
        return relations


class County:
    id = None
    name = None

    def get(self, id):
        query = f"Select id, name FROM county WHERE id={id}"
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.name = row[1]
            return self

    def filter(self):
        query = f"Select id, name FROM county"
        result = DbConnection.selectQuery(query)
        counties = []
        for row in result:
            county = County()
            county.id = row[0]
            county.name = row[1]
            counties.append(county)
        return counties


class SubCounty:
    id = None
    name = None
    county = None

    def get(self, id):
        query = f"Select id, name, countyid FROM subcounty WHERE id={id}"
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.name = row[1]
            self.county = County().get(row[2])
            return self

    def filter(self, **kwargs):
        query = f"Select id, name, countyid FROM subcounty {stringify_kwargs(kwargs)}"
        result = DbConnection.selectQuery(query)
        subcounties = []
        for row in result:
            subcounty = SubCounty()
            subcounty.id = row[0]
            subcounty.name = row[1]
            subcounty.county = County().get(row[2])
            subcounties.append(subcounty)
        return subcounties


class Patient:
    id = None
    firstName = None
    lastName = None
    birthDate = None
    gender: Gender = None
    telephone = None
    address = None
    subCounty: SubCounty = None
    email = None
    maritalStatus : MaritalStatus = None

    def create(self):
        query = f"""
            INSERT INTO patient(
    	        firstname, lastname, dob, genderid, telephone, address, subcountyid, email, maritalstatusid)
            VALUES (
                '{self.firstName}', '{self.lastName}', '{self.birthDate}', {self.gender.id}, '{self.telephone}', '{self.address}',
                {self.subCounty.id}, '{self.email}', {self.maritalStatus.id}
            );
            """
        id = DbConnection.insertQuery(query)
        if id:
            return self.get(id=id)

    def get(self, id):
        query = f"""
            Select id,firstname, lastname, dob, genderid, telephone, address, subcountyid, email, maritalstatusid 
            FROM patient 
            WHERE id={id}
        """
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.firstName = row[1]
            self.lastName = row[2]
            self.birthDate = row[3]
            self.gender = Gender().get(id=row[4])
            self.telephone = row[5]
            self.address = row[6]
            self.subCounty = SubCounty().get(id=row[7])
            self.email = row[8]
            self.maritalStatus = MaritalStatus().get(id=row[9])
            return self

    def filter(self, **kwargs):
        query = f"""
            Select id,firstname, lastname, dob, genderid, telephone, address, subcountyid, email, maritalstatusid 
            From patient {stringify_kwargs(kwargs)}"""
        result = DbConnection.selectQuery(query)
        patients = []
        for row in result:
            patient = Patient()
            patient.id = row[0]
            patient.firstName = row[1]
            patient.lastName = row[2]
            patient.birthDate = row[3]
            patient.gender = Gender().get(id=row[4])
            patient.telephone = row[5]
            patient.address = row[6]
            patient.subCounty = SubCounty().get(id=row[7])
            patient.email = row[8]
            patient.maritalStatus = MaritalStatus().get(id=row[9])
            patients.append(patient)
        return patients


class Kin:
    id = None
    firstName = None
    lastName = None
    birthDate = None
    gender: Gender = None
    telephone = None

    def create(self):
        query = f"""
            INSERT INTO kin(
    	        firstname, lastname, dob, genderid, telephone)
            VALUES (
                '{self.firstName}', '{self.lastName}', '{self.birthDate}', {self.gender.id}, '{self.telephone}'
            )
            RETURNING id;
            """
        id = DbConnection.insertQuery(query)
        if id:
            return self.get(id=id)

    def get(self, id):
        query = f"""
            Select id,firstname, lastname, dob, genderid, telephone 
            FROM kin 
            WHERE id={id}
        """
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.firstName = row[1]
            self.lastName = row[2]
            self.birthDate = row[3]
            self.gender = Gender().get(id=row[4])
            self.telephone = row[5]
            self.patient = Patient().get(row[7])
            return self

    def filter(self, **kwargs):
        query = f"""
            Select id,firstname, lastname, dob, genderid, telephone
            From kin {stringify_kwargs(kwargs)}"""
        result = DbConnection.selectQuery(query)
        kins = []
        for row in result:
            kin = Kin()
            kin.id = row[0]
            kin.firstName = row[1]
            kin.lastName = row[2]
            kin.birthDate = row[3]
            kin.gender = Gender().get(id=row[4])
            kin.telephone = row[5]
            kins.append(kin)
        return kins


class PatientKin:
    patient = None
    kin = None
    relationship = None

    def create(self):
        query = f"""
           INSERT INTO patientkin(
                patientid, kinid, relationshipid)
           VALUES ({self.patient.id}, {self.kin.id}, {self.relationship.id})
        RETURNING id;
                    """
        records = DbConnection.insertQuery(query)
        if records and len(records) > 0:
            id = records[0][0]
            return self.get(id=id)

    def get(self, id):
        query = f"""
            Select id,patientid, kinid, relationshipid
            FROM patientkin 
            WHERE id={id}
        """
        result = DbConnection.selectQuery(query)
        for row in result:
            self.id = row[0]
            self.patient = Patient().get(id=row[1])
            self.kin = Patient().get(id=row[2])
            self.relationship = Relationship().get(id=row[3])
            return self

    def filter(self, **kwargs):
        query = f"""
            Select id,patientid, kinid, relationshipid
            FROM patientkin
            {stringify_kwargs(kwargs)}"""
        result = DbConnection.selectQuery(query)
        patientkins = []
        for row in result:
            patientkin = PatientKin()
            patientkin.id = row[0]
            patientkin.patient = Patient().get(id=row[1])
            patientkin.kin = Patient().get(id=row[2])
            patientkin.relationship = Relationship().get(id=row[3])
            patientkins.append(patientkin)
        return patientkins
