import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User, UserManager


@pytest.mark.django_db
class TestUserManager:
    """Test suite for custom UserManager"""

    def test_create_user_with_email_and_password(self):
        """Test creating a user with email and password"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.check_password('testpass123')
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError"""
        with pytest.raises(ValueError, match='The Email field must be set'):
            User.objects.create_user(
                email='',
                password='testpass123',
                username='testuser',
                first_name='Test',
                last_name='User'
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            username='admin',
            first_name='Admin',
            last_name='User'
        )

        assert user.email == 'admin@example.com'
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True
        assert user.role == User.ADMIN


@pytest.mark.django_db
class TestUserModel:
    """Test suite for User model"""

    def test_create_user_with_required_fields(self):
        """Test creating a user with only required fields"""
        user = User.objects.create_user(
            email='therapist@example.com',
            password='securepass123',
            username='therapist1',
            first_name='Jane',
            last_name='Doe'
        )

        assert user.id is not None
        assert user.email == 'therapist@example.com'
        assert user.username == 'therapist1'
        assert user.first_name == 'Jane'
        assert user.last_name == 'Doe'
        assert user.is_active is True
        assert user.role == User.VIEWER  # Default role
        assert user.specialization == User.GENERAL  # Default specialization
        assert user.failed_login_attempts == 0
        assert user.two_factor_enabled is False

    def test_create_ot_with_license(self):
        """Test creating an OT user with license information"""
        user = User.objects.create_user(
            email='ot@example.com',
            password='securepass123',
            username='ot1',
            first_name='John',
            last_name='Smith',
            role=User.OT,
            license_number='OT123456',
            license_state='CA',
            license_expiry_date=date.today() + timedelta(days=365),
            npi_number='1234567890',
            specialization=User.GERIATRICS
        )

        assert user.role == User.OT
        assert user.license_number == 'OT123456'
        assert user.license_state == 'CA'
        assert user.npi_number == '1234567890'
        assert user.specialization == User.GERIATRICS

    def test_user_str_representation(self):
        """Test string representation of user"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Alice',
            last_name='Johnson'
        )

        assert str(user) == 'Alice Johnson (test@example.com)'

    def test_get_full_name(self):
        """Test get_full_name method"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Bob',
            last_name='Williams'
        )

        assert user.get_full_name() == 'Bob Williams'

    def test_get_short_name(self):
        """Test get_short_name method"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Charlie',
            last_name='Brown'
        )

        assert user.get_short_name() == 'Charlie'

    def test_email_normalization(self):
        """Test that email is normalized to lowercase"""
        user = User.objects.create_user(
            email='TEST@EXAMPLE.COM',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        assert user.email == 'test@example.com'

    def test_unique_email_constraint(self):
        """Test that email must be unique"""
        User.objects.create_user(
            email='unique@example.com',
            password='pass123',
            username='user1',
            first_name='User',
            last_name='One'
        )

        with pytest.raises(ValidationError):
            User.objects.create_user(
                email='unique@example.com',  # Duplicate
                password='pass456',
                username='user2',
                first_name='User',
                last_name='Two'
            )

    def test_unique_username_constraint(self):
        """Test that username must be unique"""
        User.objects.create_user(
            email='user1@example.com',
            password='pass123',
            username='uniqueuser',
            first_name='User',
            last_name='One'
        )

        with pytest.raises(ValidationError):
            User.objects.create_user(
                email='user2@example.com',
                password='pass456',
                username='uniqueuser',  # Duplicate
                first_name='User',
                last_name='Two'
            )

    def test_ot_requires_license_number(self):
        """Test that OT role requires license number"""
        user = User(
            email='ot@example.com',
            username='ot1',
            first_name='OT',
            last_name='Therapist',
            role=User.OT,
            is_active=True
            # Missing license_number and license_expiry_date
        )

        with pytest.raises(ValidationError) as exc_info:
            user.full_clean()

        assert 'license_number' in exc_info.value.error_dict

    def test_ot_requires_license_expiry_date(self):
        """Test that OT role requires license expiry date"""
        user = User(
            email='ot@example.com',
            username='ot1',
            first_name='OT',
            last_name='Therapist',
            role=User.OT,
            license_number='OT123',
            is_active=True
            # Missing license_expiry_date
        )

        with pytest.raises(ValidationError) as exc_info:
            user.full_clean()

        assert 'license_expiry_date' in exc_info.value.error_dict

    def test_expired_license_validation(self):
        """Test that expired license raises validation error"""
        user = User(
            email='ot@example.com',
            username='ot1',
            first_name='OT',
            last_name='Therapist',
            role=User.OT,
            license_number='OT123',
            license_expiry_date=date.today() - timedelta(days=1),  # Expired
            is_active=True
        )

        with pytest.raises(ValidationError) as exc_info:
            user.full_clean()

        assert 'license_expiry_date' in exc_info.value.error_dict

    def test_admin_does_not_require_license(self):
        """Test that admin role does not require license"""
        user = User.objects.create_user(
            email='admin@example.com',
            password='pass123',
            username='admin1',
            first_name='Admin',
            last_name='User',
            role=User.ADMIN,
            is_active=True
            # No license required
        )

        assert user.role == User.ADMIN
        assert user.license_number == ''

    def test_increment_failed_login(self):
        """Test incrementing failed login attempts"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        assert user.failed_login_attempts == 0

        user.increment_failed_login()
        user.refresh_from_db()
        assert user.failed_login_attempts == 1

        user.increment_failed_login()
        user.refresh_from_db()
        assert user.failed_login_attempts == 2

    def test_account_locked_after_5_failed_attempts(self):
        """Test that account is locked after 5 failed login attempts"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        for _ in range(5):
            user.increment_failed_login()
            user.refresh_from_db()

        assert user.failed_login_attempts == 5
        assert user.account_locked_until is not None
        assert user.is_account_locked() is True

    def test_reset_failed_login_attempts(self):
        """Test resetting failed login attempts on successful login"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        user.failed_login_attempts = 3
        user.save()

        user.reset_failed_login_attempts()
        user.refresh_from_db()

        assert user.failed_login_attempts == 0
        assert user.account_locked_until is None
        assert user.last_login is not None
        assert user.last_activity is not None

    def test_is_account_locked_returns_false_when_not_locked(self):
        """Test is_account_locked returns False when account is not locked"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        assert user.is_account_locked() is False

    def test_is_account_locked_auto_unlocks_after_timeout(self):
        """Test that account auto-unlocks after timeout period"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        # Lock account in the past
        user.account_locked_until = timezone.now() - timedelta(minutes=1)
        user.save()

        # Should auto-unlock
        assert user.is_account_locked() is False

        user.refresh_from_db()
        assert user.account_locked_until is None
        assert user.failed_login_attempts == 0

    def test_lock_account(self):
        """Test manually locking account"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        user.lock_account(minutes=15)
        user.refresh_from_db()

        assert user.account_locked_until is not None
        assert user.is_account_locked() is True

    def test_is_session_expired(self):
        """Test session expiration logic"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        # No activity - should be expired
        assert user.is_session_expired() is True

        # Recent activity - should not be expired
        user.last_activity = timezone.now()
        user.save()
        assert user.is_session_expired() is False

        # Old activity - should be expired
        user.last_activity = timezone.now() - timedelta(minutes=20)
        user.save()
        assert user.is_session_expired() is True

    def test_update_activity(self):
        """Test updating last activity timestamp"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        old_activity = user.last_activity
        user.update_activity()
        user.refresh_from_db()

        assert user.last_activity is not None
        assert user.last_activity != old_activity

    def test_is_password_expired_no_last_changed(self):
        """Test password expiration when never changed"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        # Password_last_changed should be set automatically
        assert user.password_last_changed is not None
        assert user.is_password_expired(days=90) is False

    def test_is_password_expired_old_password(self):
        """Test password expiration for old password"""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        # Set password changed date to 100 days ago
        user.password_last_changed = timezone.now() - timedelta(days=100)
        user.save()

        assert user.is_password_expired(days=90) is True

    def test_has_role(self):
        """Test has_role method"""
        user = User.objects.create_user(
            email='ot@example.com',
            password='pass123',
            username='ot1',
            first_name='OT',
            last_name='User',
            role=User.OT,
            license_number='OT123',
            license_expiry_date=date.today() + timedelta(days=365)
        )

        assert user.has_role(User.OT) is True
        assert user.has_role(User.ADMIN) is False

    def test_is_clinician(self):
        """Test is_clinician method"""
        ot_user = User.objects.create_user(
            email='ot@example.com',
            password='pass123',
            username='ot1',
            first_name='OT',
            last_name='User',
            role=User.OT,
            license_number='OT123',
            license_expiry_date=date.today() + timedelta(days=365)
        )

        ota_user = User.objects.create_user(
            email='ota@example.com',
            password='pass123',
            username='ota1',
            first_name='OTA',
            last_name='User',
            role=User.OTA,
            license_number='OTA123',
            license_expiry_date=date.today() + timedelta(days=365)
        )

        admin_user = User.objects.create_user(
            email='admin@example.com',
            password='pass123',
            username='admin1',
            first_name='Admin',
            last_name='User',
            role=User.ADMIN
        )

        assert ot_user.is_clinician() is True
        assert ota_user.is_clinician() is True
        assert admin_user.is_clinician() is False

    def test_is_license_expiring_soon(self):
        """Test license expiration warning"""
        user = User.objects.create_user(
            email='ot@example.com',
            password='pass123',
            username='ot1',
            first_name='OT',
            last_name='User',
            role=User.OT,
            license_number='OT123',
            license_expiry_date=date.today() + timedelta(days=15)
        )

        assert user.is_license_expiring_soon(days=30) is True
        assert user.is_license_expiring_soon(days=10) is False

    def test_user_with_all_roles(self):
        """Test creating users with all available roles"""
        roles = [User.ADMIN, User.OT, User.OTA, User.SUPERVISOR, User.VIEWER]

        for i, role in enumerate(roles):
            if role in [User.OT, User.OTA]:
                user = User.objects.create_user(
                    email=f'{role}{i}@example.com',
                    password='pass123',
                    username=f'{role}{i}',
                    first_name='Test',
                    last_name='User',
                    role=role,
                    license_number=f'LIC{i}',
                    license_expiry_date=date.today() + timedelta(days=365)
                )
            else:
                user = User.objects.create_user(
                    email=f'{role}{i}@example.com',
                    password='pass123',
                    username=f'{role}{i}',
                    first_name='Test',
                    last_name='User',
                    role=role
                )

            assert user.role == role

    def test_user_with_all_specializations(self):
        """Test creating users with all specializations"""
        specializations = [
            User.GERIATRICS,
            User.PEDIATRICS,
            User.NEURO,
            User.ORTHOPEDIC,
            User.HAND,
            User.GENERAL
        ]

        for i, spec in enumerate(specializations):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                password='pass123',
                username=f'user{i}',
                first_name='Test',
                last_name='User',
                specialization=spec
            )

            assert user.specialization == spec

    def test_password_hashing(self):
        """Test that passwords are hashed, not stored in plaintext"""
        user = User.objects.create_user(
            email='test@example.com',
            password='myplainpassword',
            username='testuser',
            first_name='Test',
            last_name='User'
        )

        # Password should be hashed
        assert user.password != 'myplainpassword'
        # But check_password should work
        assert user.check_password('myplainpassword') is True
        assert user.check_password('wrongpassword') is False

    def test_created_by_audit_trail(self):
        """Test created_by audit trail"""
        admin = User.objects.create_user(
            email='admin@example.com',
            password='pass123',
            username='admin',
            first_name='Admin',
            last_name='User',
            role=User.ADMIN
        )

        new_user = User.objects.create_user(
            email='newuser@example.com',
            password='pass123',
            username='newuser',
            first_name='New',
            last_name='User',
            created_by=admin
        )

        assert new_user.created_by == admin

    def test_user_ordering(self):
        """Test that users are ordered by last name, then first name"""
        User.objects.create_user(
            email='zebra@example.com',
            password='pass123',
            username='zebra',
            first_name='Zebra',
            last_name='Zoo'
        )
        User.objects.create_user(
            email='alice@example.com',
            password='pass123',
            username='alice',
            first_name='Alice',
            last_name='Anderson'
        )
        User.objects.create_user(
            email='bob@example.com',
            password='pass123',
            username='bob',
            first_name='Bob',
            last_name='Anderson'
        )

        users = list(User.objects.all())

        assert users[0].last_name == 'Anderson'
        assert users[0].first_name == 'Alice'
        assert users[1].last_name == 'Anderson'
        assert users[1].first_name == 'Bob'
        assert users[2].last_name == 'Zoo'

    def test_npi_number_format_validation(self):
        """Test NPI number format validation"""
        # Valid NPI
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123',
            username='testuser',
            first_name='Test',
            last_name='User',
            npi_number='1234567890'
        )
        assert user.npi_number == '1234567890'

        # Invalid NPI
        invalid_npis = ['123456789', '12345678901', '123456789A']
        for i, npi in enumerate(invalid_npis):
            user = User(
                email=f'test{i}@example.com',
                username=f'testuser{i}',
                first_name='Test',
                last_name='User',
                npi_number=npi
            )
            user.set_password('pass123')  # Set password to avoid validation error
            with pytest.raises(ValidationError):
                user.full_clean()

    def test_license_state_format_validation(self):
        """Test license state format validation"""
        # Valid state codes
        valid_states = ['CA', 'NY', 'TX']
        for state in valid_states:
            user = User.objects.create_user(
                email=f'test{state}@example.com',
                password='pass123',
                username=f'testuser{state}',
                first_name='Test',
                last_name='User',
                license_state=state
            )
            assert user.license_state == state

        # Invalid state codes
        invalid_states = ['ca', 'CAL', 'C', '12']
        for i, state in enumerate(invalid_states):
            user = User(
                email=f'test{i}@example.com',
                username=f'testuser{i}',
                first_name='Test',
                last_name='User',
                license_state=state
            )
            user.set_password('pass123')  # Set password to avoid validation error
            with pytest.raises(ValidationError):
                user.full_clean()
