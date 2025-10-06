import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from organizations.models import Organization


@pytest.mark.django_db
class TestOrganizationModel:
    """Test suite for Organization model"""

    def test_create_organization_with_required_fields(self):
        """Test creating an organization with only required fields"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital"
        )

        assert org.id is not None
        assert org.name == "Test Hospital"
        assert org.organization_type == Organization.HOSPITAL
        assert org.schema_name == "test_hospital"
        assert org.subdomain == "testhospital"
        assert org.is_active is True
        assert org.subscription_tier == Organization.FREE
        assert org.max_users == 5
        assert org.max_patients == 50
        assert org.business_associate_agreement_signed is False
        assert org.created_at is not None
        assert org.updated_at is not None

    def test_create_organization_with_all_fields(self):
        """Test creating an organization with all fields populated"""
        baa_date = date.today()

        org = Organization.objects.create(
            name="Comprehensive Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="comprehensive_hospital",
            subdomain="comprehensive",
            npi_number="1234567890",
            tax_id="12-3456789",
            business_associate_agreement_signed=True,
            baa_signed_date=baa_date,
            subscription_tier=Organization.ENTERPRISE,
            max_users=100,
            max_patients=1000,
            features_enabled={
                "assessments_enabled": True,
                "analytics_enabled": True
            }
        )

        assert org.npi_number == "1234567890"
        assert org.tax_id == "12-3456789"
        assert org.business_associate_agreement_signed is True
        assert org.baa_signed_date == baa_date
        assert org.subscription_tier == Organization.ENTERPRISE
        assert org.max_users == 100
        assert org.max_patients == 1000
        assert org.features_enabled["assessments_enabled"] is True

    def test_organization_str_representation(self):
        """Test string representation of organization"""
        org = Organization.objects.create(
            name="Test Clinic",
            organization_type=Organization.CLINIC,
            schema_name="test_clinic",
            subdomain="testclinic"
        )

        assert str(org) == "Test Clinic (Clinic)"

    def test_unique_schema_name_constraint(self):
        """Test that schema_name must be unique"""
        Organization.objects.create(
            name="Hospital A",
            organization_type=Organization.HOSPITAL,
            schema_name="unique_schema",
            subdomain="hospitala"
        )

        # Our model.save() calls full_clean(), which raises ValidationError for unique constraints
        with pytest.raises(ValidationError):
            Organization.objects.create(
                name="Hospital B",
                organization_type=Organization.HOSPITAL,
                schema_name="unique_schema",  # Duplicate
                subdomain="hospitalb"
            )

    def test_unique_subdomain_constraint(self):
        """Test that subdomain must be unique"""
        Organization.objects.create(
            name="Clinic A",
            organization_type=Organization.CLINIC,
            schema_name="clinic_a",
            subdomain="uniqueclinic"
        )

        # Our model.save() calls full_clean(), which raises ValidationError for unique constraints
        with pytest.raises(ValidationError):
            Organization.objects.create(
                name="Clinic B",
                organization_type=Organization.CLINIC,
                schema_name="clinic_b",
                subdomain="uniqueclinic"  # Duplicate
            )

    def test_unique_npi_number_constraint(self):
        """Test that npi_number must be unique when provided"""
        Organization.objects.create(
            name="Hospital A",
            organization_type=Organization.HOSPITAL,
            schema_name="hospital_a",
            subdomain="hospitala",
            npi_number="1234567890"
        )

        # Our model.save() calls full_clean(), which raises ValidationError for unique constraints
        with pytest.raises(ValidationError):
            Organization.objects.create(
                name="Hospital B",
                organization_type=Organization.HOSPITAL,
                schema_name="hospital_b",
                subdomain="hospitalb",
                npi_number="1234567890"  # Duplicate
            )

    def test_schema_name_format_validation(self):
        """Test schema_name format validation"""
        # Valid schema names
        valid_names = ["test_org", "org123", "my_org_2025"]
        for i, schema_name in enumerate(valid_names):
            org = Organization(
                name="Test Org",
                organization_type=Organization.CLINIC,
                schema_name=schema_name,
                subdomain=f"sub{i}"  # Use simple numeric subdomain to avoid format issues
            )
            org.full_clean()  # Should not raise

        # Invalid schema names
        invalid_names = ["Test_Org", "123org", "org-name", "public", "pg_catalog"]
        for i, schema_name in enumerate(invalid_names):
            org = Organization(
                name="Test Org",
                organization_type=Organization.CLINIC,
                schema_name=schema_name,
                subdomain=f"subdomain{i}"  # Use simple numeric subdomain
            )
            with pytest.raises(ValidationError):
                org.full_clean()

    def test_subdomain_format_validation(self):
        """Test subdomain format validation"""
        # Valid subdomains
        valid_subdomains = ["test", "test123", "test-org", "my-org-2025"]
        for i, subdomain in enumerate(valid_subdomains):
            org = Organization(
                name="Test Org",
                organization_type=Organization.CLINIC,
                schema_name=f"schema{i}",
                subdomain=subdomain
            )
            org.full_clean()  # Should not raise

        # Invalid subdomains
        invalid_subdomains = ["Test", "test_org", "-test", "test-", "TEST"]
        for subdomain in invalid_subdomains:
            org = Organization(
                name="Test Org",
                organization_type=Organization.CLINIC,
                schema_name=f"schema{subdomain}",
                subdomain=subdomain
            )
            with pytest.raises(ValidationError):
                org.full_clean()

    def test_npi_number_format_validation(self):
        """Test NPI number must be exactly 10 digits"""
        # Valid NPI
        org = Organization(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital",
            npi_number="1234567890"
        )
        org.full_clean()  # Should not raise

        # Invalid NPI numbers
        invalid_npis = ["123456789", "12345678901", "123456789A", "abc1234567"]
        for npi in invalid_npis:
            org = Organization(
                name="Test Hospital",
                organization_type=Organization.HOSPITAL,
                schema_name="test_hospital2",
                subdomain="testhospital2",
                npi_number=npi
            )
            with pytest.raises(ValidationError):
                org.full_clean()

    def test_baa_validation_signed_without_date(self):
        """Test that BAA signed requires a date"""
        org = Organization(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital",
            business_associate_agreement_signed=True,
            baa_signed_date=None
        )

        with pytest.raises(ValidationError) as exc_info:
            org.full_clean()

        assert 'baa_signed_date' in exc_info.value.error_dict

    def test_baa_validation_date_without_signed(self):
        """Test that BAA date requires signed flag to be True"""
        org = Organization(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital",
            business_associate_agreement_signed=False,
            baa_signed_date=date.today()
        )

        with pytest.raises(ValidationError) as exc_info:
            org.full_clean()

        assert 'business_associate_agreement_signed' in exc_info.value.error_dict

    def test_reserved_schema_names_rejected(self):
        """Test that reserved PostgreSQL schema names are rejected"""
        reserved_names = ['public', 'information_schema', 'pg_catalog', 'pg_temp']

        for schema_name in reserved_names:
            org = Organization(
                name="Test Org",
                organization_type=Organization.CLINIC,
                schema_name=schema_name,
                subdomain="testorg"
            )
            with pytest.raises(ValidationError) as exc_info:
                org.full_clean()

            assert 'schema_name' in exc_info.value.error_dict

    def test_get_default_features_free_tier(self):
        """Test default features for FREE tier"""
        org = Organization.objects.create(
            name="Free Clinic",
            organization_type=Organization.CLINIC,
            schema_name="free_clinic",
            subdomain="freeclinic",
            subscription_tier=Organization.FREE
        )

        features = org.get_default_features()

        assert features['assessments_enabled'] is True
        assert features['treatment_plans_enabled'] is False
        assert features['analytics_enabled'] is False
        assert features['pdf_export_enabled'] is False
        assert features['api_access_enabled'] is False
        assert features['custom_branding_enabled'] is False
        assert features['sso_enabled'] is False

    def test_get_default_features_professional_tier(self):
        """Test default features for PROFESSIONAL tier"""
        org = Organization.objects.create(
            name="Pro Clinic",
            organization_type=Organization.CLINIC,
            schema_name="pro_clinic",
            subdomain="proclinic",
            subscription_tier=Organization.PROFESSIONAL
        )

        features = org.get_default_features()

        assert features['assessments_enabled'] is True
        assert features['treatment_plans_enabled'] is True
        assert features['analytics_enabled'] is True
        assert features['pdf_export_enabled'] is True
        assert features['api_access_enabled'] is False
        assert features['custom_branding_enabled'] is False
        assert features['sso_enabled'] is False

    def test_get_default_features_enterprise_tier(self):
        """Test default features for ENTERPRISE tier"""
        org = Organization.objects.create(
            name="Enterprise Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="enterprise_hospital",
            subdomain="enterprisehospital",
            subscription_tier=Organization.ENTERPRISE
        )

        features = org.get_default_features()

        assert features['assessments_enabled'] is True
        assert features['treatment_plans_enabled'] is True
        assert features['analytics_enabled'] is True
        assert features['pdf_export_enabled'] is True
        assert features['api_access_enabled'] is True
        assert features['custom_branding_enabled'] is True
        assert features['sso_enabled'] is True

    def test_is_feature_enabled_initializes_features(self):
        """Test that is_feature_enabled initializes features if empty"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital",
            subscription_tier=Organization.PROFESSIONAL,
            features_enabled={}
        )

        # Should initialize features on first call
        result = org.is_feature_enabled('analytics_enabled')

        assert result is True
        assert org.features_enabled != {}
        assert org.features_enabled['analytics_enabled'] is True

    def test_is_feature_enabled_returns_correct_value(self):
        """Test that is_feature_enabled returns correct values"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital",
            features_enabled={
                'assessments_enabled': True,
                'custom_feature': False
            }
        )

        assert org.is_feature_enabled('assessments_enabled') is True
        assert org.is_feature_enabled('custom_feature') is False
        assert org.is_feature_enabled('nonexistent_feature') is False

    def test_organization_types(self):
        """Test all organization types can be created"""
        types = [
            Organization.HOSPITAL,
            Organization.CLINIC,
            Organization.NETWORK,
            Organization.PRIVATE_PRACTICE
        ]

        for i, org_type in enumerate(types):
            # Use simple numeric subdomain to avoid format validation issues
            org = Organization.objects.create(
                name=f"Test {org_type}",
                organization_type=org_type,
                schema_name=f"test_{org_type.replace('_', '')}_{i}",
                subdomain=f"sub{i}"
            )
            assert org.organization_type == org_type

    def test_soft_delete_with_is_active_flag(self):
        """Test soft delete functionality using is_active"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital"
        )

        assert org.is_active is True

        # Soft delete
        org.is_active = False
        org.save()

        # Verify still exists in database
        retrieved_org = Organization.objects.get(id=org.id)
        assert retrieved_org.is_active is False

    def test_timestamps_auto_update(self):
        """Test that timestamps are automatically set"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital"
        )

        created_at = org.created_at
        updated_at = org.updated_at

        assert created_at is not None
        assert updated_at is not None
        assert created_at == updated_at

        # Update and verify updated_at changes
        org.name = "Updated Hospital"
        org.save()

        assert org.updated_at > updated_at
        assert org.created_at == created_at  # Should not change

    def test_default_max_limits(self):
        """Test default max_users and max_patients values"""
        org = Organization.objects.create(
            name="Test Clinic",
            organization_type=Organization.CLINIC,
            schema_name="test_clinic",
            subdomain="testclinic"
        )

        assert org.max_users == 5
        assert org.max_patients == 50

    def test_custom_max_limits(self):
        """Test setting custom max_users and max_patients"""
        org = Organization.objects.create(
            name="Large Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="large_hospital",
            subdomain="largehospital",
            max_users=200,
            max_patients=5000
        )

        assert org.max_users == 200
        assert org.max_patients == 5000

    def test_json_field_default(self):
        """Test that features_enabled JSONField defaults to empty dict"""
        org = Organization.objects.create(
            name="Test Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="test_hospital",
            subdomain="testhospital"
        )

        assert org.features_enabled == {}

    def test_organization_ordering(self):
        """Test that organizations are ordered by name"""
        Organization.objects.create(
            name="Zebra Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="zebra_hospital",
            subdomain="zebra"
        )
        Organization.objects.create(
            name="Alpha Clinic",
            organization_type=Organization.CLINIC,
            schema_name="alpha_clinic",
            subdomain="alpha"
        )
        Organization.objects.create(
            name="Middle Hospital",
            organization_type=Organization.HOSPITAL,
            schema_name="middle_hospital",
            subdomain="middle"
        )

        orgs = list(Organization.objects.all())

        assert orgs[0].name == "Alpha Clinic"
        assert orgs[1].name == "Middle Hospital"
        assert orgs[2].name == "Zebra Hospital"
