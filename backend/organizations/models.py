import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Organization(models.Model):
    """
    Represents hospitals, clinics, or healthcare facilities.
    This is the multi-tenant parent model stored in the public schema.
    """

    # Organization Types
    HOSPITAL = 'hospital'
    CLINIC = 'clinic'
    NETWORK = 'network'
    PRIVATE_PRACTICE = 'private_practice'

    ORGANIZATION_TYPE_CHOICES = [
        (HOSPITAL, 'Hospital'),
        (CLINIC, 'Clinic'),
        (NETWORK, 'Healthcare Network'),
        (PRIVATE_PRACTICE, 'Private Practice'),
    ]

    # Subscription Tiers
    FREE = 'free'
    PROFESSIONAL = 'professional'
    ENTERPRISE = 'enterprise'

    SUBSCRIPTION_TIER_CHOICES = [
        (FREE, 'Free'),
        (PROFESSIONAL, 'Professional'),
        (ENTERPRISE, 'Enterprise'),
    ]

    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Organization name")
    organization_type = models.CharField(
        max_length=50,
        choices=ORGANIZATION_TYPE_CHOICES,
        help_text="Type of healthcare facility"
    )

    # Multi-tenancy Fields
    schema_name = models.CharField(
        max_length=63,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z][a-z0-9_]*$',
                message='Schema name must start with a letter and contain only lowercase letters, numbers, and underscores'
            )
        ],
        help_text="PostgreSQL schema name for tenant isolation"
    )
    subdomain = models.CharField(
        max_length=63,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$',
                message='Subdomain must contain only lowercase letters, numbers, and hyphens'
            )
        ],
        help_text="Subdomain for URL routing (e.g., stmarys.otassess.com)"
    )

    # Business Identifiers
    npi_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='NPI number must be exactly 10 digits'
            )
        ],
        help_text="National Provider Identifier (10 digits)"
    )
    tax_id = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="EIN/Tax ID"
    )

    # HIPAA Compliance
    business_associate_agreement_signed = models.BooleanField(
        default=False,
        help_text="Has the Business Associate Agreement been signed?"
    )
    baa_signed_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date BAA was signed"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Soft delete flag"
    )

    # Subscription & Limits
    subscription_tier = models.CharField(
        max_length=50,
        choices=SUBSCRIPTION_TIER_CHOICES,
        default=FREE,
        help_text="Subscription tier"
    )
    max_users = models.PositiveIntegerField(
        default=5,
        help_text="Maximum number of users allowed"
    )
    max_patients = models.PositiveIntegerField(
        default=50,
        help_text="Maximum number of active patients allowed"
    )

    # Feature Flags
    features_enabled = models.JSONField(
        default=dict,
        blank=True,
        help_text="Feature flags for this organization"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organizations'
        ordering = ['name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        indexes = [
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['organization_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_organization_type_display()})"

    def clean(self):
        """Custom validation logic"""
        super().clean()

        # If BAA is signed, date must be provided
        if self.business_associate_agreement_signed and not self.baa_signed_date:
            raise ValidationError({
                'baa_signed_date': 'BAA signed date is required when BAA is marked as signed'
            })

        # If BAA date is provided, BAA must be marked as signed
        if self.baa_signed_date and not self.business_associate_agreement_signed:
            raise ValidationError({
                'business_associate_agreement_signed': 'BAA must be marked as signed when date is provided'
            })

        # Schema name cannot be 'public' or 'pg_*'
        if self.schema_name in ['public', 'information_schema'] or self.schema_name.startswith('pg_'):
            raise ValidationError({
                'schema_name': 'Schema name cannot be "public", "information_schema", or start with "pg_"'
            })

    def save(self, *args, **kwargs):
        """Override save to run full_clean"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_default_features(self):
        """Return default feature flags based on subscription tier"""
        default_features = {
            'assessments_enabled': True,
            'treatment_plans_enabled': False,
            'analytics_enabled': False,
            'pdf_export_enabled': False,
            'api_access_enabled': False,
            'custom_branding_enabled': False,
            'sso_enabled': False,
        }

        if self.subscription_tier == self.PROFESSIONAL:
            default_features.update({
                'treatment_plans_enabled': True,
                'analytics_enabled': True,
                'pdf_export_enabled': True,
            })
        elif self.subscription_tier == self.ENTERPRISE:
            default_features.update({
                'treatment_plans_enabled': True,
                'analytics_enabled': True,
                'pdf_export_enabled': True,
                'api_access_enabled': True,
                'custom_branding_enabled': True,
                'sso_enabled': True,
            })

        return default_features

    def is_feature_enabled(self, feature_name):
        """Check if a specific feature is enabled for this organization"""
        if not self.features_enabled:
            self.features_enabled = self.get_default_features()
            self.save()

        return self.features_enabled.get(feature_name, False)

    def can_add_user(self):
        """Check if organization can add another user based on subscription limit"""
        # This will need to be implemented once User model exists
        # For now, just return True if under max_users
        return True  # Placeholder

    def can_add_patient(self):
        """Check if organization can add another patient based on subscription limit"""
        # This will need to be implemented once Patient model exists
        # For now, just return True if under max_patients
        return True  # Placeholder