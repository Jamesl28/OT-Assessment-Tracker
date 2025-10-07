import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from assessments.models import KatzADLAssessment, BarthelAssessment, FIMAssessment
from patients.models import Patient
from users.models import User


@pytest.fixture
def test_user(db):
    """Create a test OT user"""
    return User.objects.create_user(
        email='ot@example.com',
        password='testpass123',
        username='ot1',
        first_name='Jane',
        last_name='Therapist',
        role=User.OT,
        license_number='OT123',
        license_expiry_date=date.today() + timedelta(days=365)
    )


@pytest.fixture
def test_patient(db, test_user):
    """Create a test patient"""
    return Patient.objects.create(
        medical_record_number='MRN001',
        first_name='John',
        last_name='Doe',
        date_of_birth=date(1950, 1, 1),
        gender=Patient.MALE,
        primary_diagnosis='Stroke',
        admission_date=date.today() - timedelta(days=10),
        created_by=test_user
    )


# =============================================================================
# KATZ ADL ASSESSMENT TESTS
# =============================================================================

@pytest.mark.django_db
class TestKatzADLAssessment:
    """Test suite for Katz ADL Assessment"""

    def test_create_katz_assessment_all_independent(self, test_patient, test_user):
        """Test creating Katz assessment with all independent scores"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=KatzADLAssessment.INDEPENDENT,
            dressing=KatzADLAssessment.INDEPENDENT,
            toileting=KatzADLAssessment.INDEPENDENT,
            transferring=KatzADLAssessment.INDEPENDENT,
            continence=KatzADLAssessment.INDEPENDENT,
            feeding=KatzADLAssessment.INDEPENDENT
        )

        assert assessment.id is not None
        assert assessment.total_score == 6
        assert assessment.get_interpretation() == "Independent in all ADLs"

    def test_create_katz_assessment_all_dependent(self, test_patient, test_user):
        """Test creating Katz assessment with all dependent scores"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=KatzADLAssessment.DEPENDENT,
            dressing=KatzADLAssessment.DEPENDENT,
            toileting=KatzADLAssessment.DEPENDENT,
            transferring=KatzADLAssessment.DEPENDENT,
            continence=KatzADLAssessment.DEPENDENT,
            feeding=KatzADLAssessment.DEPENDENT
        )

        assert assessment.total_score == 0
        assert "Very severely dependent" in assessment.get_interpretation()

    def test_katz_score_calculation(self, test_patient, test_user):
        """Test Katz total score calculation"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1,
            dressing=1,
            toileting=0,
            transferring=1,
            continence=0,
            feeding=1
        )

        assert assessment.total_score == 4
        assert "Moderately dependent" in assessment.get_interpretation()

    def test_katz_str_representation(self, test_patient, test_user):
        """Test string representation"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        assert str(assessment) == f"Katz ADL Assessment - John Doe ({date.today()})"

    def test_katz_baseline_flag(self, test_patient, test_user):
        """Test baseline flag"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1,
            is_baseline=True
        )

        assert assessment.is_baseline is True

    def test_katz_with_clinical_notes(self, test_patient, test_user):
        """Test assessment with clinical notes"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1, dressing=0, toileting=1,
            transferring=1, continence=1, feeding=1,
            notes="Patient requires assistance with dressing due to limited ROM",
            goals="Increase independence in dressing",
            recommendations="Continue OT 3x/week focusing on UE strengthening"
        )

        assert "ROM" in assessment.notes
        assert "independence" in assessment.goals
        assert "OT" in assessment.recommendations


# =============================================================================
# BARTHEL INDEX ASSESSMENT TESTS
# =============================================================================

@pytest.mark.django_db
class TestBarthelAssessment:
    """Test suite for Barthel Index Assessment"""

    def test_create_barthel_assessment_max_score(self, test_patient, test_user):
        """Test creating Barthel with maximum independence (100)"""
        assessment = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=10,
            bathing=5,
            grooming=5,
            dressing=10,
            bowels=10,
            bladder=10,
            toilet_use=10,
            transfers=15,
            mobility=15,
            stairs=10
        )

        assert assessment.total_score == 100
        assert assessment.get_interpretation() == "Independent (90-100)"

    def test_create_barthel_assessment_min_score(self, test_patient, test_user):
        """Test creating Barthel with minimum score (0)"""
        assessment = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=0,
            bathing=0,
            grooming=0,
            dressing=0,
            bowels=0,
            bladder=0,
            toilet_use=0,
            transfers=0,
            mobility=0,
            stairs=0
        )

        assert assessment.total_score == 0
        assert "Totally dependent" in assessment.get_interpretation()

    def test_barthel_score_calculation(self, test_patient, test_user):
        """Test Barthel score calculation with mixed values"""
        assessment = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=5,
            bathing=5,
            grooming=5,
            dressing=5,
            bowels=5,
            bladder=5,
            toilet_use=5,
            transfers=10,
            mobility=10,
            stairs=5
        )

        assert assessment.total_score == 60
        assert "Minimal dependence" in assessment.get_interpretation()

    def test_barthel_interpretations(self, test_patient, test_user):
        """Test all Barthel interpretation levels"""
        # Test each interpretation level with simpler scoring
        test_cases = [
            (100, "Independent"),  # Max score
            (75, "Minimal dependence"),
            (50, "Partial dependence"),
            (30, "Very dependent"),
            (10, "Totally dependent")
        ]

        for i, (score, expected_interp) in enumerate(test_cases):
            # Create assessment with simple distribution to hit target score
            if score == 100:
                assessment = BarthelAssessment.objects.create(
                    patient=test_patient, assessed_by=test_user,
                    assessment_date=date.today() - timedelta(days=i),
                    feeding=10, bathing=5, grooming=5, dressing=10,
                    bowels=10, bladder=10, toilet_use=10,
                    transfers=15, mobility=15, stairs=10
                )
            elif score == 75:
                assessment = BarthelAssessment.objects.create(
                    patient=test_patient, assessed_by=test_user,
                    assessment_date=date.today() - timedelta(days=i),
                    feeding=10, bathing=5, grooming=5, dressing=10,
                    bowels=10, bladder=10, toilet_use=10,
                    transfers=10, mobility=5, stairs=0
                )
            elif score == 50:
                assessment = BarthelAssessment.objects.create(
                    patient=test_patient, assessed_by=test_user,
                    assessment_date=date.today() - timedelta(days=i),
                    feeding=5, bathing=5, grooming=5, dressing=5,
                    bowels=5, bladder=5, toilet_use=5,
                    transfers=5, mobility=5, stairs=5
                )
            elif score == 30:
                assessment = BarthelAssessment.objects.create(
                    patient=test_patient, assessed_by=test_user,
                    assessment_date=date.today() - timedelta(days=i),
                    feeding=5, bathing=0, grooming=5, dressing=0,
                    bowels=5, bladder=5, toilet_use=0,
                    transfers=5, mobility=5, stairs=0
                )
            else:  # score == 10
                assessment = BarthelAssessment.objects.create(
                    patient=test_patient, assessed_by=test_user,
                    assessment_date=date.today() - timedelta(days=i),
                    feeding=0, bathing=0, grooming=5, dressing=0,
                    bowels=0, bladder=5, toilet_use=0,
                    transfers=0, mobility=0, stairs=0
                )

            assert expected_interp in assessment.get_interpretation()

    def test_barthel_ordering(self, test_patient, test_user):
        """Test that assessments are ordered by date descending"""
        assessment1 = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today() - timedelta(days=2),
            feeding=10, bathing=5, grooming=5, dressing=10,
            bowels=10, bladder=10, toilet_use=10,
            transfers=15, mobility=15, stairs=10
        )

        assessment2 = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=10, bathing=5, grooming=5, dressing=10,
            bowels=10, bladder=10, toilet_use=10,
            transfers=15, mobility=15, stairs=10
        )

        # Filter by patient to avoid interference from other tests
        assessments = list(BarthelAssessment.objects.filter(patient=test_patient).order_by('-assessment_date', '-created_at'))
        assert assessments[0] == assessment2  # Most recent first
        assert assessments[1] == assessment1


# =============================================================================
# FIM ASSESSMENT TESTS
# =============================================================================

@pytest.mark.django_db
class TestFIMAssessment:
    """Test suite for FIM Assessment"""

    def test_create_fim_assessment_max_score(self, test_patient, test_user):
        """Test creating FIM with maximum independence (126)"""
        assessment = FIMAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            # Self-care
            eating=7, grooming=7, bathing=7,
            dressing_upper=7, dressing_lower=7, toileting=7,
            # Sphincter
            bladder_management=7, bowel_management=7,
            # Transfers
            transfer_bed_chair=7, transfer_toilet=7, transfer_tub_shower=7,
            # Locomotion
            locomotion_walk_wheelchair=7, locomotion_stairs=7,
            # Communication
            comprehension=7, expression=7,
            # Social cognition
            social_interaction=7, problem_solving=7, memory=7
        )

        assert assessment.total_score == 126
        assert assessment.get_interpretation() == "Complete Independence (108-126)"

    def test_create_fim_assessment_min_score(self, test_patient, test_user):
        """Test creating FIM with minimum score (18)"""
        assessment = FIMAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            # Self-care
            eating=1, grooming=1, bathing=1,
            dressing_upper=1, dressing_lower=1, toileting=1,
            # Sphincter
            bladder_management=1, bowel_management=1,
            # Transfers
            transfer_bed_chair=1, transfer_toilet=1, transfer_tub_shower=1,
            # Locomotion
            locomotion_walk_wheelchair=1, locomotion_stairs=1,
            # Communication
            comprehension=1, expression=1,
            # Social cognition
            social_interaction=1, problem_solving=1, memory=1
        )

        assert assessment.total_score == 18
        assert "Complete Dependence" in assessment.get_interpretation()

    def test_fim_motor_subscore(self, test_patient, test_user):
        """Test FIM motor subscore calculation"""
        assessment = FIMAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            # Motor items = 7 each (13 items)
            eating=7, grooming=7, bathing=7,
            dressing_upper=7, dressing_lower=7, toileting=7,
            bladder_management=7, bowel_management=7,
            transfer_bed_chair=7, transfer_toilet=7, transfer_tub_shower=7,
            locomotion_walk_wheelchair=7, locomotion_stairs=7,
            # Cognitive items = 1 each (5 items)
            comprehension=1, expression=1,
            social_interaction=1, problem_solving=1, memory=1
        )

        motor_score = assessment.calculate_motor_score()
        assert motor_score == 91  # 13 items * 7

    def test_fim_cognitive_subscore(self, test_patient, test_user):
        """Test FIM cognitive subscore calculation"""
        assessment = FIMAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            # Motor items = 1 each (13 items)
            eating=1, grooming=1, bathing=1,
            dressing_upper=1, dressing_lower=1, toileting=1,
            bladder_management=1, bowel_management=1,
            transfer_bed_chair=1, transfer_toilet=1, transfer_tub_shower=1,
            locomotion_walk_wheelchair=1, locomotion_stairs=1,
            # Cognitive items = 7 each (5 items)
            comprehension=7, expression=7,
            social_interaction=7, problem_solving=7, memory=7
        )

        cognitive_score = assessment.calculate_cognitive_score()
        assert cognitive_score == 35  # 5 items * 7

    def test_fim_mixed_scores(self, test_patient, test_user):
        """Test FIM with mixed functional levels"""
        assessment = FIMAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            # Self-care: Mix of scores
            eating=6, grooming=5, bathing=4,
            dressing_upper=5, dressing_lower=4, toileting=5,
            # Sphincter
            bladder_management=6, bowel_management=6,
            # Transfers
            transfer_bed_chair=4, transfer_toilet=4, transfer_tub_shower=3,
            # Locomotion
            locomotion_walk_wheelchair=4, locomotion_stairs=3,
            # Communication
            comprehension=6, expression=6,
            # Social cognition
            social_interaction=5, problem_solving=5, memory=5
        )

        # 6+5+4+5+4+5+6+6+4+4+3+4+3+6+6+5+5+5 = 86
        assert assessment.total_score == 86
        assert "Modified Dependence" in assessment.get_interpretation()

    def test_fim_all_interpretations(self, test_patient, test_user):
        """Test all FIM interpretation levels"""
        test_cases = [
            (120, "Complete Independence"),
            (95, "Modified Independence"),
            (70, "Modified Dependence"),
            (40, "Complete Dependence")
        ]

        for i, (score, expected) in enumerate(test_cases):
            # Create simplified assessment
            avg_score = score // 18
            assessment = FIMAssessment.objects.create(
                patient=test_patient,
                assessed_by=test_user,
                assessment_date=date.today() - timedelta(days=i),
                eating=avg_score, grooming=avg_score, bathing=avg_score,
                dressing_upper=avg_score, dressing_lower=avg_score, toileting=avg_score,
                bladder_management=avg_score, bowel_management=avg_score,
                transfer_bed_chair=avg_score, transfer_toilet=avg_score, transfer_tub_shower=avg_score,
                locomotion_walk_wheelchair=avg_score, locomotion_stairs=avg_score,
                comprehension=avg_score, expression=avg_score,
                social_interaction=avg_score, problem_solving=avg_score, memory=avg_score
            )

            assert expected in assessment.get_interpretation()


# =============================================================================
# SHARED ASSESSMENT VALIDATION TESTS
# =============================================================================

@pytest.mark.django_db
class TestAssessmentValidation:
    """Test validation rules shared across all assessments"""

    def test_assessment_date_cannot_be_future(self, test_patient, test_user):
        """Test that assessment date cannot be in the future"""
        assessment = KatzADLAssessment(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today() + timedelta(days=1),  # Future
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        with pytest.raises(ValidationError) as exc_info:
            assessment.full_clean()

        assert 'assessment_date' in exc_info.value.error_dict

    def test_assessment_date_cannot_be_before_admission(self, test_patient, test_user):
        """Test that assessment date must be >= admission date"""
        assessment = KatzADLAssessment(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=test_patient.admission_date - timedelta(days=1),  # Before admission
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        with pytest.raises(ValidationError) as exc_info:
            assessment.full_clean()

        assert 'assessment_date' in exc_info.value.error_dict

    def test_assessment_with_valid_dates(self, test_patient, test_user):
        """Test assessment with valid dates"""
        assessment = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=test_patient.admission_date + timedelta(days=1),
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        assert assessment.assessment_date > test_patient.admission_date
        assert assessment.assessment_date <= date.today()

    def test_incomplete_assessment(self, test_patient, test_user):
        """Test creating incomplete assessment"""
        assessment = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=10, bathing=5, grooming=5, dressing=10,
            bowels=10, bladder=10, toilet_use=10,
            transfers=15, mobility=15, stairs=10,
            is_complete=False
        )

        assert assessment.is_complete is False

    def test_multiple_assessments_same_patient(self, test_patient, test_user):
        """Test creating multiple assessments for same patient"""
        assessment1 = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today() - timedelta(days=5),
            bathing=0, dressing=0, toileting=0,
            transferring=0, continence=0, feeding=0,
            is_baseline=True
        )

        assessment2 = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        # Both should exist
        assert KatzADLAssessment.objects.filter(patient=test_patient).count() == 2
        # Should show improvement
        assert assessment2.total_score > assessment1.total_score

    def test_assessment_related_names(self, test_patient, test_user):
        """Test reverse relationships work correctly"""
        katz = KatzADLAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            bathing=1, dressing=1, toileting=1,
            transferring=1, continence=1, feeding=1
        )

        # Test patient relationship
        assert katz in test_patient.katzadlassessment_assessments.all()

        # Test assessed_by relationship
        assert katz in test_user.katzadlassessment_conducted.all()

    def test_assessment_timestamps(self, test_patient, test_user):
        """Test that timestamps are set correctly"""
        import time

        assessment = BarthelAssessment.objects.create(
            patient=test_patient,
            assessed_by=test_user,
            assessment_date=date.today(),
            feeding=10, bathing=5, grooming=5, dressing=10,
            bowels=10, bladder=10, toilet_use=10,
            transfers=15, mobility=15, stairs=10
        )

        assert assessment.created_at is not None
        assert assessment.updated_at is not None

        # Update and verify updated_at changes
        old_updated = assessment.updated_at
        time.sleep(0.01)  # Small delay to ensure timestamp difference
        assessment.notes = "Updated notes"
        assessment.save()

        assert assessment.updated_at >= old_updated
