import random
from typing import get_args
from DataGenUtil import *
import json
from faker import Faker

GENDER = ['Male','Female']
BOOLEAN = [True, False]
OPERATIONAL_STATUS = ['Active','Inactive']
CHARTER_STATUS = ['School Charter', 'Open Enrollment', 'Not a Charter School']
GRADE_LEVEL = ['First Grade','Second Grade','Third Grade','Fourth Grade','Fifth Grade',
'Sixth Grade','Seventh Grade','Eighth Grade','Ninth Grade','Tenth Grade','Eleventh Grade','Twelfth Grade']
SCHOOL_TYPES = ['High School', 'Middle School', 'Elementary School']
SUBJECT_NAMES = ['Foreign Language and Literature','Fine and Performing Arts','Social Studies',
'Life and Physical Sciences','Social Sciences and History', 'Mathematics','Military Science']
LEVELS_OF_EDUCATION = ['Some College No Degree', 'Doctorate', 'Bachelor\'s','Master\'s']
PERSONAL_INFORMATION_VERIFICATION_DESCRIPTIONS = ['Entry in family Bible', 'Other official document',
 'State-issued ID', 'Hospital certificate', 'Passport', 'Parents affidavit', 'Immigration document/visa', 'Drivers license']
RACES = ['Asian' , 'Native Hawaiian - Pacific Islander', 'American Indian - Alaska Native', 'White']
ORG_CATEGORIES = ['Local Education Agency', 'School', 'State Education Agency', 'Education Organization Network']
LEA_CATEGORIES = ['Charter', 'Independent']


class EdFiDataGenerator:
    def __init__(self, lea_id = -1, number_students_per_school=100, include_optional_fields=True, school_year='2021', credit_conversion_factor = 2.0, number_of_grades_per_school = 5, is_current_school_year = True, graduation_plans_per_school = 10, unique_id_length = 5, number_staffs_per_school = 50, number_sections_per_school = 10):
        # Set a seed value in Faker so it generates same values every run.
        self.faker = Faker('en_US')
        Faker.seed(2)

        self.include_optional_fields = include_optional_fields
        self.graduation_plans_per_school = graduation_plans_per_school
        self.school_year = school_year
        self.lea_id = lea_id
        self.country = 'United States of America'
        self.number_students_per_school = number_students_per_school
        self.credit_conversion_factor = credit_conversion_factor
        self.number_of_grades_per_school = number_of_grades_per_school
        self.is_current_school_year = is_current_school_year
        self.unique_id_length = unique_id_length
        self.number_staffs_per_school = number_staffs_per_school
        self.number_sections_per_school = number_sections_per_school

    def get_descriptor_string(self, key, value):
        return "uri://ed-fi.org/{}#{}".format(key,value)

    def generate_data(self, num_of_schools, writer):
        lea = {}
        if self.lea_id == -1:
            lea = self.create_LEA()
        edfi_data = [self.create_school(self.lea_id) for _ in range(num_of_schools)]
        edfi_data_formatted = self.format_edfi_data(edfi_data)

        if len(lea) > 0: 
            writer.write(f'EdFi/LEA.json',list_of_dict_to_json([lea]))
        writer.write(f'EdFi/School.json',list_of_dict_to_json(edfi_data_formatted['Schools']))
        writer.write(f'EdFi/Student.json',list_of_dict_to_json(edfi_data_formatted['Students']))
        writer.write(f'EdFi/StudentSchoolAssociation.json',list_of_dict_to_json(edfi_data_formatted['StudentSchoolAssociations']))
        writer.write(f'EdFi/Course.json',list_of_dict_to_json(edfi_data_formatted['Courses']))
        writer.write(f'EdFi/Calendar.json',list_of_dict_to_json(edfi_data_formatted['Calendars']))
        writer.write(f'EdFi/Session.json',list_of_dict_to_json(edfi_data_formatted['Sessions']))
        writer.write(f'EdFi/StaffSchoolAssociation.json',list_of_dict_to_json(edfi_data_formatted['StaffSchoolAssociations']))
        writer.write(f'EdFi/Section.json',list_of_dict_to_json(edfi_data_formatted['Sections']))
        writer.write(f'EdFi/Staff.json',list_of_dict_to_json(edfi_data_formatted['Staffs']))
        writer.write(f'EdFi/StudentSectionAssociation.json',list_of_dict_to_json(edfi_data_formatted['StudentSectionAssociations']))
        writer.write(f'EdFi/StaffSectionAssociation.json',list_of_dict_to_json(edfi_data_formatted['StaffSectionAssociations']))
        writer.write(f'EdFi/CourseOffering.json',list_of_dict_to_json(edfi_data_formatted['CourseOfferings']))
        writer.write(f'EdFi/StaffEducationOrganizationEmploymentAssociation.json',list_of_dict_to_json(edfi_data_formatted['StaffEducationOrganizationEmploymentAssociations']))
        writer.write(f'EdFi/StudentEducationOrganizationAssociation.json',list_of_dict_to_json(edfi_data_formatted['StudentEducationOrganizationAssociations']))


    def create_LEA(self):
        lea_id = self.faker.random_number(digits = self.unique_id_length)
        self.lea_id = lea_id
        return {
            "categories": [{"educationOrganizationCategoryDescriptor": self.get_descriptor_string("EducationOrganizationCategoryDescriptor", category)} for category in random.sample(ORG_CATEGORIES,2)],
            "localEducationAgencyId": self.lea_id,
            "charterStatusDescriptor": self.get_descriptor_string('CharterStatusDescriptor',random.choice(CHARTER_STATUS)),
            "localEducationAgencyCategoryDescriptor": self.get_descriptor_string("LocalEducationAgencyCategoryDescriptor",random.choice(LEA_CATEGORIES)),
            "nameOfInstitution": self.faker.state() + ' ' + 'Local Education Agency'
        }


    def create_school(self, lea_id):
        school_type = random.choice(SCHOOL_TYPES)
        school_name = self.faker.city() + ' ' + school_type
        school = {
            'schoolId': self.faker.random_number(digits = self.unique_id_length),
            'nameOfInstitution': school_name,
            "localEducationAgencyReference": {
                "localEducationAgencyId": lea_id
            },
            'operationalStatusDescriptor': self.get_descriptor_string('OperationalStatusDescriptor',random.choice(OPERATIONAL_STATUS)),
            'shortNameOfInstitution': ''.join([word[0] for word in school_name.split()]),
            'website':''.join(['www.',school_name.lower().replace(' ',''),'.com']),
            'administrativeFundingControlDescriptor': self.get_descriptor_string('AdministrativeFundingControlDescriptor',random.choice(['public', 'private']) + ' School'),
            'charterStatusDescriptor': self.get_descriptor_string('CharterStatusDescriptor',random.choice(CHARTER_STATUS)),
            'schoolTypeDescriptor': self.get_descriptor_string('SchoolTypeDescriptor','Regular'),
            'titleIPartASchoolDesignationDescriptor': self.get_descriptor_string('TitleIPartASchoolDesignationDescriptor','Not A Title I School'),
            'addresses': [],
            'educationOrganizationCategories':[{'EducationOrganizationCategoryDescriptor': self.get_descriptor_string('EducationOrganizationCategoryDescriptor','School')}],
            'identificationCodes': [
                {
                    'educationOrganizationIdentificationSystemDescriptor': self.get_descriptor_string('EducationOrganizationIdentificationSystemDescriptor','SEA'),
                    'identificationCode': self.faker.random_number(digits=10)
                }
            ],
            'institutionTelephones': self.create_telephones(),
            'internationalAddresses': [],
            'schoolCategories': [
                {
                    'SchoolCategoryDescriptor': self.get_descriptor_string('SchoolCategoryDescriptor',school_type)
                }
            ],
            'gradeLevels': [
                {'gradeLevelDescriptor': self.get_descriptor_string('GradeLevelDescriptor',grade)} for grade in random.sample(GRADE_LEVEL, 4)
            ]
        }

        school['_SchoolYears'] = self.create_school_years()
        school['_Calendars'] = self.create_calendars(school)
        school['_Students'] = self.create_students()
        school['_Courses'] = self.create_courses(school['schoolId'],school_name)
        school['_GraduationPlans'] = self.create_graduation_plans(school)
        school['_StudentAssociations'] = self.create_student_school_associations(school)
        school['_Staffs'] = self.create_staffs()
        school['_StaffSchoolAssociations'] = self.create_staff_school_associations(school)
        school['_Sessions'] = self.create_sessions(school)
        school['_CourseOfferings'] = self.create_course_offerings(school)
        school['_Sections'] = self.create_sections(school)
        school['_StudentEducationOrganizationAssociations'] = self.create_student_education_org_association(self, school)
        school['_StaffEducationOrganizationEmploymentAssociations'] = self.create_staff_employments(school)
        school['_StaffSectionAssociations'] = self.create_staff_section_associations(school)
        school['_StudentSectionAssociations'] = self.create_student_section_associations(school)
        return school

    def create_students(self):
        students = []
        for _ in range(self.number_students_per_school):
            gender = random.choice(GENDER)
            fname = self.faker.first_name_male() if gender == 'Male' else self.faker.first_name_female()
            students.append({
                'studentUniqueId': self.faker.random_number(digits = self.unique_id_length),
                "birthCity": self.faker.city(),
                "birthDate": str(self.faker.date_between(start_date='-18y',end_date='-5y')),
                "birthSexDescriptor": self.get_descriptor_string('sexDescriptor', gender),
                "firstName": fname,
                "identificationDocuments": [],
                "lastSurname": self.faker.last_name(),
                "otherNames": [
                    {
                        "lastSurname": self.faker.last_name(),
                        "OtherNameTypeDescriptor": self.get_descriptor_string('otherNameTypeDescriptor','Nickname'),
                        "FirstName": self.faker.first_name_male() if gender == 'Male' else self.faker.first_name_female(),
                        "PersonalTitlePrefix": 'Mr' if gender == 'Male' else 'Ms'
                    }
                ],
                "personalIdentificationDocuments": [],
                "personalTitlePrefix": 'Mr' if gender == 'Male' else 'Ms',
                "visas": []
                
        })
        return students


    def create_student_school_associations(self,school):
        result = []
        for student in school['_Students']:
            result.append({
                "schoolReference": {
                    "schoolId": school['schoolId']
                },
                "studentReference": {
                    "studentUniqueId": student['studentUniqueId']
                },
                "entryDate": str(self.faker.date_between(start_date='-5y',end_date='today')),
                "entryGradeLevelDescriptor": "uri://ed-fi.org/GradeLevelDescriptor#{}".format(random.choice(GRADE_LEVEL)),
                "alternativeGraduationPlans": [],
                "educationPlans": []
            })
        return result

    def create_calendars(self,school):
        return {
            'calendarCode':self.faker.random_number(digits = self.unique_id_length),
            "schoolReference": {
                "schoolId": school['schoolId']
            },
            "schoolYearTypeReference": {
                "schoolYear": self.school_year
            },
            'calendarTypeDescriptor': self.get_descriptor_string('CalendarTypeDescriptor','Student Specific'),
            'GradeLevel': []
        }

    def create_address(self):
        address = []
        state = self.faker.state_abbr()
        for n in ['Physical', 'Mailing']:
            address.append({
                'addressType':n,
                'city':self.faker.city(),
                'postalCode':self.faker.postcode(),
                'stateAbbreviation':state,
                'streetNumberName':self.faker.street_name()
            })
        return address

    def create_courses(self,school_id,school_name):
        courses = []
        for subject in SUBJECT_NAMES:
            courseCode = '{}-{}'.format(subject[0:3].upper(),random.choice(range(1,5)))
            courses.append({
                "educationOrganizationReference": {
                    "educationOrganizationId": school_id
                },
                "courseCode": courseCode,
                "academicSubjectDescriptor": self.get_descriptor_string('academicSubjectDescriptor', subject),
                "courseDefinedByDescriptor": self.get_descriptor_string('CourseDefinedByDescriptor','SEA'),
                "courseDescription": 'Description about {}'.format(subject),
                "courseGPAApplicabilityDescriptor": self.get_descriptor_string('CourseGPAApplicabilityDescriptor',random.choice(['Applicable','Not Applicable'])),
                "courseTitle": subject,
                "highSchoolCourseRequirement": random.choice(BOOLEAN),
                "numberOfParts": 1,
                "competencyLevels": [],
                "identificationCodes": [
                    {
                        "courseIdentificationSystemDescriptor": self.get_descriptor_string('CourseIdentificationSystemDescriptor','LEA course code'),
                        "courseCatalogURL": "http://www.{}.edu/coursecatalog".format(school_name.lower().replace(' ','')),
                        "identificationCode": courseCode
                    },
                    {
                        "courseIdentificationSystemDescriptor": self.get_descriptor_string('CourseIdentificationSystemDescriptor','State course code'),
                        "identificationCode": self.faker.random_number(digits = self.unique_id_length)
                    }
                ],
                "learningObjectives": [],
                "learningStandards": [],
                "levelCharacteristics": [
                    {
                        "courseLevelCharacteristicDescriptor": self.get_descriptor_string('CourseLevelCharacteristicDescriptor','Core Subject')
                    }
                ],
                "offeredGradeLevels": []
            })
        return courses


    def create_graduation_plans(self, school):
        graduation_plans = []
        for _ in range(self.graduation_plans_per_school):
            graduation_plans.append({
                "educationOrganizationReference": {
                    "EducationOrganizationId": school['schoolId']
                },
                "graduationSchoolYearTypeReference": {
                    "schoolYear": self.school_year
                },
                "graduationPlanTypeDescriptor": self.get_descriptor_string('GraduationPlanTypeDescriptor', random.choice(['Minimum','Recommended'])),
                "totalRequiredCredits": random.choice(range(20,30)),
                "creditsByCourses": [],
                "creditsByCreditCategories": [
                    {
                        "creditCategoryDescriptor": self.get_descriptor_string('CreditCategoryDescriptor','Honors'),
                        "credits": random.choice(range(5,15))
                    }
                ],
                "creditsBySubjects": [],
                "requiredAssessments": []
            })
        return graduation_plans

    def create_school_years(self):
        return {
            'schoolYear': self.school_year,
            'currentSchoolYear': self.is_current_school_year,
            'schoolYearDescription': 'Description about school year'
        }

    def create_telephones(self):
        return [
            {
                'InstitutionTelephoneNumberTypeDescriptor': self.get_descriptor_string('InstitutionTelephoneNumberTypeDescriptor', _),
                "TelephoneNumber": self.faker.phone_number()
            }
            for _ in ['Fax','Main']
        ]

    def create_staffs(self):
        staffs = []
        for _ in range(self.number_staffs_per_school):
            gender = random.choice(GENDER)
            fname = self.faker.first_name_male() if gender == 'Male' else self.faker.first_name_female()
            lname = self.faker.last_name()
            staffs.append({
                
                "staffUniqueId": self.faker.random_number(digits = self.unique_id_length),
                "birthDate": str(self.faker.date_between(start_date='-60y',end_date='-30y')),
                "firstName": fname,
                "highestCompletedLevelOfEducationDescriptor": self.get_descriptor_string('LevelOfEducationDescriptor', value = random.choice(LEVELS_OF_EDUCATION)),
                "hispanicLatinoEthnicity": random.choice(BOOLEAN),
                "lastSurname": lname,
                "loginId": '{}{}'.format(fname[0],lname.lower()),
                "personalTitlePrefix": 'Mr' if gender == 'Male' else 'Ms',
                "sexDescriptor": self.get_descriptor_string('SexDescriptor', value = gender),
                "yearsOfPriorProfessionalExperience": random.choice(range(50)),
                "addresses": [],
                "ancestryEthnicOrigins": [],
                "credentials": [],
                "electronicMails": [
                    {
                        "electronicMailAddress": "{}{}@edfi.org".format(fname,lname),
                        "electronicMailTypeDescriptor": self.get_descriptor_string('ElectronicMailTypeDescriptor','Work')
                    }
                ],
                "identificationCodes": [
                    {
                        "staffIdentificationSystemDescriptor": self.get_descriptor_string('StaffIdentificationSystemDescriptor','State'),
                        "identificationCode": self.faker.random_number(digits = self.unique_id_length)
                    }
                ],
                "identificationDocuments": [],
                "internationalAddresses": [],
                "languages": [],
                "otherNames": [
                    {
                        "lastSurname": self.faker.last_name(),
                        "OtherNameTypeDescriptor": self.get_descriptor_string('otherNameTypeDescriptor','Nickname'),
                        "FirstName": self.faker.first_name_male() if gender == 'Male' else self.faker.first_name_female(),
                        "PersonalTitlePrefix": 'Mr' if gender == 'Male' else 'Ms'
                    }
                ],
                "personalIdentificationDocuments": [
                    {
                        "identificationDocumentUseDescriptor": "uri://ed-fi.org/IdentificationDocumentUseDescriptor#Personal Information Verification",
                        "personalInformationVerificationDescriptor": self.get_descriptor_string('PersonalInformationVerificationDescriptor', value = random.choice(PERSONAL_INFORMATION_VERIFICATION_DESCRIPTIONS))
                    }
                ],
                "races": [
                    {
                        "raceDescriptor": self.get_descriptor_string('RaceDescriptor', value = random.choice(RACES))
                    }
                ]
            })
        return staffs

    def create_sessions(self, school):

        return [{
            "schoolReference":{
                "schoolId":school['schoolId']
            },
            "schoolYearTypeReference": {
                "schoolYear": self.school_year
            },
            "sessionName": "{} - {} Fall Semester".format(int(self.school_year) - 1, self.school_year ),
            "beginDate": "{}-08-{}".format(int(self.school_year) - 1, random.randint(1,30)),
            "endDate": "{}-12-{}".format(int(self.school_year) - 1, random.randint(1,30)),
            "termDescriptor": self.get_descriptor_string('TermDescriptor', 'Fall Semester'),
            "totalInstructionalDays": random.randint(60,130),
            "gradingPeriods": []
        },
        {
            "schoolReference":{
                "schoolId":school['schoolId']
            },
            "schoolYearTypeReference": {
                "schoolYear": self.school_year
            },
            "sessionName": "{} - {} Spring Semester".format(int(self.school_year) - 1, self.school_year ),
            "beginDate": "{}-08-{}".format(int(self.school_year) - 1, random.randint(1,30)),
            "endDate": "{}-12-{}".format(int(self.school_year) - 1, random.randint(1,30)),
            "termDescriptor": self.get_descriptor_string('TermDescriptor', 'Fall Semester'),
            "totalInstructionalDays": random.randint(60,130),
            "gradingPeriods": []
        }]

    def create_sections(self, school):
        sections = []
        for _ in range(self.number_sections_per_school):
            courseOffering = random.choice(school['_CourseOfferings'])
            subjectName = random.choice(SUBJECT_NAMES)
            subjectNumber = random.randint(1,5)
            sections.append({
                "courseOfferingReference": {
                    "localCourseCode": courseOffering['localCourseCode'],
                    "schoolId": courseOffering['schoolReference']['schoolId'],
                    "schoolYear": self.school_year,
                    "sessionName": courseOffering['sessionReference']['sessionName']
                },
                "locationSchoolReference": {
                    "schoolId": school['schoolId']     
                },
                "sectionIdentifier": self.faker.uuid4().replace('-',''),
                "availableCredits": random.randint(1,4),
                "educationalEnvironmentDescriptor": self.get_descriptor_string('EducationalEnvironmentDescriptor','Classroom'),
                "sectionName": "{} {}".format(subjectName, subjectNumber),
                "sequenceOfCourse": random.randint(1,5),
                "characteristics": [],
                "classPeriods": [],
                "courseLevelCharacteristics": [],
                "offeredGradeLevels": [],
                "programs": []
            })
        return sections

    def create_course_offerings(self, school):
        result = []
        for course in school['_Courses']:
            result.append({
                "localCourseCode": "LCC_{}_{}".format(course['courseCode'],school['schoolId']),
                "courseReference": {
                    "courseCode": course['courseCode'],
                    "educationOrganizationId": school['schoolId']
                },
                "schoolReference": {
                    "schoolId": school['schoolId']
                },
                "sessionReference": {
                    "schoolId": school['schoolId'],
                    "schoolYear": self.school_year,
                    "sessionName": random.choice(school['_Sessions'])['sessionName']
                }
            })
        return result

    def create_staff_employments(self, school):
        result = []
        for staff in school['_Staffs']:
            result.append({
                "employmentStatusDescriptor": "uri://ed-fi.org/EmploymentStatusDescriptor#Tenured or permanent",
                "hireDate": str(self.faker.date_between(start_date='-10y',end_date='-1y')),
                "educationOrganizationReference": {
                    "educationOrganizationId": school['schoolId']
                },
                "staffReference": {
                    "staffUniqueId": staff['staffUniqueId']
                },
                "endDate": str(self.faker.date_between(start_date='-1y',end_date='today')),
                "hourlyWage": random.choice(range(10,20)),
                "offerDate": str(self.faker.date_between(start_date='-10y',end_date='-1y'))
            })
        return result

    def create_student_education_org_association(self, school):
        result = []
        for student in school['_Students']:
            result.append({
                "educationOrganizationReference": {
                    "educationOrganizationId": school['schoolId']
                },
                "studentReference": {
                    "studentUniqueId": student['studentUniqueId']
                },
                "sexDescriptor": student['birthSexDescriptor']
            })
        return result

    def create_student_section_associations(self, school):
        student_section_associations = []
        session = random.choice(school['_Sessions'])
        for student in school['_Students']:
            course = random.choice(school['_Courses'])
            section = random.choice(school['_Sections'])
            student_section_associations.append({
                    "sectionReference": {
                        "localCourseCode": course['courseCode'],
                        "schoolId": school['schoolId'],
                        "SchoolYear": self.school_year,
                        "sectionIdentifier": section['sectionIdentifier'],
                        "sessionName": session['sessionName']
                    },
                    "studentReference": {
                        "studentUniqueId": student['studentUniqueId'],
                    },
                    "beginDate": session['beginDate'],
                    "endDate": session['endDate'],
                    "homeroomIndicator": random.choice(BOOLEAN)
                })
        return student_section_associations

    def create_staff_section_associations(self,school):
        staff_section_associations = []
        for staff in school['_Staffs']:
            session = random.choice(school['_Sessions'])
            section = random.choice(school['_Sections'])
            staff_section_associations.append({
                "sectionReference": {
                    "localCourseCode": section['courseOfferingReference']['localCourseCode'],
                    "schoolId": school['schoolId'],
                    "SchoolYear": self.school_year,
                    "sectionIdentifier": section['sectionIdentifier'],
                    "sessionName": session['sessionName']
                },
                "staffReference": {
                    "staffUniqueId": staff['staffUniqueId']
                },
                "beginDate": session['beginDate'],
                "classroomPositionDescriptor": "uri://ed-fi.org/ClassroomPositionDescriptor#Teacher of Record",
                "endDate": session['endDate']
            })
        return staff_section_associations


    def create_staff_school_associations(self, school):
        staff_school_associations = []
        for staff in school['_Staffs']:
            staff_school_associations.append({
                "schoolReference": {
                    "schoolId": school['schoolId']
                },
                "StaffReference": {
                    "staffUniqueId": staff['staffUniqueId']
                },
                "programAssignmentDescriptor": self.get_descriptor_string('ProgramAssignmentDescriptor','Regular Education'),
                "academicSubjects": [
                    {
                        "academicSubjectDescriptor": self.get_descriptor_string('AcademicSubjectDescriptor',random.choice(SUBJECT_NAMES))
                    }
                ],
                "gradeLevels": [
                    {'GradeLevelDescriptor': self.get_descriptor_string('GradeLevelDescriptor',i)} for i in random.sample(GRADE_LEVEL,4)
            ],
            })
        return staff_school_associations

    def format_edfi_data(self,data):
        result = {
            'Schools':[],
            'Students':[],
            'Calendars':[],
            'Courses':[],
            'StudentSchoolAssociations':[],
            'Staffs':[],
            'Sections': [],
            'StaffSchoolAssociations':[],
            'Sessions':[],
            'StudentSectionAssociations':[],
            'StaffSectionAssociations':[],
            'CourseOfferings':[],
            'StaffEducationOrganizationEmploymentAssociations': [],
            'StudentEducationOrganizationAssociations': []

        }
        for school in data:
            result['Schools'].append({key: school[key] for key in school if not (key.startswith('_')) })
            result['Students'] += school['_Students']
            result['Courses'] += school['_Courses']
            result['StudentSchoolAssociations'] += school['_StudentAssociations']
            result['Calendars'].append(school['_Calendars'])
            result['Staffs'] += school['_Staffs']
            result['Sections'] += school['_Sections']
            result['StaffSchoolAssociations'] += school['_StaffSchoolAssociations']
            result['Sessions'] += school['_Sessions']
            result['StudentSectionAssociations'] += school['_StudentSectionAssociations']
            result['StaffSectionAssociations'] += school['_StaffSectionAssociations']
            result['CourseOfferings'] += school['_CourseOfferings']
            result['StaffEducationOrganizationEmploymentAssociations'] += school['_StaffEducationOrganizationEmploymentAssociations']
            result['StudentEducationOrganizationAssociations'] += school['_StudentEducationOrganizationAssociations']


        return result
