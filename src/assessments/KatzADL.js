import React, { useState } from 'react';
import { Activity, ArrowLeft, ArrowRight, Save, CheckCircle, User, Calendar } from 'lucide-react';

const KatzADL = ({ onBack }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState({});
  const [notes, setNotes] = useState({});

  const categories = [
    {
      id: 'bathing',
      title: 'Bathing',
      description: 'Ability to bathe oneself',
      options: [
        { value: 1, label: 'Independent', description: 'Bathes self completely or needs help in bathing only a single part of the body' },
        { value: 0, label: 'Dependent', description: 'Needs help with bathing more than one part of the body, getting in or out of the tub or shower' }
      ],
      quickNotes: {
        1: [
          'Patient independently completes bathing with no assistance',
          'Demonstrates safe transfers in/out of shower',
          'Requires setup only for bathing tasks',
          'Uses adaptive equipment independently for bathing'
        ],
        0: [
          'Requires moderate assistance for bathing activities',
          'Unable to safely transfer in/out of shower without help',
          'Needs physical assistance with upper/lower body washing',
          'Cognitive deficits impact bathing safety and completion'
        ]
      }
    },
    {
      id: 'dressing',
      title: 'Dressing',
      description: 'Ability to dress oneself',
      options: [
        { value: 1, label: 'Independent', description: 'Gets clothes and dresses without any help except tying shoes' },
        { value: 0, label: 'Dependent', description: 'Needs help with dressing or needs to be completely dressed' }
      ],
      quickNotes: {
        1: [
          'Patient dresses independently with minimal time required',
          'Successfully uses adaptive equipment for dressing',
          'Demonstrates good problem-solving for fasteners',
          'Completes upper and lower body dressing without assistance'
        ],
        0: [
          'Requires assistance with upper body dressing',
          'Unable to manage fasteners or buttons',
          'Needs help with lower body dressing due to balance deficits',
          'Requires verbal cues for sequencing of dressing tasks'
        ]
      }
    },
    {
      id: 'toileting',
      title: 'Toileting',
      description: 'Ability to use the toilet',
      options: [
        { value: 1, label: 'Independent', description: 'Goes to toilet, uses toilet, arranges clothes, and returns without any help' },
        { value: 0, label: 'Dependent', description: 'Needs help transferring to the toilet, cleaning self, or using bedpan/commode' }
      ],
      quickNotes: {
        1: [
          'Independently manages all aspects of toileting',
          'Transfers safely to/from toilet without assistance',
          'Manages clothing and hygiene independently',
          'No accidents or incontinence issues noted'
        ],
        0: [
          'Requires assistance with transfers to/from toilet',
          'Needs help managing clothing during toileting',
          'Occasional incontinence noted',
          'Requires standby assistance for safety during toileting'
        ]
      }
    },
    {
      id: 'transferring',
      title: 'Transferring',
      description: 'Ability to move in and out of bed/chair',
      options: [
        { value: 1, label: 'Independent', description: 'Moves in and out of bed or chair without help' },
        { value: 0, label: 'Dependent', description: 'Needs help in moving from bed to chair or requires a complete transfer' }
      ],
      quickNotes: {
        1: [
          'Performs bed mobility independently',
          'Transfers safely without assistive devices',
          'Demonstrates good body mechanics during transfers',
          'No fall risk noted during transfers'
        ],
        0: [
          'Requires moderate assistance for bed-to-chair transfers',
          'Uses assistive device for safe transfers',
          'Needs verbal cuing for safe transfer techniques',
          'Two-person assist recommended for safety'
        ]
      }
    },
    {
      id: 'continence',
      title: 'Continence',
      description: 'Ability to control bladder and bowel',
      options: [
        { value: 1, label: 'Independent', description: 'Exercises complete self-control over urination and defecation' },
        { value: 0, label: 'Dependent', description: 'Partially or totally incontinent of bowel or bladder' }
      ],
      quickNotes: {
        1: [
          'Full bladder and bowel control maintained',
          'No incontinence episodes noted',
          'Manages toileting schedule independently',
          'Effectively communicates toileting needs'
        ],
        0: [
          'Occasional incontinence episodes',
          'Requires prompted toileting schedule',
          'Uses incontinence products as needed',
          'Bladder/bowel management program in place'
        ]
      }
    },
    {
      id: 'feeding',
      title: 'Feeding',
      description: 'Ability to feed oneself',
      options: [
        { value: 1, label: 'Independent', description: 'Gets food from plate into mouth without help' },
        { value: 0, label: 'Dependent', description: 'Needs partial or total help with feeding or requires parenteral feeding' }
      ],
      quickNotes: {
        1: [
          'Feeds self all meals without assistance',
          'Uses adaptive utensils effectively',
          'Maintains adequate nutrition intake',
          'No choking or swallowing concerns noted'
        ],
        0: [
          'Requires setup and/or feeding assistance',
          'Modified diet texture needed for safety',
          'Needs verbal cues to complete meals',
          'Swallowing concerns requiring close monitoring'
        ]
      }
    }
  ];

  const currentCategory = categories[currentStep];
  const totalSteps = categories.length;
  const isLastStep = currentStep === totalSteps - 1;
  const isComplete = currentStep === totalSteps;

  const handleResponse = (value) => {
    setResponses({ ...responses, [currentCategory.id]: value });
  };

  const handleNoteSelect = (note) => {
    const currentNotes = notes[currentCategory.id] || '';
    const newNotes = currentNotes ? `${currentNotes}\n${note}` : note;
    setNotes({ ...notes, [currentCategory.id]: newNotes });
  };

  const handleNext = () => {
    if (responses[currentCategory.id] !== undefined) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const calculateScore = () => {
    return Object.values(responses).reduce((sum, val) => sum + val, 0);
  };

  const getScoreInterpretation = (score) => {
    if (score === 6) return { level: 'Excellent', color: 'text-green-600', description: 'Independent in all ADLs' };
    if (score >= 4) return { level: 'Good', color: 'text-emerald-600', description: 'Mostly independent with minimal assistance' };
    if (score >= 2) return { level: 'Moderate', color: 'text-yellow-600', description: 'Requires assistance with several ADLs' };
    return { level: 'Significant Impairment', color: 'text-red-600', description: 'Requires substantial assistance' };
  };

  if (isComplete) {
    const score = calculateScore();
    const interpretation = getScoreInterpretation(score);

    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <CheckCircle className="text-green-600" size={32} />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Assessment Complete</h1>
              <p className="text-gray-600">Katz ADL Assessment Results</p>
            </div>

            <div className="bg-emerald-50 border-2 border-emerald-200 rounded-lg p-6 mb-8">
              <div className="text-center">
                <div className="text-5xl font-bold text-emerald-600 mb-2">{score}/6</div>
                <div className={`text-xl font-semibold ${interpretation.color} mb-2`}>
                  {interpretation.level}
                </div>
                <p className="text-gray-600">{interpretation.description}</p>
              </div>
            </div>

            <div className="space-y-6 mb-8">
              <h2 className="text-xl font-semibold text-gray-900">Detailed Results</h2>
              {categories.map((category) => (
                <div key={category.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold text-gray-900">{category.title}</h3>
                      <p className="text-sm text-gray-500">{category.description}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      responses[category.id] === 1
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {responses[category.id] === 1 ? 'Independent' : 'Dependent'}
                    </span>
                  </div>
                  {notes[category.id] && (
                    <div className="mt-3 p-3 bg-gray-50 rounded border border-gray-200">
                      <p className="text-sm text-gray-700 whitespace-pre-line">{notes[category.id]}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="flex gap-4">
              <button
                onClick={onBack}
                className="flex-1 bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 font-medium"
              >
                Back to Dashboard
              </button>
              <button className="flex-1 bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 font-medium">
                Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const selectedResponse = responses[currentCategory.id];
  const quickNotesForSelection = selectedResponse !== undefined
    ? currentCategory.quickNotes[selectedResponse]
    : [];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft size={20} />
            Back to Dashboard
          </button>
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Katz ADL Assessment</h1>
              <p className="text-gray-600 mt-1">Activities of Daily Living Evaluation</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Progress</div>
              <div className="text-2xl font-bold text-emerald-600">
                {currentStep + 1}/{totalSteps}
              </div>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-emerald-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Assessment Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{currentCategory.title}</h2>
            <p className="text-gray-600">{currentCategory.description}</p>
          </div>

          <div className="space-y-4 mb-8">
            {currentCategory.options.map((option) => (
              <button
                key={option.value}
                onClick={() => handleResponse(option.value)}
                className={`w-full text-left p-6 rounded-lg border-2 transition-all ${
                  responses[currentCategory.id] === option.value
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-200 hover:border-emerald-300'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-semibold text-lg text-gray-900 mb-1">
                      {option.label}
                    </div>
                    <p className="text-gray-600">{option.description}</p>
                  </div>
                  {responses[currentCategory.id] === option.value && (
                    <CheckCircle className="text-emerald-600 flex-shrink-0 ml-4" size={24} />
                  )}
                </div>
              </button>
            ))}
          </div>

          {/* Quick Notes */}
          {quickNotesForSelection.length > 0 && (
            <div className="mb-8">
              <h3 className="font-semibold text-gray-900 mb-3">Quick Clinical Notes</h3>
              <div className="grid grid-cols-1 gap-2">
                {quickNotesForSelection.map((note, index) => (
                  <button
                    key={index}
                    onClick={() => handleNoteSelect(note)}
                    className="text-left p-3 text-sm bg-gray-50 hover:bg-emerald-50 border border-gray-200 hover:border-emerald-300 rounded transition-colors"
                  >
                    {note}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Notes Textarea */}
          <div className="mb-8">
            <label className="block font-semibold text-gray-900 mb-2">
              Clinical Notes
            </label>
            <textarea
              value={notes[currentCategory.id] || ''}
              onChange={(e) => setNotes({ ...notes, [currentCategory.id]: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              rows="4"
              placeholder="Add detailed observations, context, or recommendations..."
            />
          </div>

          {/* Navigation */}
          <div className="flex gap-4">
            <button
              onClick={handleBack}
              disabled={currentStep === 0}
              className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={handleNext}
              disabled={responses[currentCategory.id] === undefined}
              className="flex-1 flex items-center justify-center gap-2 bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLastStep ? 'Complete Assessment' : 'Next'}
              {!isLastStep && <ArrowRight size={20} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KatzADL;
