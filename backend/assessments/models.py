import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import date


class BaseAssessment(models.Model):
    """
    Abstract base model for all assessment types.
    Provides common fields and functionality shared across all assessments.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.PROTECT,
        related_name='%(class)s_assessments',  # Creates katzadlassessment_assessments, etc.
        help_text="Patient being assessed"
    )

    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_conducted',
        help_text="Therapist who conducted the assessment"
    )

    # Assessment Metadata
    assessment_date = models.DateField(
        db_index=True,
        help_text="Date the assessment was conducted"
    )

    total_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Total assessment score (calculated)"
    )

    # Clinical Notes
    notes = models.TextField(
        blank=True,
        help_text="Clinical notes and observations"
    )

    goals = models.TextField(
        blank=True,
        help_text="Treatment goals based on this assessment"
    )

    recommendations = models.TextField(
        blank=True,
        help_text="Clinical recommendations"
    )

    # Status
    is_complete = models.BooleanField(
        default=True,
        help_text="Assessment is complete and finalized"
    )

    is_baseline = models.BooleanField(
        default=False,
        help_text="This is a baseline/initial assessment"
    )

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This model won't create a database table
        ordering = ['-assessment_date', '-created_at']

    def __str__(self):
        return f"{self._meta.verbose_name} - {self.patient.get_full_name()} ({self.assessment_date})"

    def clean(self):
        """Common validation for all assessments"""
        super().clean()

        # Assessment date cannot be in the future
        if self.assessment_date and self.assessment_date > date.today():
            raise ValidationError({
                'assessment_date': 'Assessment date cannot be in the future'
            })

        # Assessment date must be >= patient admission date
        if self.assessment_date and self.patient_id:
            if self.assessment_date < self.patient.admission_date:
                raise ValidationError({
                    'assessment_date': 'Assessment date cannot be before patient admission date'
                })

    def save(self, *args, **kwargs):
        """Override save to calculate total score and run validation"""
        # Calculate total score before saving
        if hasattr(self, 'calculate_total_score'):
            self.total_score = self.calculate_total_score()

        self.full_clean()
        super().save(*args, **kwargs)

    def calculate_total_score(self):
        """
        Calculate total score for the assessment.
        Must be implemented by each concrete assessment class.
        """
        raise NotImplementedError("Subclasses must implement calculate_total_score()")


# =============================================================================
# KATZ ADL ASSESSMENT
# =============================================================================

class KatzADLAssessment(BaseAssessment):
    """
    Katz Index of Independence in Activities of Daily Living (ADL)

    Measures independence in 6 basic ADL functions.
    Scoring: 0 = Dependent, 1 = Independent
    Total Score Range: 0-6 (higher is better)
    """

    # Scoring choices
    DEPENDENT = 0
    INDEPENDENT = 1

    SCORE_CHOICES = [
        (DEPENDENT, 'Dependent'),
        (INDEPENDENT, 'Independent'),
    ]

    # The 6 ADL Functions
    bathing = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Bathing: 0=Dependent, 1=Independent"
    )

    dressing = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Dressing: 0=Dependent, 1=Independent"
    )

    toileting = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Toileting: 0=Dependent, 1=Independent"
    )

    transferring = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Transferring: 0=Dependent, 1=Independent"
    )

    continence = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Continence: 0=Dependent, 1=Independent"
    )

    feeding = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Feeding: 0=Dependent, 1=Independent"
    )

    class Meta:
        db_table = 'assessments_katz_adl'
        verbose_name = 'Katz ADL Assessment'
        verbose_name_plural = 'Katz ADL Assessments'
        indexes = [
            models.Index(fields=['patient', 'assessment_date']),
            models.Index(fields=['assessment_date', 'is_baseline']),
        ]

    def calculate_total_score(self):
        """Calculate total Katz ADL score (0-6)"""
        return sum([
            self.bathing,
            self.dressing,
            self.toileting,
            self.transferring,
            self.continence,
            self.feeding
        ])

    def get_interpretation(self):
        """Return clinical interpretation of the score"""
        score = self.total_score if self.total_score is not None else self.calculate_total_score()

        if score == 6:
            return "Independent in all ADLs"
        elif score >= 4:
            return "Moderately dependent (4-5 functions independent)"
        elif score >= 2:
            return "Severely dependent (2-3 functions independent)"
        else:
            return "Very severely dependent (0-1 functions independent)"


# =============================================================================
# BARTHEL INDEX ASSESSMENT
# =============================================================================

class BarthelAssessment(BaseAssessment):
    """
    Barthel Index (BI) - Measures functional independence in ADL

    10 items with varying point scales
    Total Score Range: 0-100 (higher is better)
    """

    # Feeding
    feeding = models.IntegerField(
        choices=[
            (0, 'Unable'),
            (5, 'Needs help (e.g., cutting, spreading butter)'),
            (10, 'Independent')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Feeding ability"
    )

    # Bathing
    bathing = models.IntegerField(
        choices=[
            (0, 'Dependent'),
            (5, 'Independent (or in shower)')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Bathing ability"
    )

    # Grooming
    grooming = models.IntegerField(
        choices=[
            (0, 'Needs help with personal care'),
            (5, 'Independent (face/hair/teeth/shaving)')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Grooming ability"
    )

    # Dressing
    dressing = models.IntegerField(
        choices=[
            (0, 'Dependent'),
            (5, 'Needs help but can do about half unaided'),
            (10, 'Independent (including buttons, zips, laces)')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Dressing ability"
    )

    # Bowels
    bowels = models.IntegerField(
        choices=[
            (0, 'Incontinent (or needs enema)'),
            (5, 'Occasional accident'),
            (10, 'Continent')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Bowel control"
    )

    # Bladder
    bladder = models.IntegerField(
        choices=[
            (0, 'Incontinent or catheterized and unable to manage alone'),
            (5, 'Occasional accident'),
            (10, 'Continent')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Bladder control"
    )

    # Toilet Use
    toilet_use = models.IntegerField(
        choices=[
            (0, 'Dependent'),
            (5, 'Needs some help, but can do something alone'),
            (10, 'Independent (on and off, dressing, wiping)')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Toilet use ability"
    )

    # Transfers (bed to chair and back)
    transfers = models.IntegerField(
        choices=[
            (0, 'Unable - no sitting balance'),
            (5, 'Major help (1-2 people, physical), can sit'),
            (10, 'Minor help (verbal or physical)'),
            (15, 'Independent')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        help_text="Transfer ability"
    )

    # Mobility (on level surfaces)
    mobility = models.IntegerField(
        choices=[
            (0, 'Immobile or < 50 yards'),
            (5, 'Wheelchair independent, including corners, > 50 yards'),
            (10, 'Walks with help of one person (verbal or physical) > 50 yards'),
            (15, 'Independent (but may use aid) for > 50 yards')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        help_text="Mobility ability"
    )

    # Stairs
    stairs = models.IntegerField(
        choices=[
            (0, 'Unable'),
            (5, 'Needs help (verbal, physical, carrying aid)'),
            (10, 'Independent')
        ],
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Stair climbing ability"
    )

    class Meta:
        db_table = 'assessments_barthel'
        verbose_name = 'Barthel Index Assessment'
        verbose_name_plural = 'Barthel Index Assessments'
        indexes = [
            models.Index(fields=['patient', 'assessment_date']),
            models.Index(fields=['assessment_date', 'is_baseline']),
        ]

    def calculate_total_score(self):
        """Calculate total Barthel Index score (0-100)"""
        return sum([
            self.feeding,
            self.bathing,
            self.grooming,
            self.dressing,
            self.bowels,
            self.bladder,
            self.toilet_use,
            self.transfers,
            self.mobility,
            self.stairs
        ])

    def get_interpretation(self):
        """Return clinical interpretation of the score"""
        score = self.total_score if self.total_score is not None else self.calculate_total_score()

        if score >= 90:
            return "Independent (90-100)"
        elif score >= 60:
            return "Minimal dependence (60-89)"
        elif score >= 40:
            return "Partial dependence (40-59)"
        elif score >= 20:
            return "Very dependent (20-39)"
        else:
            return "Totally dependent (0-19)"


# =============================================================================
# FIM ASSESSMENT
# =============================================================================

class FIMAssessment(BaseAssessment):
    """
    Functional Independence Measure (FIM)

    18 items rated on a 7-point scale
    Total Score Range: 18-126 (higher is better)

    Scoring:
    7 = Complete Independence (timely, safely)
    6 = Modified Independence (device)
    5 = Supervision or setup
    4 = Minimal assistance (subject performs >= 75%)
    3 = Moderate assistance (subject performs >= 50%)
    2 = Maximal assistance (subject performs >= 25%)
    1 = Total assistance (subject performs < 25%)
    """

    # FIM Score Choices
    FIM_CHOICES = [
        (1, '1 - Total Assistance (<25%)'),
        (2, '2 - Maximal Assistance (25-49%)'),
        (3, '3 - Moderate Assistance (50-74%)'),
        (4, '4 - Minimal Assistance (75%+)'),
        (5, '5 - Supervision/Setup'),
        (6, '6 - Modified Independence (device)'),
        (7, '7 - Complete Independence'),
    ]

    # SELF-CARE (6 items)
    eating = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Eating"
    )

    grooming = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Grooming"
    )

    bathing = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Bathing"
    )

    dressing_upper = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Dressing - Upper Body"
    )

    dressing_lower = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Dressing - Lower Body"
    )

    toileting = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Toileting"
    )

    # SPHINCTER CONTROL (2 items)
    bladder_management = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Bladder Management"
    )

    bowel_management = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Bowel Management"
    )

    # TRANSFERS (3 items)
    transfer_bed_chair = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Transfer: Bed, Chair, Wheelchair"
    )

    transfer_toilet = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Transfer: Toilet"
    )

    transfer_tub_shower = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Transfer: Tub or Shower"
    )

    # LOCOMOTION (2 items)
    locomotion_walk_wheelchair = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Locomotion: Walk/Wheelchair"
    )

    locomotion_stairs = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Locomotion: Stairs"
    )

    # COMMUNICATION (2 items)
    comprehension = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Comprehension"
    )

    expression = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Expression"
    )

    # SOCIAL COGNITION (3 items)
    social_interaction = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Social Interaction"
    )

    problem_solving = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Problem Solving"
    )

    memory = models.IntegerField(
        choices=FIM_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Memory"
    )

    class Meta:
        db_table = 'assessments_fim'
        verbose_name = 'FIM Assessment'
        verbose_name_plural = 'FIM Assessments'
        indexes = [
            models.Index(fields=['patient', 'assessment_date']),
            models.Index(fields=['assessment_date', 'is_baseline']),
        ]

    def calculate_total_score(self):
        """Calculate total FIM score (18-126)"""
        return sum([
            # Self-care
            self.eating,
            self.grooming,
            self.bathing,
            self.dressing_upper,
            self.dressing_lower,
            self.toileting,
            # Sphincter control
            self.bladder_management,
            self.bowel_management,
            # Transfers
            self.transfer_bed_chair,
            self.transfer_toilet,
            self.transfer_tub_shower,
            # Locomotion
            self.locomotion_walk_wheelchair,
            self.locomotion_stairs,
            # Communication
            self.comprehension,
            self.expression,
            # Social cognition
            self.social_interaction,
            self.problem_solving,
            self.memory
        ])

    def calculate_motor_score(self):
        """Calculate motor subscore (13 items, 13-91)"""
        return sum([
            # Self-care
            self.eating,
            self.grooming,
            self.bathing,
            self.dressing_upper,
            self.dressing_lower,
            self.toileting,
            # Sphincter control
            self.bladder_management,
            self.bowel_management,
            # Transfers
            self.transfer_bed_chair,
            self.transfer_toilet,
            self.transfer_tub_shower,
            # Locomotion
            self.locomotion_walk_wheelchair,
            self.locomotion_stairs
        ])

    def calculate_cognitive_score(self):
        """Calculate cognitive subscore (5 items, 5-35)"""
        return sum([
            self.comprehension,
            self.expression,
            self.social_interaction,
            self.problem_solving,
            self.memory
        ])

    def get_interpretation(self):
        """Return clinical interpretation of the score"""
        score = self.total_score if self.total_score is not None else self.calculate_total_score()

        if score >= 108:
            return "Complete Independence (108-126)"
        elif score >= 90:
            return "Modified Independence (90-107)"
        elif score >= 54:
            return "Modified Dependence (54-89)"
        else:
            return "Complete Dependence (18-53)"
