import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    """
    Custom user manager for creating users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for healthcare providers and staff.
    Extends AbstractBaseUser for full control over authentication.

    This model represents therapists, OTs, OTAs, admins, and other staff members.
    Patients are NOT users - they have a separate Patient model.
    """

    # Role Choices
    ADMIN = 'admin'
    OT = 'ot'
    OTA = 'ota'
    SUPERVISOR = 'supervisor'
    VIEWER = 'viewer'

    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (OT, 'Occupational Therapist'),
        (OTA, 'Occupational Therapy Assistant'),
        (SUPERVISOR, 'Supervisor'),
        (VIEWER, 'Viewer (Read-only)'),
    ]

    # Specialization Choices
    GERIATRICS = 'geriatrics'
    PEDIATRICS = 'pediatrics'
    NEURO = 'neuro'
    ORTHOPEDIC = 'orthopedic'
    HAND = 'hand'
    GENERAL = 'general'

    SPECIALIZATION_CHOICES = [
        (GERIATRICS, 'Geriatrics'),
        (PEDIATRICS, 'Pediatrics'),
        (NEURO, 'Neurology'),
        (ORTHOPEDIC, 'Orthopedic'),
        (HAND, 'Hand Therapy'),
        (GENERAL, 'General Practice'),
    ]

    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        help_text="User's email address (used for login)"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Username can only contain letters, numbers, and @/./+/-/_ characters'
            )
        ],
        help_text="Unique username"
    )

    # Personal Information (will be encrypted in production)
    first_name = models.CharField(max_length=150, help_text="First name")
    last_name = models.CharField(max_length=150, help_text="Last name")

    # Professional Information
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=VIEWER,
        db_index=True,
        help_text="User's role in the organization"
    )
    license_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Professional license number"
    )
    license_state = models.CharField(
        max_length=2,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}$',
                message='License state must be a 2-letter uppercase state code'
            )
        ],
        help_text="State where license was issued (e.g., CA, NY)"
    )
    license_expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text="License expiration date"
    )
    npi_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='NPI number must be exactly 10 digits'
            )
        ],
        help_text="National Provider Identifier (10 digits)"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text="Department or unit"
    )
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default=GENERAL,
        help_text="Clinical specialization"
    )

    # Account Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="User account is active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="User can access admin site"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Email has been verified"
    )

    # Security Fields (HIPAA Compliance)
    failed_login_attempts = models.PositiveIntegerField(
        default=0,
        help_text="Number of consecutive failed login attempts"
    )
    account_locked_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Account locked until this time (null if not locked)"
    )
    password_last_changed = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When password was last changed"
    )
    password_must_change = models.BooleanField(
        default=False,
        help_text="Force user to change password on next login"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last successful login"
    )
    last_activity = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last activity timestamp (for session timeout)"
    )

    # Two-Factor Authentication
    two_factor_enabled = models.BooleanField(
        default=False,
        help_text="Two-factor authentication is enabled"
    )
    two_factor_secret = models.CharField(
        max_length=255,
        blank=True,
        help_text="2FA secret key (encrypted)"
    )

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        help_text="User who created this account"
    )

    # Required for AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['last_name', 'first_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['last_activity']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def clean(self):
        """Custom validation logic"""
        super().clean()

        # Active OT/OTA users must have valid license
        if self.is_active and self.role in [self.OT, self.OTA]:
            if not self.license_number:
                raise ValidationError({
                    'license_number': 'License number is required for OT and OTA roles'
                })
            if not self.license_expiry_date:
                raise ValidationError({
                    'license_expiry_date': 'License expiry date is required for OT and OTA roles'
                })
            if self.license_expiry_date and self.license_expiry_date < timezone.now().date():
                raise ValidationError({
                    'license_expiry_date': 'License has expired. Please update license information.'
                })

        # Normalize email
        if self.email:
            self.email = self.email.lower()

    def save(self, *args, **kwargs):
        """Override save to run validation and set password_last_changed"""
        # Set password_last_changed on first save or when password changes
        if not self.pk or self.password != User.objects.filter(pk=self.pk).values_list('password', flat=True).first():
            self.password_last_changed = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the user's first name"""
        return self.first_name

    def increment_failed_login(self):
        """
        Increment failed login attempts and lock account if threshold reached.
        HIPAA requirement: Lock account after 5 failed attempts.
        """
        self.failed_login_attempts += 1

        if self.failed_login_attempts >= 5:
            self.lock_account()
        else:
            # Don't call full_clean() here to avoid validation issues during login
            super(User, self).save(update_fields=['failed_login_attempts', 'updated_at'])

    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter on successful login"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.last_login = timezone.now()
        self.last_activity = timezone.now()
        # Don't call full_clean() here to avoid validation issues during login
        super(User, self).save(update_fields=['failed_login_attempts', 'account_locked_until',
                                             'last_login', 'last_activity', 'updated_at'])

    def lock_account(self, minutes=30):
        """
        Lock account for specified duration.
        Default: 30 minutes (HIPAA recommendation)
        """
        self.account_locked_until = timezone.now() + timedelta(minutes=minutes)
        # Don't call full_clean() here to avoid validation issues
        super(User, self).save(update_fields=['account_locked_until', 'failed_login_attempts', 'updated_at'])

    def is_account_locked(self):
        """Check if account is currently locked"""
        if not self.account_locked_until:
            return False

        if timezone.now() < self.account_locked_until:
            return True

        # Lock period has expired, clear the lock
        self.account_locked_until = None
        self.failed_login_attempts = 0
        super(User, self).save(update_fields=['account_locked_until', 'failed_login_attempts', 'updated_at'])
        return False

    def is_session_expired(self, timeout_minutes=15):
        """
        Check if user session has expired due to inactivity.
        HIPAA requirement: 15-minute timeout
        """
        if not self.last_activity:
            return True

        timeout = timedelta(minutes=timeout_minutes)
        return timezone.now() > (self.last_activity + timeout)

    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = timezone.now()
        super(User, self).save(update_fields=['last_activity', 'updated_at'])

    def is_password_expired(self, days=90):
        """
        Check if password needs to be changed.
        HIPAA recommendation: 90-day password rotation
        """
        if not self.password_last_changed:
            return True

        expiry_date = self.password_last_changed + timedelta(days=days)
        return timezone.now() > expiry_date

    def can_access_patient(self, patient):
        """
        Check if user has permission to access a specific patient.
        This will be implemented once Patient model exists.
        """
        # Admins and supervisors can access all patients
        if self.role in [self.ADMIN, self.SUPERVISOR]:
            return True

        # Viewers can only read (implement in view layer)
        # OTs and OTAs can access assigned patients (implement after Patient model)
        return True  # Placeholder

    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role

    def is_clinician(self):
        """Check if user is a clinical staff member (OT or OTA)"""
        return self.role in [self.OT, self.OTA]

    def is_license_expiring_soon(self, days=30):
        """Check if license is expiring within specified days"""
        if not self.license_expiry_date:
            return False

        expiry_threshold = timezone.now().date() + timedelta(days=days)
        return self.license_expiry_date <= expiry_threshold
