import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from patients.models import Patient
from users.models import User


@pytest.fixture
def test_user(db):
    """Create a test user for patient creation"""
    return User.objects.create_user(
        email='therapist@example.com',
        password='testpass123',
        username='therapist1',
        first_name='Jane',
        last_name='Doe',
        role=User.OT,
        license_number='OT123',
        license_expiry_date=date.today() + timedelta(days=365)
    )


@pytest.mark.django_db
class TestPatientModel:
    """Test suite for Patient model"""

    def test_create_patient_with_required_fields(self, test_user):
        """Test creating a patient with only required fields"""
        patient = Patient.objects.create(
            medical_record_number='MRN001',
            first_name='John',
            last_name='Smith',
            date_of_birth=date(1950, 5, 15),
            gender=Patient.MALE,
            primary_diagnosis='Stroke',
            admission_date=date.today(),
            created_by=test_user
        )

        assert patient.id is not None
        assert patient.medical_record_number == 'MRN001'
        assert patient.first_name == 'John'
        assert patient.last_name == 'Smith'
        assert patient.gender == Patient.MALE
        assert patient.is_active is True
        assert patient.anonymized_for_research is False
        assert patient.consent_for_data_use is False

    def test_create_patient_with_all_fields(self, test_user):
        """Test creating a patient with all fields populated"""
        patient = Patient.objects.create(
            medical_record_number='MRN002',
            first_name='Alice',
            last_name='Johnson',
            middle_name='Marie',
            date_of_birth=date(1970, 3, 20),
            gender=Patient.FEMALE,
            ssn_last_4='1234',
            primary_diagnosis='Hip Replacement',
            icd10_codes=['M16.11', 'Z96.641'],
            secondary_diagnoses=['Hypertension', 'Diabetes'],
            comorbidities=['Heart Disease'],
            admission_date=date.today() - timedelta(days=5),
            discharge_date=date.today(),
            discharge_disposition=Patient.HOME,
            referring_physician='Dr. Smith',
            primary_care_physician='Dr. Jones',
            contact_phone='555-1234',
            contact_email='alice@example.com',
            address={'street': '123 Main St', 'city': 'Springfield', 'state': 'IL', 'zip': '62701'},
            emergency_contact={'name': 'Bob Johnson', 'relationship': 'Spouse', 'phone': '555-5678'},
            insurance_info={'primary': 'Blue Cross', 'policy_number': 'BC123456'},
            advance_directives={'dnr': False, 'healthcare_proxy': 'Bob Johnson'},
            allergies=['Penicillin', 'Latex'],
            medications=['Aspirin', 'Lisinopril'],
            precautions=[Patient.PRECAUTION_FALL_RISK],
            created_by=test_user
        )

        assert patient.middle_name == 'Marie'
        assert patient.ssn_last_4 == '1234'
        assert len(patient.icd10_codes) == 2
        assert patient.discharge_disposition == Patient.HOME
        assert patient.contact_phone == '555-1234'
        assert len(patient.allergies) == 2
        assert Patient.PRECAUTION_FALL_RISK in patient.precautions

    def test_patient_str_representation(self, test_user):
        """Test string representation of patient"""
        patient = Patient.objects.create(
            medical_record_number='MRN003',
            first_name='Bob',
            last_name='Williams',
            date_of_birth=date(1960, 8, 10),
            gender=Patient.MALE,
            primary_diagnosis='Fracture',
            admission_date=date.today(),
            created_by=test_user
        )

        assert str(patient) == 'Bob Williams (MRN: MRN003)'

    def test_get_full_name_without_middle_name(self, test_user):
        """Test get_full_name without middle name"""
        patient = Patient.objects.create(
            medical_record_number='MRN004',
            first_name='Charlie',
            last_name='Brown',
            date_of_birth=date(1980, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        assert patient.get_full_name() == 'Charlie Brown'

    def test_get_full_name_with_middle_name(self, test_user):
        """Test get_full_name with middle name"""
        patient = Patient.objects.create(
            medical_record_number='MRN005',
            first_name='David',
            last_name='Lee',
            middle_name='Thomas',
            date_of_birth=date(1975, 6, 25),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        assert patient.get_full_name() == 'David Thomas Lee'

    def test_get_age(self, test_user):
        """Test age calculation"""
        # Patient born 30 years ago
        birth_date = date.today() - timedelta(days=30*365)
        patient = Patient.objects.create(
            medical_record_number='MRN006',
            first_name='Test',
            last_name='User',
            date_of_birth=birth_date,
            gender=Patient.FEMALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        age = patient.get_age()
        assert age == 29 or age == 30  # Account for leap years

    def test_unique_mrn_constraint(self, test_user):
        """Test that medical_record_number must be unique"""
        Patient.objects.create(
            medical_record_number='MRN_UNIQUE',
            first_name='Patient',
            last_name='One',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        with pytest.raises(ValidationError):
            Patient.objects.create(
                medical_record_number='MRN_UNIQUE',  # Duplicate
                first_name='Patient',
                last_name='Two',
                date_of_birth=date(1970, 1, 1),
                gender=Patient.FEMALE,
                primary_diagnosis='Test',
                admission_date=date.today(),
                created_by=test_user
            )

    def test_date_of_birth_cannot_be_future(self, test_user):
        """Test that date of birth cannot be in the future"""
        patient = Patient(
            medical_record_number='MRN007',
            first_name='Future',
            last_name='Baby',
            date_of_birth=date.today() + timedelta(days=1),  # Future date
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        with pytest.raises(ValidationError) as exc_info:
            patient.full_clean()

        assert 'date_of_birth' in exc_info.value.error_dict

    def test_admission_date_cannot_be_future(self, test_user):
        """Test that admission date cannot be in the future"""
        patient = Patient(
            medical_record_number='MRN008',
            first_name='Future',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today() + timedelta(days=1),  # Future date
            created_by=test_user
        )

        with pytest.raises(ValidationError) as exc_info:
            patient.full_clean()

        assert 'admission_date' in exc_info.value.error_dict

    def test_discharge_date_cannot_be_before_admission(self, test_user):
        """Test that discharge date must be >= admission date"""
        patient = Patient(
            medical_record_number='MRN009',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            discharge_date=date.today() - timedelta(days=1),  # Before admission
            created_by=test_user
        )

        with pytest.raises(ValidationError) as exc_info:
            patient.full_clean()

        assert 'discharge_date' in exc_info.value.error_dict

    def test_discharge_requires_disposition(self, test_user):
        """Test that discharge date requires discharge disposition"""
        patient = Patient(
            medical_record_number='MRN010',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today() - timedelta(days=5),
            discharge_date=date.today(),
            # Missing discharge_disposition
            created_by=test_user
        )

        with pytest.raises(ValidationError) as exc_info:
            patient.full_clean()

        assert 'discharge_disposition' in exc_info.value.error_dict

    def test_discharge_with_disposition_valid(self, test_user):
        """Test that discharge with disposition is valid"""
        patient = Patient.objects.create(
            medical_record_number='MRN011',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today() - timedelta(days=5),
            discharge_date=date.today(),
            discharge_disposition=Patient.HOME,
            created_by=test_user
        )

        assert patient.discharge_disposition == Patient.HOME
        assert patient.is_discharged() is True

    def test_is_discharged(self, test_user):
        """Test is_discharged method"""
        # Not discharged
        patient1 = Patient.objects.create(
            medical_record_number='MRN012',
            first_name='Active',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )
        assert patient1.is_discharged() is False

        # Discharged
        patient2 = Patient.objects.create(
            medical_record_number='MRN013',
            first_name='Discharged',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today() - timedelta(days=5),
            discharge_date=date.today(),
            discharge_disposition=Patient.HOME,
            created_by=test_user
        )
        assert patient2.is_discharged() is True

    def test_get_length_of_stay_active_patient(self, test_user):
        """Test length of stay calculation for active patient"""
        admission = date.today() - timedelta(days=10)
        patient = Patient.objects.create(
            medical_record_number='MRN014',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=admission,
            created_by=test_user
        )

        los = patient.get_length_of_stay()
        assert los == 10

    def test_get_length_of_stay_discharged_patient(self, test_user):
        """Test length of stay calculation for discharged patient"""
        admission = date.today() - timedelta(days=10)
        discharge = date.today() - timedelta(days=3)

        patient = Patient.objects.create(
            medical_record_number='MRN015',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=admission,
            discharge_date=discharge,
            discharge_disposition=Patient.HOME,
            created_by=test_user
        )

        los = patient.get_length_of_stay()
        assert los == 7  # 10 - 3 = 7 days

    def test_ssn_last_4_validation(self, test_user):
        """Test SSN last 4 validation"""
        # Valid SSN last 4
        patient = Patient.objects.create(
            medical_record_number='MRN016',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            ssn_last_4='1234',
            created_by=test_user
        )
        assert patient.ssn_last_4 == '1234'

        # Invalid SSN last 4
        invalid_ssns = ['123', '12345', 'abcd', '12a4']
        for i, ssn in enumerate(invalid_ssns):
            patient = Patient(
                medical_record_number=f'MRN_SSN_{i}',
                first_name='Test',
                last_name='Patient',
                date_of_birth=date(1960, 1, 1),
                gender=Patient.MALE,
                primary_diagnosis='Test',
                admission_date=date.today(),
                ssn_last_4=ssn,
                created_by=test_user
            )
            with pytest.raises(ValidationError):
                patient.full_clean()

    def test_all_genders(self, test_user):
        """Test creating patients with all gender options"""
        genders = [Patient.MALE, Patient.FEMALE, Patient.OTHER, Patient.PREFER_NOT_TO_SAY]

        for i, gender in enumerate(genders):
            patient = Patient.objects.create(
                medical_record_number=f'MRN_GENDER_{i}',
                first_name='Test',
                last_name='Patient',
                date_of_birth=date(1960, 1, 1),
                gender=gender,
                primary_diagnosis='Test',
                admission_date=date.today(),
                created_by=test_user
            )
            assert patient.gender == gender

    def test_all_discharge_dispositions(self, test_user):
        """Test all discharge disposition options"""
        dispositions = [Patient.HOME, Patient.SNF, Patient.LTACH, Patient.REHAB, Patient.DECEASED, Patient.AMA]

        for i, disposition in enumerate(dispositions):
            patient = Patient.objects.create(
                medical_record_number=f'MRN_DISP_{i}',
                first_name='Test',
                last_name='Patient',
                date_of_birth=date(1960, 1, 1),
                gender=Patient.MALE,
                primary_diagnosis='Test',
                admission_date=date.today() - timedelta(days=5),
                discharge_date=date.today(),
                discharge_disposition=disposition,
                created_by=test_user
            )
            assert patient.discharge_disposition == disposition

    def test_add_precaution(self, test_user):
        """Test adding precautions"""
        patient = Patient.objects.create(
            medical_record_number='MRN017',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        patient.add_precaution(Patient.PRECAUTION_FALL_RISK)
        patient.refresh_from_db()
        assert Patient.PRECAUTION_FALL_RISK in patient.precautions

        # Adding duplicate should not duplicate
        patient.add_precaution(Patient.PRECAUTION_FALL_RISK)
        patient.refresh_from_db()
        assert patient.precautions.count(Patient.PRECAUTION_FALL_RISK) == 1

    def test_remove_precaution(self, test_user):
        """Test removing precautions"""
        patient = Patient.objects.create(
            medical_record_number='MRN018',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            precautions=[Patient.PRECAUTION_FALL_RISK, Patient.PRECAUTION_ISOLATION],
            created_by=test_user
        )

        patient.remove_precaution(Patient.PRECAUTION_FALL_RISK)
        patient.refresh_from_db()
        assert Patient.PRECAUTION_FALL_RISK not in patient.precautions
        assert Patient.PRECAUTION_ISOLATION in patient.precautions

    def test_has_precaution(self, test_user):
        """Test checking for precautions"""
        patient = Patient.objects.create(
            medical_record_number='MRN019',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            precautions=[Patient.PRECAUTION_FALL_RISK],
            created_by=test_user
        )

        assert patient.has_precaution(Patient.PRECAUTION_FALL_RISK) is True
        assert patient.has_precaution(Patient.PRECAUTION_ISOLATION) is False

    def test_anonymize_for_export_without_consent(self, test_user):
        """Test anonymization without consent"""
        patient = Patient.objects.create(
            medical_record_number='MRN020',
            first_name='Sensitive',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Sensitive Diagnosis',
            icd10_codes=['M16.11'],
            admission_date=date.today() - timedelta(days=10),
            consent_for_data_use=False,
            created_by=test_user
        )

        anonymized = patient.anonymize_for_export()

        assert 'first_name' not in anonymized
        assert 'last_name' not in anonymized
        assert 'medical_record_number' not in anonymized
        assert anonymized['primary_diagnosis'] == '[REDACTED]'
        assert anonymized['icd10_codes'] == []
        assert anonymized['age'] is not None
        assert anonymized['gender'] == Patient.MALE

    def test_anonymize_for_export_with_consent(self, test_user):
        """Test anonymization with consent"""
        patient = Patient.objects.create(
            medical_record_number='MRN021',
            first_name='Consenting',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.FEMALE,
            primary_diagnosis='Hip Replacement',
            icd10_codes=['M16.11'],
            comorbidities=['Diabetes', 'Hypertension'],
            medications=['Metformin', 'Lisinopril'],
            admission_date=date.today() - timedelta(days=10),
            consent_for_data_use=True,
            created_by=test_user
        )

        anonymized = patient.anonymize_for_export()

        assert anonymized['primary_diagnosis'] == 'Hip Replacement'
        assert len(anonymized['icd10_codes']) == 1
        assert anonymized['comorbidities_count'] == 2
        assert anonymized['medications_count'] == 2

    def test_patient_ordering(self, test_user):
        """Test that patients are ordered by last name, then first name"""
        Patient.objects.create(
            medical_record_number='MRN_Z',
            first_name='Zebra',
            last_name='Zoo',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )
        Patient.objects.create(
            medical_record_number='MRN_A1',
            first_name='Alice',
            last_name='Anderson',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.FEMALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )
        Patient.objects.create(
            medical_record_number='MRN_A2',
            first_name='Bob',
            last_name='Anderson',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        patients = list(Patient.objects.all())

        assert patients[0].last_name == 'Anderson'
        assert patients[0].first_name == 'Alice'
        assert patients[1].last_name == 'Anderson'
        assert patients[1].first_name == 'Bob'
        assert patients[2].last_name == 'Zoo'

    def test_created_by_audit_trail(self, test_user):
        """Test created_by audit trail"""
        patient = Patient.objects.create(
            medical_record_number='MRN022',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        assert patient.created_by == test_user
        assert patient.created_at is not None
        assert patient.updated_at is not None

    def test_updated_by_audit_trail(self, test_user):
        """Test updated_by audit trail"""
        patient = Patient.objects.create(
            medical_record_number='MRN023',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        # Create another user to update
        update_user = User.objects.create_user(
            email='updater@example.com',
            password='pass123',
            username='updater',
            first_name='Update',
            last_name='User'
        )

        patient.primary_diagnosis = 'Updated Diagnosis'
        patient.updated_by = update_user
        patient.save()

        assert patient.updated_by == update_user

    def test_json_field_defaults(self, test_user):
        """Test that JSON fields default to empty list/dict"""
        patient = Patient.objects.create(
            medical_record_number='MRN024',
            first_name='Test',
            last_name='Patient',
            date_of_birth=date(1960, 1, 1),
            gender=Patient.MALE,
            primary_diagnosis='Test',
            admission_date=date.today(),
            created_by=test_user
        )

        assert patient.icd10_codes == []
        assert patient.secondary_diagnoses == []
        assert patient.comorbidities == []
        assert patient.allergies == []
        assert patient.medications == []
        assert patient.precautions == []
        assert patient.address == {}
        assert patient.emergency_contact == {}
        assert patient.insurance_info == {}
        assert patient.advance_directives == {}
