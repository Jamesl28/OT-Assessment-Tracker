import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from datetime import date


class Patient(models.Model):
    """
    Patient model containing Protected Health Information (PHI).

    CRITICAL: All PHI fields should be encrypted in production.
    For now, we're marking fields that need encryption with comments.
    Field-level encryption will be implemented in Phase 2.

    This model represents patients receiving occupational therapy services.
    """

    # Gender Choices
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (PREFER_NOT_TO_SAY, 'Prefer not to say'),
    ]

    # Discharge Disposition Choices
    HOME = 'home'
    SNF = 'snf'  # Skilled Nursing Facility
    LTACH = 'ltach'  # Long-term Acute Care Hospital
    REHAB = 'rehab'  # Rehabilitation Facility
    DECEASED = 'deceased'
    AMA = 'ama'  # Against Medical Advice

    DISCHARGE_DISPOSITION_CHOICES = [
        (HOME, 'Home'),
        (SNF, 'Skilled Nursing Facility'),
        (LTACH, 'Long-term Acute Care Hospital'),
        (REHAB, 'Rehabilitation Facility'),
        (DECEASED, 'Deceased'),
        (AMA, 'Against Medical Advice'),
    ]

    # Precautions Choices (multi-select via JSONField)
    PRECAUTION_FALL_RISK = 'fall_risk'
    PRECAUTION_ISOLATION = 'isolation'
    PRECAUTION_WEIGHT_BEARING = 'weight_bearing_restrictions'
    PRECAUTION_ASPIRATION = 'aspiration_risk'

    PRECAUTION_CHOICES = [
        PRECAUTION_FALL_RISK,
        PRECAUTION_ISOLATION,
        PRECAUTION_WEIGHT_BEARING,
        PRECAUTION_ASPIRATION,
    ]

    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Medical Record Number (MRN) - PHI
    # TODO: Encrypt in production
    medical_record_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Medical Record Number (unique per facility)"
    )

    # Personal Information - PHI
    # TODO: Encrypt all these fields in production
    first_name = models.CharField(max_length=150, help_text="Patient's first name")
    last_name = models.CharField(max_length=150, help_text="Patient's last name")
    middle_name = models.CharField(max_length=150, blank=True, help_text="Patient's middle name")

    date_of_birth = models.DateField(
        help_text="Patient's date of birth"
    )

    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        help_text="Patient's gender"
    )

    # SSN Last 4 - PHI
    # TODO: Encrypt in production
    ssn_last_4 = models.CharField(
        max_length=4,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='SSN last 4 must be exactly 4 digits'
            )
        ],
        help_text="Last 4 digits of SSN"
    )

    # Medical Information - PHI
    # TODO: Encrypt in production
    primary_diagnosis = models.TextField(
        help_text="Primary diagnosis"
    )

    icd10_codes = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of ICD-10 diagnosis codes"
    )

    secondary_diagnoses = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of secondary diagnoses"
    )

    comorbidities = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of comorbidities"
    )

    # Admission/Discharge Information
    admission_date = models.DateField(
        db_index=True,
        help_text="Date patient was admitted"
    )

    discharge_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Date patient was discharged"
    )

    discharge_disposition = models.CharField(
        max_length=50,
        choices=DISCHARGE_DISPOSITION_CHOICES,
        blank=True,
        help_text="Where patient went after discharge"
    )

    # Healthcare Providers - PHI
    # TODO: Encrypt in production
    referring_physician = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of referring physician"
    )

    primary_care_physician = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of primary care physician"
    )

    # Contact Information - PHI
    # TODO: Encrypt in production
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Patient's contact phone number"
    )

    contact_email = models.EmailField(
        max_length=255,
        blank=True,
        help_text="Patient's email address"
    )

    address = models.JSONField(
        default=dict,
        blank=True,
        help_text="Patient's address (street, city, state, zip)"
    )

    # Emergency Contact - PHI
    # TODO: Encrypt in production
    emergency_contact = models.JSONField(
        default=dict,
        blank=True,
        help_text="Emergency contact information (name, relationship, phone)"
    )

    # Insurance Information - PHI
    # TODO: Encrypt in production
    insurance_info = models.JSONField(
        default=dict,
        blank=True,
        help_text="Insurance information (primary, secondary)"
    )

    # Advance Directives - PHI
    # TODO: Encrypt in production
    advance_directives = models.JSONField(
        default=dict,
        blank=True,
        help_text="Advance directives (DNR, healthcare proxy, etc.)"
    )

    # Medical Information - PHI
    # TODO: Encrypt in production
    allergies = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of patient allergies"
    )

    medications = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of current medications"
    )

    # Precautions
    precautions = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of precautions (fall_risk, isolation, etc.)"
    )

    # Status Flags
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Patient is currently active (not discharged/soft deleted)"
    )

    anonymized_for_research = models.BooleanField(
        default=False,
        help_text="Patient data has been anonymized for research purposes"
    )

    consent_for_data_use = models.BooleanField(
        default=False,
        help_text="Patient has consented to data use for research/analytics"
    )

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # Don't allow deleting users who created patients
        related_name='patients_created',
        help_text="User who created this patient record"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_updated',
        help_text="User who last updated this patient record"
    )

    class Meta:
        db_table = 'patients'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['is_active', 'admission_date']),
            models.Index(fields=['medical_record_number']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} (MRN: {self.medical_record_number})"

    def clean(self):
        """Custom validation logic"""
        super().clean()

        # Date of birth cannot be in the future
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValidationError({
                'date_of_birth': 'Date of birth cannot be in the future'
            })

        # Age must be reasonable (0-120 years)
        if self.date_of_birth:
            age = self.get_age()
            if age < 0 or age > 120:
                raise ValidationError({
                    'date_of_birth': f'Age ({age}) is not reasonable. Must be between 0 and 120 years.'
                })

        # Discharge date must be >= admission date
        if self.discharge_date and self.discharge_date < self.admission_date:
            raise ValidationError({
                'discharge_date': 'Discharge date cannot be before admission date'
            })

        # If discharged, must have discharge disposition
        if self.discharge_date and not self.discharge_disposition:
            raise ValidationError({
                'discharge_disposition': 'Discharge disposition is required when patient is discharged'
            })

        # Admission date cannot be in the future
        if self.admission_date and self.admission_date > date.today():
            raise ValidationError({
                'admission_date': 'Admission date cannot be in the future'
            })

    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return patient's full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()

    def get_age(self):
        """Calculate patient's current age in years"""
        if not self.date_of_birth:
            return None

        today = date.today()
        age = today.year - self.date_of_birth.year

        # Adjust if birthday hasn't occurred yet this year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        return age

    def get_length_of_stay(self):
        """
        Calculate length of stay in days.
        Returns days since admission if not discharged,
        or days between admission and discharge if discharged.
        """
        if not self.admission_date:
            return None

        end_date = self.discharge_date if self.discharge_date else date.today()
        los = (end_date - self.admission_date).days
        return los

    def is_discharged(self):
        """Check if patient has been discharged"""
        return self.discharge_date is not None

    def has_active_assessments(self):
        """
        Check if patient has any active/pending assessments.
        This will be implemented once Assessment model exists.
        """
        # TODO: Implement after Assessment model is created
        return False  # Placeholder

    def anonymize_for_export(self):
        """
        Return anonymized version of patient data for research/analytics.
        Removes all PHI while keeping clinically relevant data.
        """
        return {
            'id': str(self.id),
            'age': self.get_age(),
            'gender': self.gender,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'length_of_stay': self.get_length_of_stay(),
            'discharge_disposition': self.discharge_disposition,
            'primary_diagnosis': self.primary_diagnosis if self.consent_for_data_use else '[REDACTED]',
            'icd10_codes': self.icd10_codes if self.consent_for_data_use else [],
            'comorbidities_count': len(self.comorbidities) if self.comorbidities else 0,
            'medications_count': len(self.medications) if self.medications else 0,
            'precautions': self.precautions,
            'is_active': self.is_active,
        }

    def add_precaution(self, precaution):
        """Add a precaution if not already present"""
        if precaution in self.PRECAUTION_CHOICES and precaution not in self.precautions:
            if not self.precautions:
                self.precautions = []
            self.precautions.append(precaution)
            self.save()

    def remove_precaution(self, precaution):
        """Remove a precaution if present"""
        if self.precautions and precaution in self.precautions:
            self.precautions.remove(precaution)
            self.save()

    def has_precaution(self, precaution):
        """Check if patient has a specific precaution"""
        return precaution in self.precautions if self.precautions else False
