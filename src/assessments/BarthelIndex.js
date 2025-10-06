import React, { useState } from 'react';
import { Activity, ArrowLeft, ArrowRight, Save, CheckCircle } from 'lucide-react';

const BarthelIndex = ({ onBack }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    patientName: '',
    patientId: '',
    assessmentDate: '',
    feeding: '',
    feedingNotes: '',
    bathing: '',
    bathingNotes: '',
    grooming: '',
    groomingNotes: '',
    dressing: '',
    dressingNotes: '',
    bowels: '',
    bowelsNotes: '',
    bladder: '',
    bladderNotes: '',
    toiletUse: '',
    toiletUseNotes: '',
    transfers: '',
    transfersNotes: '',
    mobility: '',
    mobilityNotes: '',
    stairs: '',
    stairsNotes: '',
    notes: ''
  });

  const assessmentCategories = [
    {
      id: 'feeding',
      title: 'Feeding',
      description: 'Assess ability to feed oneself',
      options: [
        { value: '10', label: 'Independent', description: 'Able to eat any normal food (not only soft food). Food cooked and served by others but not cut up' },
        { value: '5', label: 'Needs Help', description: 'Food cut up, but patient feeds self' },
        { value: '0', label: 'Dependent', description: 'Unable to feed self' }
      ],
      quickNotes: {
        '10': [
          'Patient feeds self independently with standard utensils',
          'Demonstrates appropriate eating pace and safety',
          'Manages all food textures without difficulty',
          'No modifications required for independent feeding'
        ],
        '5': [
          'Requires food to be cut into bite-sized pieces',
          'Benefits from adaptive utensils for independence',
          'Needs set-up but completes feeding independently',
          'Demonstrates decreased fine motor coordination affecting utensil use'
        ],
        '0': [
          'Unable to self-feed; requires total assistance',
          'Requires mod to max assist for all feeding tasks',
          'Patient demonstrates hand tremors preventing self-feeding',
          'NPO status; receiving alternate nutrition'
        ]
      }
    },
    {
      id: 'bathing',
      title: 'Bathing',
      description: 'Assess ability to bathe oneself',
      options: [
        { value: '5', label: 'Independent', description: 'May use bath, shower or take a sponge bath. Must be able to do all steps without another person being present' },
        { value: '0', label: 'Dependent', description: 'Needs help with bathing' }
      ],
      quickNotes: {
        '5': [
          'Patient bathes independently including all body parts',
          'Safely manages tub/shower transfers without assistance',
          'Completes bathing within reasonable timeframe',
          'Demonstrates appropriate safety awareness during bathing'
        ],
        '0': [
          'Requires mod to max assist for bathing tasks',
          'Unable to safely transfer in/out of tub without assistance',
          'Requires stand-by assist for safety during bathing',
          'Patient fatigues quickly requiring frequent rest breaks'
        ]
      }
    },
    {
      id: 'grooming',
      title: 'Grooming',
      description: 'Assess personal hygiene (hair, teeth, face, shaving)',
      options: [
        { value: '5', label: 'Independent', description: 'Can wash hands and face, comb hair, clean teeth, and shave' },
        { value: '0', label: 'Dependent', description: 'Needs help with personal care' }
      ],
      quickNotes: {
        '5': [
          'Patient completes all grooming tasks independently',
          'Manages oral hygiene without assistance',
          'Independently performs hair care and shaving',
          'Demonstrates good attention to personal appearance'
        ],
        '0': [
          'Requires assistance with oral hygiene tasks',
          'Unable to manage grooming tasks without verbal cues',
          'Needs mod assist for hair care and shaving',
          'Demonstrates decreased awareness of grooming needs'
        ]
      }
    },
    {
      id: 'dressing',
      title: 'Dressing',
      description: 'Assess ability to dress and undress',
      options: [
        { value: '10', label: 'Independent', description: 'Able to put on, take off, and secure all clothing. Can tie shoes unless physically unable' },
        { value: '5', label: 'Needs Help', description: 'Can do about half unaided' },
        { value: '0', label: 'Dependent', description: 'Unable to dress self' }
      ],
      quickNotes: {
        '10': [
          'Patient independently dons/doffs all clothing items',
          'Manages fasteners (buttons, zippers) without difficulty',
          'Demonstrates appropriate clothing selection',
          'Completes dressing in reasonable timeframe'
        ],
        '5': [
          'Requires assistance with lower body dressing only',
          'Needs help with fasteners but manages other tasks',
          'Benefits from adaptive equipment for partial independence',
          'Able to dress upper extremities independently'
        ],
        '0': [
          'Requires max assist for all dressing tasks',
          'Unable to sequence dressing activities',
          'Demonstrates poor balance affecting dressing safety',
          'Needs total assistance due to decreased ROM and strength'
        ]
      }
    },
    {
      id: 'bowels',
      title: 'Bowel Control',
      description: 'Assess bowel continence',
      options: [
        { value: '10', label: 'Continent', description: 'No accidents. Able to use suppository/enema if needed' },
        { value: '5', label: 'Occasional Accident', description: 'Less than once per week or needs help with suppository/enema' },
        { value: '0', label: 'Incontinent', description: 'Frequent accidents' }
      ],
      quickNotes: {
        '10': [
          'Patient maintains full bowel control',
          'Independently manages bowel routine',
          'No accidents reported during assessment period',
          'Demonstrates appropriate awareness of bowel needs'
        ],
        '5': [
          'Occasional accidents noted (less than weekly)',
          'Requires assistance with suppository management',
          'Benefits from scheduled bowel program',
          'Demonstrates improved awareness with reminders'
        ],
        '0': [
          'Frequent bowel accidents requiring management',
          'Unable to maintain bowel control',
          'Requires complete bowel care program',
          'Demonstrates decreased awareness of bowel needs'
        ]
      }
    },
    {
      id: 'bladder',
      title: 'Bladder Control',
      description: 'Assess bladder continence',
      options: [
        { value: '10', label: 'Continent', description: 'No accidents. Able to use any aids (catheter) if needed' },
        { value: '5', label: 'Occasional Accident', description: 'Less than once per day or needs help with catheter' },
        { value: '0', label: 'Incontinent', description: 'Frequent accidents or catheter and unable to manage' }
      ],
      quickNotes: {
        '10': [
          'Patient maintains full bladder control',
          'Independently manages catheter care if applicable',
          'No incontinence episodes reported',
          'Follows toileting schedule independently'
        ],
        '5': [
          'Occasional urinary accidents (less than daily)',
          'Requires assistance with catheter management',
          'Benefits from prompted toileting schedule',
          'Demonstrates urge incontinence with some awareness'
        ],
        '0': [
          'Frequent urinary incontinence requiring management',
          'Has indwelling catheter requiring total assistance',
          'Unable to maintain bladder control',
          'Requires complete continence care program'
        ]
      }
    },
    {
      id: 'toiletUse',
      title: 'Toilet Use',
      description: 'Assess ability to use toilet',
      options: [
        { value: '10', label: 'Independent', description: 'Able to get on/off, arrange clothes, clean self, and flush' },
        { value: '5', label: 'Needs Help', description: 'Needs help but can do some things alone' },
        { value: '0', label: 'Dependent', description: 'Unable to use toilet' }
      ],
      quickNotes: {
        '10': [
          'Patient manages all toileting tasks independently',
          'Safely transfers on/off toilet without assistance',
          'Completes hygiene management appropriately',
          'Maintains safety awareness during toileting'
        ],
        '5': [
          'Requires assistance with clothing management',
          'Needs help with transfers but manages hygiene',
          'Benefits from grab bars for safe transfers',
          'Requires stand-by assist for safety'
        ],
        '0': [
          'Unable to transfer to toilet without max assist',
          'Requires complete assistance with all toileting tasks',
          'Uses bedside commode with total assistance',
          'Unable to manage hygiene without help'
        ]
      }
    },
    {
      id: 'transfers',
      title: 'Transfers (Bed to Chair)',
      description: 'Assess ability to transfer',
      options: [
        { value: '15', label: 'Independent', description: 'No help needed including locking wheelchair' },
        { value: '10', label: 'Minor Help', description: 'Minimal assistance or supervision' },
        { value: '5', label: 'Major Help', description: 'Able to sit but needs max assistance to transfer' },
        { value: '0', label: 'Unable', description: 'No sitting balance; mechanical lift required' }
      ],
      quickNotes: {
        '15': [
          'Patient transfers independently to all surfaces',
          'Demonstrates safe transfer technique throughout',
          'Locks wheelchair and manages footrests appropriately',
          'Maintains excellent trunk control during transfers'
        ],
        '10': [
          'Requires minimal verbal cues for safe transfers',
          'Needs contact guard assist for safety',
          'Demonstrates mostly independent transfer ability',
          'Benefits from transfer equipment but otherwise independent'
        ],
        '5': [
          'Requires mod to max assist for transfers',
          'Able to sit but unable to stand without significant help',
          'Demonstrates poor weight-bearing ability',
          'Requires two-person assist for safe transfers'
        ],
        '0': [
          'No sitting balance; unable to assist with transfers',
          'Requires mechanical lift for all transfers',
          'Total dependence for transfer activities',
          'Unable to weight bear at all'
        ]
      }
    },
    {
      id: 'mobility',
      title: 'Mobility (Walking)',
      description: 'Assess walking ability on level surface',
      options: [
        { value: '15', label: 'Independent', description: 'Can walk 50 yards without help. May use aids except walking frame' },
        { value: '10', label: 'Walks with Help', description: 'Can walk 50 yards with help or supervision' },
        { value: '5', label: 'Wheelchair Independent', description: 'If unable to walk, can propel wheelchair 50 yards independently' },
        { value: '0', label: 'Immobile', description: 'Unable to walk or propel wheelchair' }
      ],
      quickNotes: {
        '15': [
          'Patient ambulates independently on level surfaces',
          'Walks greater than 50 yards without assistance',
          'Uses appropriate assistive device safely',
          'Demonstrates good endurance for mobility tasks'
        ],
        '10': [
          'Requires supervision for safe ambulation',
          'Needs contact guard assist for 50 yard distance',
          'Demonstrates fair endurance requiring rest breaks',
          'Benefits from assistive device with minimal help'
        ],
        '5': [
          'Independently propels wheelchair 50+ yards',
          'Manages wheelchair mobility on level surfaces',
          'Demonstrates good wheelchair safety awareness',
          'Unable to ambulate but independent in wheelchair'
        ],
        '0': [
          'Unable to ambulate or propel wheelchair',
          'Requires total assistance for all mobility',
          'No functional mobility without max assist',
          'Dependent for all mobility needs'
        ]
      }
    },
    {
      id: 'stairs',
      title: 'Stairs',
      description: 'Assess ability to climb stairs',
      options: [
        { value: '10', label: 'Independent', description: 'Can go up and down stairs safely without help. May use aids' },
        { value: '5', label: 'Needs Help', description: 'Needs help or supervision for safety' },
        { value: '0', label: 'Unable', description: 'Unable to use stairs' }
      ],
      quickNotes: {
        '10': [
          'Patient navigates stairs independently and safely',
          'Ascends/descends full flight without assistance',
          'Uses handrail appropriately for safety',
          'Demonstrates good balance and endurance on stairs'
        ],
        '5': [
          'Requires contact guard assist for stair safety',
          'Needs supervision ascending/descending stairs',
          'Demonstrates fair balance requiring stand-by assist',
          'Benefits from handrail with minimal help'
        ],
        '0': [
          'Unable to navigate stairs safely',
          'Requires max assist for any stair climbing',
          'Demonstrates poor balance precluding stair use',
          'Not appropriate for stairs at this time'
        ]
      }
    }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const calculateScore = () => {
    const score = assessmentCategories.reduce((total, cat) => {
      return total + (parseInt(formData[cat.id]) || 0);
    }, 0);
    return score;
  };

  const getScoreInterpretation = (score) => {
    if (score >= 90) return 'Independent - minimal assistance needed';
    if (score >= 60) return 'Mild dependence - requires some assistance';
    if (score >= 40) return 'Moderate dependence - requires significant assistance';
    if (score >= 20) return 'Severe dependence - requires extensive assistance';
    return 'Total dependence - requires help with all activities';
  };

  const isStepValid = () => {
    if (currentStep === 0) {
      return formData.patientName && formData.patientId && formData.assessmentDate;
    }
    if (currentStep > 0 && currentStep <= assessmentCategories.length) {
      const category = assessmentCategories[currentStep - 1];
      return formData[category.id] !== '';
    }
    return true;
  };

  const nextStep = () => {
    if (currentStep < assessmentCategories.length + 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = () => {
    const finalScore = calculateScore();
    console.log('Form submitted:', formData);
    console.log('Total Score:', finalScore);
    alert(`Assessment Complete!\nBarthel Index Score: ${finalScore}/100\n${getScoreInterpretation(finalScore)}`);
  };

  const renderPatientInfo = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-light text-neutral-900 mb-2">Patient Information</h2>
        <p className="text-neutral-500 font-light">Enter the patient details to begin the Barthel Index assessment</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-light text-neutral-700 mb-2">Patient Name</label>
          <input
            type="text"
            value={formData.patientName}
            onChange={(e) => handleInputChange('patientName', e.target.value)}
            className="w-full px-4 py-3 border border-neutral-200 focus:outline-none focus:border-emerald-600 transition-colors font-light"
            placeholder="Enter patient full name"
          />
        </div>

        <div>
          <label className="block text-sm font-light text-neutral-700 mb-2">Patient ID</label>
          <input
            type="text"
            value={formData.patientId}
            onChange={(e) => handleInputChange('patientId', e.target.value)}
            className="w-full px-4 py-3 border border-neutral-200 focus:outline-none focus:border-emerald-600 transition-colors font-light"
            placeholder="Enter patient ID"
          />
        </div>

        <div>
          <label className="block text-sm font-light text-neutral-700 mb-2">Assessment Date</label>
          <input
            type="date"
            value={formData.assessmentDate}
            onChange={(e) => handleInputChange('assessmentDate', e.target.value)}
            className="w-full px-4 py-3 border border-neutral-200 focus:outline-none focus:border-emerald-600 transition-colors font-light"
          />
        </div>
      </div>
    </div>
  );

  const renderAssessmentStep = () => {
    const category = assessmentCategories[currentStep - 1];
    const notesField = `${category.id}Notes`;

    return (
      <div className="space-y-6">
        <div>
          <div className="text-sm text-emerald-600 font-light mb-2">
            Step {currentStep} of {assessmentCategories.length}
          </div>
          <h2 className="text-3xl font-light text-neutral-900 mb-2">{category.title}</h2>
          <p className="text-neutral-500 font-light">{category.description}</p>
        </div>

        <div className="space-y-3">
          {category.options.map((option) => (
            <label
              key={option.value}
              className={`block p-6 border-2 cursor-pointer transition-all hover:bg-emerald-50/30 ${
                formData[category.id] === option.value
                  ? 'border-emerald-600 bg-emerald-50/50'
                  : 'border-neutral-200'
              }`}
            >
              <div className="flex items-start gap-4">
                <input
                  type="radio"
                  name={category.id}
                  value={option.value}
                  checked={formData[category.id] === option.value}
                  onChange={(e) => handleInputChange(category.id, e.target.value)}
                  className="mt-1 w-5 h-5 text-emerald-600"
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-neutral-900">{option.label}</span>
                    <span className="text-sm text-emerald-600 font-light">({option.value} points)</span>
                  </div>
                  <div className="text-sm text-neutral-600 font-light">{option.description}</div>
                </div>
              </div>
            </label>
          ))}
        </div>

        {/* Quick Notes Section */}
        <div className="border-t border-neutral-200 pt-6">
          <label className="block text-sm font-medium text-neutral-900 mb-3">
            Clinical Notes
            {formData[category.id] && (
              <span className="ml-2 text-xs font-light text-emerald-600">
                (Showing notes for: {category.options.find(opt => opt.value === formData[category.id])?.label})
              </span>
            )}
          </label>

          {formData[category.id] && (
            <div className="mb-4">
              <p className="text-xs text-neutral-500 font-light mb-2">Quick select common observations:</p>
              <div className="flex flex-wrap gap-2">
                {category.quickNotes[formData[category.id]].map((note, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      const currentNotes = formData[notesField];
                      const noteWithPeriod = note.endsWith('.') ? note : `${note}.`;
                      const newNote = currentNotes ? `${currentNotes} ${noteWithPeriod}` : noteWithPeriod;
                      handleInputChange(notesField, newNote);
                    }}
                    className="text-xs px-3 py-1.5 bg-neutral-100 hover:bg-emerald-100 text-neutral-700 hover:text-emerald-700 border border-neutral-200 hover:border-emerald-300 transition-all font-light text-left"
                  >
                    + {note}
                  </button>
                ))}
              </div>
            </div>
          )}

          {!formData[category.id] && (
            <div className="mb-4 p-4 bg-neutral-50 border border-neutral-200 text-sm text-neutral-600 font-light">
              Select an assessment level above to see relevant quick notes
            </div>
          )}

          <textarea
            value={formData[notesField]}
            onChange={(e) => handleInputChange(notesField, e.target.value)}
            rows={4}
            className="w-full px-4 py-3 border border-neutral-200 focus:outline-none focus:border-emerald-600 transition-colors font-light text-sm"
            placeholder="Add or edit clinical observations for this category..."
          />

          {formData[notesField] && (
            <button
              type="button"
              onClick={() => handleInputChange(notesField, '')}
              className="mt-2 text-xs text-neutral-500 hover:text-neutral-700 font-light"
            >
              Clear notes
            </button>
          )}
        </div>
      </div>
    );
  };

  const renderReview = () => {
    const score = calculateScore();

    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-light text-neutral-900 mb-2">Review Assessment</h2>
          <p className="text-neutral-500 font-light">Review the Barthel Index results before submitting</p>
        </div>

        <div className="bg-emerald-50 border-l-4 border-emerald-600 p-6">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="text-emerald-600" size={24} />
            <h3 className="text-xl font-medium text-neutral-900">Assessment Complete</h3>
          </div>
          <div className="text-3xl font-light text-emerald-600 mt-4">
            Barthel Index Score: {score}/100
          </div>
          <p className="text-sm text-neutral-600 font-light mt-2">
            {getScoreInterpretation(score)}
          </p>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-light text-neutral-900">Patient Information</h3>
          <div className="grid grid-cols-2 gap-4 bg-white border border-neutral-200 p-4">
            <div>
              <div className="text-xs text-neutral-500 font-light mb-1">Patient Name</div>
              <div className="font-medium text-neutral-900">{formData.patientName}</div>
            </div>
            <div>
              <div className="text-xs text-neutral-500 font-light mb-1">Patient ID</div>
              <div className="font-medium text-neutral-900">{formData.patientId}</div>
            </div>
            <div className="col-span-2">
              <div className="text-xs text-neutral-500 font-light mb-1">Assessment Date</div>
              <div className="font-medium text-neutral-900">{formData.assessmentDate}</div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-light text-neutral-900">Assessment Results</h3>
          <div className="space-y-4">
            {assessmentCategories.map((cat) => (
              <div key={cat.id} className="border border-neutral-200 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-neutral-900">{cat.title}</span>
                  <span className="text-emerald-600 font-medium">
                    {formData[cat.id]}/{cat.options[0].value} points
                  </span>
                </div>
                {formData[`${cat.id}Notes`] && (
                  <div className="mt-2 pt-2 border-t border-neutral-100">
                    <p className="text-xs text-neutral-500 font-light mb-1">Clinical Notes:</p>
                    <p className="text-sm text-neutral-700 font-light">{formData[`${cat.id}Notes`]}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-light text-neutral-700 mb-2">Additional Notes (Optional)</label>
          <textarea
            value={formData.notes}
            onChange={(e) => handleInputChange('notes', e.target.value)}
            rows={4}
            className="w-full px-4 py-3 border border-neutral-200 focus:outline-none focus:border-emerald-600 transition-colors font-light"
            placeholder="Add any additional observations or notes..."
          />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-emerald-600 rounded-full flex items-center justify-center">
                <Activity className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-2xl font-light tracking-tight text-neutral-900">Barthel Index</h1>
                <p className="text-sm text-emerald-600 font-light">Activities of Daily Living Assessment</p>
              </div>
            </div>
            <button
              onClick={onBack}
              className="text-neutral-500 hover:text-neutral-900 font-light flex items-center gap-2 transition-colors"
            >
              <ArrowLeft size={18} strokeWidth={1.5} />
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4">
          <div className="flex items-center gap-2">
            {[...Array(assessmentCategories.length + 2)].map((_, idx) => (
              <div
                key={idx}
                className={`h-2 flex-1 transition-all ${
                  idx <= currentStep ? 'bg-emerald-600' : 'bg-neutral-200'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Form Content */}
      <div className="max-w-4xl mx-auto px-8 py-12">
        <div className="bg-white border border-neutral-200 p-8 mb-6">
          {currentStep === 0 && renderPatientInfo()}
          {currentStep > 0 && currentStep <= assessmentCategories.length && renderAssessmentStep()}
          {currentStep === assessmentCategories.length + 1 && renderReview()}
        </div>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={`px-6 py-3 font-light flex items-center gap-2 transition-colors ${
              currentStep === 0
                ? 'text-neutral-300 cursor-not-allowed'
                : 'text-neutral-700 hover:text-neutral-900'
            }`}
          >
            <ArrowLeft size={18} strokeWidth={1.5} />
            Previous
          </button>

          {currentStep < assessmentCategories.length + 1 ? (
            <button
              onClick={nextStep}
              disabled={!isStepValid()}
              className={`px-6 py-3 font-light flex items-center gap-2 transition-colors ${
                isStepValid()
                  ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                  : 'bg-neutral-200 text-neutral-400 cursor-not-allowed'
              }`}
            >
              Next
              <ArrowRight size={18} strokeWidth={1.5} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 font-light flex items-center gap-2 transition-colors"
            >
              <Save size={18} strokeWidth={1.5} />
              Submit Assessment
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default BarthelIndex;
