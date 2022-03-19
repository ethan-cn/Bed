import os
import importlib
from django.test import TestCase
from patient.models import Patient, Department
from user.models import UserTable, Role
from bed.models import Bed


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class BaseFileTest(TestCase):  #Test whether file is missing
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.bed_dir = os.path.join(self.project_base_dir, 'bed')
        self.patient_dir = os.path.join(self.project_base_dir, 'patient')
        self.user_dir = os.path.join(self.project_base_dir, 'user')

    def baseFile(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'hospital_bed_management'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'hospital_bed_management', 'urls.py'))
        require_exists = os.path.isfile(os.path.join(self.project_base_dir, 'requirements.txt'))
        sql_exists = os.path.isfile(os.path.join(self.project_base_dir, 'hospital_bed.sql'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Configuration directory doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Project's urls.py module doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(require_exists, f"{FAILURE_HEADER}Project's requirement.txt doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(sql_exists, f"{FAILURE_HEADER}Project's database hospital_bed.sql doesn't exist.{FAILURE_FOOTER}")

    def bedFile(self):
        bed_exists = os.path.isdir(self.bed_dir)
        bed_models_module_exists = os.path.isfile(os.path.join(self.bed_dir, 'models.py'))
        bed_views_module_exists = os.path.isfile(os.path.join(self.bed_dir, 'view.py'))

        self.assertTrue(bed_exists, f"{FAILURE_HEADER}Bed folder doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(bed_models_module_exists, f"{FAILURE_HEADER}Models file of bed doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(bed_views_module_exists, f"{FAILURE_HEADER}Views file of bed doesn't exist.{FAILURE_FOOTER}")

    def patientFile(self):
        patient_exists = os.path.isdir(self.patient_dir)
        patient_models_module_exists = os.path.isfile(os.path.join(self.patient_dir, 'models.py'))
        patient_views_module_exists = os.path.isfile(os.path.join(self.patient_dir, 'view.py'))

        self.assertTrue(patient_exists, f"{FAILURE_HEADER}Patient folder doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(patient_models_module_exists, f"{FAILURE_HEADER}Models file of patient doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(patient_views_module_exists, f"{FAILURE_HEADER}Views file of patient doesn't exist.{FAILURE_FOOTER}")

    def userFile(self):
        user_exists = os.path.isdir(self.user_dir)
        user_models_module_exists = os.path.isfile(os.path.join(self.user_dir, 'models.py'))
        user_views_module_exists = os.path.isfile(os.path.join(self.user_dir, 'view.py'))

        self.assertTrue(user_exists, f"{FAILURE_HEADER}User folder doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(user_models_module_exists, f"{FAILURE_HEADER}Models file of user doesn't exist.{FAILURE_FOOTER}")
        self.assertTrue(user_views_module_exists, f"{FAILURE_HEADER}Views file of user doesn't exist.{FAILURE_FOOTER}")

class TemplateTest(TestCase):  #Test weather using base.html
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')

    def baseFile(self):
        base_file = os.path.isfile(os.path.join(self.templates_dir, 'base.html'))

        self.assertTrue(base_file, f"{FAILURE_HEADER}Base html file doesn't exist.{FAILURE_FOOTER}")

class ModelTest(TestCase):  #Test models
    def setUp(self):
        bed = Bed.objects.get_or_create(bed_name='100', price=100, status=0)
        Bed.objects.get_or_create(bed_name='111', price=300, status=0)
        Patient.objects.get_or_create(name='Tom', age='20', patient_bed_id=bed[0])
        Department.objects.get_or_create(name='surgery', addr=3, doctor_name='Alex')
        role = Role.objects.get_or_create(role_code='0')
        UserTable.objects.get_or_create(name='Dm', password='123456', user_role=role[0])

    def testModel(self):
        bed_test = Bed.objects.get(bed_name='111')
        self.assertEqual(bed_test.price, 300, f"{FAILURE_HEADER}Tests on the bed model failed.{FAILURE_FOOTER}")
        patient_test = Patient.objects.get(name='Tom')
        bed_test1 = Bed.objects.get(bed_name='100')
        self.assertEqual(patient_test.patient_bed_id, bed_test1, f"{FAILURE_HEADER}Tests on the patient model failed.{FAILURE_FOOTER}")
        dep_test = Department.objects.get(name='surgery')
        self.assertEqual(dep_test.doctor_name, 'Alex', f"{FAILURE_HEADER}Tests on the department model failed.{FAILURE_FOOTER}")
        user_test = UserTable.objects.get(name='Dm')
        self.assertEqual(user_test.password, '123456', f"{FAILURE_HEADER}Tests on the user model failed.{FAILURE_FOOTER}")