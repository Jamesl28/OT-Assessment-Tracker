import React, { useState } from 'react';
import { Activity, ArrowLeft, ArrowRight, Save, CheckCircle } from 'lucide-react';

const FIMAssessment = ({ onBack }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    patientName: '',
    patientId: '',
    assessmentDate: '',
    eating: '',
    eatingNotes: '',
    grooming: '',
    groomingNotes: '',
    bathing: '',
    bathingNotes: '',
    dressingUpper: '',
    dressingUpperNotes: '',
    dressingLower: '',
    dressingLowerNotes: '',
    toileting: '',
    toiletingNotes: '',
    bladder: '',
    bladderNotes: '',
    bowel: '',
    bowelNotes: '',
    transfers: '',
    transfersNotes: '',
    toilet: '',
    toiletNotes: '',
    shower: '',
    showerNotes: '',
    locomotion: '',
    locomotionNotes: '',
    stairs: '',
    stairsNotes: '',
    comprehension: '',
    comprehensionNotes: '',
    expression: '',
    expressionNotes: '',
    socialInteraction: '',
    socialInteractionNotes: '',
    problemSolving: '',
    problemSolvingNotes: '',
    memory: '',
    memoryNotes: '',
    notes: ''
  });

  const assessmentCategories = [
    {
      id: 'eating',
      title: 'Eating',
      section: 'Self-Care',
      description: 'Includes use of suitable utensils to bring food to mouth, chewing and swallowing',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Patient eats from a dish, managing all consistencies independently' },
        { value: '6', label: 'Modified Independence', description: 'Requires adaptive device, extra time, or safety considerations' },
        { value: '5', label: 'Supervision', description: 'Requires cueing or supervision only' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more of eating tasks' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74% of eating tasks' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49% of eating tasks' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25% of eating tasks' }
      ],
      quickNotes: {
        '7': ['Patient eats independently with standard utensils', 'No modifications or assistance required'],
        '6': ['Uses adaptive utensils but feeds self completely', 'Requires extra time but completes independently'],
        '5': ['Needs verbal cues for safe swallowing', 'Requires supervision for pacing'],
        '4': ['Requires minimal assistance with cutting food', 'Needs help with container opening'],
        '3': ['Requires mod assist for feeding tasks', 'Patient assists but needs frequent help'],
        '2': ['Requires max assist for most feeding tasks', 'Patient participates minimally'],
        '1': ['Total assist required for all feeding', 'Unable to self-feed']
      }
    },
    {
      id: 'grooming',
      title: 'Grooming',
      section: 'Self-Care',
      description: 'Oral care, hair grooming, washing hands and face, shaving or makeup',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Completes all grooming tasks independently' },
        { value: '6', label: 'Modified Independence', description: 'Requires adaptive device or extra time' },
        { value: '5', label: 'Supervision', description: 'Requires cueing or supervision only' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more of grooming' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74% of grooming' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49% of grooming' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25% of grooming' }
      ],
      quickNotes: {
        '7': ['Completes all grooming independently', 'Maintains good personal hygiene'],
        '6': ['Uses adaptive equipment for independence', 'Requires extended time but completes tasks'],
        '5': ['Needs reminders to complete grooming', 'Requires supervision for safety'],
        '4': ['Needs minimal help with hair care', 'Requires setup but completes most tasks'],
        '3': ['Requires mod assist for oral care', 'Completes about half of grooming tasks'],
        '2': ['Requires max assist for grooming', 'Limited participation in tasks'],
        '1': ['Total dependence for all grooming', 'Unable to participate']
      }
    },
    {
      id: 'bathing',
      title: 'Bathing',
      section: 'Self-Care',
      description: 'Washing, rinsing, and drying the body from neck down (excludes back)',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Bathes independently including getting in/out of tub or shower' },
        { value: '6', label: 'Modified Independence', description: 'Requires equipment or extra time' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more of bathing' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74% of bathing' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49% of bathing' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25% of bathing' }
      ],
      quickNotes: {
        '7': ['Bathes all body parts independently', 'Safe tub/shower transfers'],
        '6': ['Uses shower chair or grab bars', 'Requires extra time but independent'],
        '5': ['Needs stand-by assist for safety', 'Requires supervision during bathing'],
        '4': ['Needs help with back only', 'Completes most bathing independently'],
        '3': ['Requires mod assist for bathing', 'Washes front of body only'],
        '2': ['Requires max assist for bathing', 'Minimal participation'],
        '1': ['Total assist for all bathing', 'Unable to participate']
      }
    },
    {
      id: 'dressingUpper',
      title: 'Dressing - Upper Body',
      section: 'Self-Care',
      description: 'Dressing above the waist, including orthotics',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Dresses upper body completely independently' },
        { value: '6', label: 'Modified Independence', description: 'Requires adaptive clothing or devices' },
        { value: '5', label: 'Supervision', description: 'Requires cueing or supervision' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25%' }
      ],
      quickNotes: {
        '7': ['Dons/doffs all UE clothing independently', 'Manages all fasteners'],
        '6': ['Uses button hook or adapted clothing', 'Independent with modifications'],
        '5': ['Needs verbal cues for sequencing', 'Requires supervision'],
        '4': ['Needs minimal help with fasteners', 'Completes most dressing'],
        '3': ['Requires mod assist for UE dressing', 'Completes about half'],
        '2': ['Requires max assist for UE dressing', 'Limited participation'],
        '1': ['Total assist for UE dressing', 'Unable to participate']
      }
    },
    {
      id: 'dressingLower',
      title: 'Dressing - Lower Body',
      section: 'Self-Care',
      description: 'Dressing below the waist, including orthotics and shoes',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Dresses lower body completely independently' },
        { value: '6', label: 'Modified Independence', description: 'Requires adaptive equipment' },
        { value: '5', label: 'Supervision', description: 'Requires cueing or supervision' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25%' }
      ],
      quickNotes: {
        '7': ['Dons/doffs all LE clothing independently', 'Puts on shoes/socks independently'],
        '6': ['Uses sock aid and reacher', 'Independent with adaptive equipment'],
        '5': ['Needs verbal cues for balance', 'Requires supervision for safety'],
        '4': ['Needs minimal help with shoes', 'Completes most LE dressing'],
        '3': ['Requires mod assist for LE dressing', 'Assists with about half'],
        '2': ['Requires max assist for LE dressing', 'Limited participation'],
        '1': ['Total assist for LE dressing', 'Unable to participate']
      }
    },
    {
      id: 'toileting',
      title: 'Toileting',
      section: 'Self-Care',
      description: 'Perineal hygiene and adjusting clothing before/after toilet use',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Manages all aspects of toileting independently' },
        { value: '6', label: 'Modified Independence', description: 'Requires equipment or extra time' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Patient performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Patient performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Patient performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Patient performs less than 25%' }
      ],
      quickNotes: {
        '7': ['Manages all toileting tasks independently', 'Completes hygiene appropriately'],
        '6': ['Uses raised toilet seat or grab bars', 'Independent with equipment'],
        '5': ['Needs supervision for safety', 'Requires verbal cues'],
        '4': ['Needs minimal help with clothing', 'Completes most tasks'],
        '3': ['Requires mod assist for toileting', 'Assists with about half'],
        '2': ['Requires max assist for toileting', 'Limited participation'],
        '1': ['Total assist for toileting', 'Unable to participate']
      }
    },
    {
      id: 'bladder',
      title: 'Bladder Management',
      section: 'Sphincter Control',
      description: 'Complete control and ability to maintain perineal hygiene',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Complete bladder control, no accidents' },
        { value: '6', label: 'Modified Independence', description: 'Uses device independently (catheter, etc.)' },
        { value: '5', label: 'Supervision', description: 'Requires supervision or reminders' },
        { value: '4', label: 'Minimal Assist', description: 'Infrequent accidents (less than once/day)' },
        { value: '3', label: 'Moderate Assist', description: 'Occasional accidents (once/day)' },
        { value: '2', label: 'Maximal Assist', description: 'Frequent accidents (more than once/day)' },
        { value: '1', label: 'Total Assist', description: 'No control or indwelling catheter' }
      ],
      quickNotes: {
        '7': ['Complete bladder control', 'No accidents reported'],
        '6': ['Manages catheter independently', 'No assistance needed'],
        '5': ['Needs reminders for toileting', 'Rare accidents with prompts'],
        '4': ['Infrequent accidents noted', 'Mostly continent'],
        '3': ['Occasional accidents daily', 'Partial control'],
        '2': ['Frequent accidents', 'Poor bladder control'],
        '1': ['Complete incontinence', 'Indwelling catheter with assistance']
      }
    },
    {
      id: 'bowel',
      title: 'Bowel Management',
      section: 'Sphincter Control',
      description: 'Complete control and ability to maintain perineal hygiene',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Complete bowel control, no accidents' },
        { value: '6', label: 'Modified Independence', description: 'Uses suppository independently' },
        { value: '5', label: 'Supervision', description: 'Requires supervision or reminders' },
        { value: '4', label: 'Minimal Assist', description: 'Infrequent accidents (less than once/week)' },
        { value: '3', label: 'Moderate Assist', description: 'Occasional accidents (once/week)' },
        { value: '2', label: 'Maximal Assist', description: 'Frequent accidents (more than once/week)' },
        { value: '1', label: 'Total Assist', description: 'No control or requires enemas' }
      ],
      quickNotes: {
        '7': ['Complete bowel control', 'No accidents reported'],
        '6': ['Manages bowel program independently', 'No assistance needed'],
        '5': ['Needs reminders for bowel routine', 'Rare accidents with prompts'],
        '4': ['Infrequent accidents noted', 'Mostly continent'],
        '3': ['Occasional accidents weekly', 'Partial control'],
        '2': ['Frequent accidents', 'Poor bowel control'],
        '1': ['Complete incontinence', 'Requires total bowel management']
      }
    },
    {
      id: 'transfers',
      title: 'Bed/Chair/Wheelchair Transfer',
      section: 'Mobility',
      description: 'Moving to and from bed, chair, wheelchair; includes coming to standing position',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Transfers safely in all situations' },
        { value: '6', label: 'Modified Independence', description: 'Uses assistive device for transfers' },
        { value: '5', label: 'Supervision', description: 'Requires supervision or cueing' },
        { value: '4', label: 'Minimal Assist', description: 'Performs 75% or more of transfer' },
        { value: '3', label: 'Moderate Assist', description: 'Performs 50-74% of transfer' },
        { value: '2', label: 'Maximal Assist', description: 'Performs 25-49% of transfer' },
        { value: '1', label: 'Total Assist', description: 'Performs less than 25% or uses lift' }
      ],
      quickNotes: {
        '7': ['Transfers independently all surfaces', 'No equipment needed'],
        '6': ['Uses grab bar or walker', 'Independent with device'],
        '5': ['Needs contact guard for safety', 'Requires supervision'],
        '4': ['Needs minimal assist to stand', 'Mostly independent'],
        '3': ['Requires mod assist for transfers', 'Assists about half'],
        '2': ['Requires max assist for transfers', 'Limited weight bearing'],
        '1': ['Total assist or mechanical lift', 'Unable to assist']
      }
    },
    {
      id: 'toilet',
      title: 'Toilet Transfer',
      section: 'Mobility',
      description: 'Getting on and off toilet',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Transfers safely and independently' },
        { value: '6', label: 'Modified Independence', description: 'Uses grab bars or raised seat' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Performs less than 25%' }
      ],
      quickNotes: {
        '7': ['Toilet transfers independently', 'No equipment needed'],
        '6': ['Uses grab bars for safety', 'Independent with equipment'],
        '5': ['Needs stand-by assist', 'Requires supervision'],
        '4': ['Needs minimal assist on/off toilet', 'Mostly independent'],
        '3': ['Requires mod assist for toilet transfers', 'Assists about half'],
        '2': ['Requires max assist for toilet transfers', 'Limited assistance provided'],
        '1': ['Total assist for toilet transfers', 'Unable to assist']
      }
    },
    {
      id: 'shower',
      title: 'Tub/Shower Transfer',
      section: 'Mobility',
      description: 'Getting in and out of tub or shower',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Transfers safely and independently' },
        { value: '6', label: 'Modified Independence', description: 'Uses shower chair or grab bars' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Performs less than 25%' }
      ],
      quickNotes: {
        '7': ['Tub/shower transfers independently', 'No equipment needed'],
        '6': ['Uses shower chair and grab bars', 'Independent with equipment'],
        '5': ['Needs stand-by assist for safety', 'Requires supervision'],
        '4': ['Needs minimal assist in/out', 'Mostly independent'],
        '3': ['Requires mod assist for shower transfers', 'Assists about half'],
        '2': ['Requires max assist for shower transfers', 'Limited assistance'],
        '1': ['Total assist for shower transfers', 'Unable to assist']
      }
    },
    {
      id: 'locomotion',
      title: 'Locomotion',
      section: 'Mobility',
      description: 'Walking or wheelchair propulsion for 150 feet',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Walks 150+ feet independently' },
        { value: '6', label: 'Modified Independence', description: 'Uses assistive device but independent' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Performs 75% or more of distance' },
        { value: '3', label: 'Moderate Assist', description: 'Performs 50-74% of distance' },
        { value: '2', label: 'Maximal Assist', description: 'Performs 25-49% of distance' },
        { value: '1', label: 'Total Assist', description: 'Performs less than 25% or pushed in w/c' }
      ],
      quickNotes: {
        '7': ['Ambulates 150+ feet independently', 'No assistive device needed'],
        '6': ['Uses walker/cane independently', 'Walks with device safely'],
        '5': ['Needs contact guard for ambulation', 'Requires supervision'],
        '4': ['Needs minimal assist for distance', 'Mostly independent'],
        '3': ['Requires mod assist for ambulation', 'Completes partial distance'],
        '2': ['Requires max assist for ambulation', 'Very limited distance'],
        '1': ['Unable to ambulate', 'Pushed in wheelchair']
      }
    },
    {
      id: 'stairs',
      title: 'Stairs',
      section: 'Mobility',
      description: 'Going up and down 12-14 stairs',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Climbs stairs safely and independently' },
        { value: '6', label: 'Modified Independence', description: 'Uses assistive device or railing' },
        { value: '5', label: 'Supervision', description: 'Requires supervision for safety' },
        { value: '4', label: 'Minimal Assist', description: 'Performs 75% or more' },
        { value: '3', label: 'Moderate Assist', description: 'Performs 50-74%' },
        { value: '2', label: 'Maximal Assist', description: 'Performs 25-49%' },
        { value: '1', label: 'Total Assist', description: 'Unable to climb stairs' }
      ],
      quickNotes: {
        '7': ['Climbs stairs independently', 'No equipment needed'],
        '6': ['Uses handrail for safety', 'Independent with railing'],
        '5': ['Needs contact guard on stairs', 'Requires supervision'],
        '4': ['Needs minimal assist on stairs', 'Mostly independent'],
        '3': ['Requires mod assist for stairs', 'Completes with help'],
        '2': ['Requires max assist for stairs', 'Very limited ability'],
        '1': ['Unable to use stairs', 'Not safe for stairs']
      }
    },
    {
      id: 'comprehension',
      title: 'Comprehension',
      section: 'Communication',
      description: 'Understanding of verbal or gestural communication',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Understands complex conversations' },
        { value: '6', label: 'Modified Independence', description: 'Understands with extra time or repetition' },
        { value: '5', label: 'Supervision', description: 'Requires prompting 10% of time' },
        { value: '4', label: 'Minimal Assist', description: 'Requires prompting 10-25% of time' },
        { value: '3', label: 'Moderate Assist', description: 'Requires prompting 25-50% of time' },
        { value: '2', label: 'Maximal Assist', description: 'Requires prompting 50-75% of time' },
        { value: '1', label: 'Total Assist', description: 'Understands less than 25% of communication' }
      ],
      quickNotes: {
        '7': ['Comprehends all communication', 'No difficulty understanding'],
        '6': ['Needs extra time or repetition', 'Generally comprehends well'],
        '5': ['Needs occasional clarification', 'Mostly understands'],
        '4': ['Needs frequent clarification', 'Some comprehension deficits'],
        '3': ['Moderate comprehension deficits', 'Needs significant help'],
        '2': ['Severe comprehension deficits', 'Very limited understanding'],
        '1': ['Minimal comprehension', 'Does not understand most communication']
      }
    },
    {
      id: 'expression',
      title: 'Expression',
      section: 'Communication',
      description: 'Vocal or gestural expression',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Expresses complex ideas clearly' },
        { value: '6', label: 'Modified Independence', description: 'Expresses with extra time or device' },
        { value: '5', label: 'Supervision', description: 'Requires prompting 10% of time' },
        { value: '4', label: 'Minimal Assist', description: 'Requires prompting 10-25% of time' },
        { value: '3', label: 'Moderate Assist', description: 'Requires prompting 25-50% of time' },
        { value: '2', label: 'Maximal Assist', description: 'Requires prompting 50-75% of time' },
        { value: '1', label: 'Total Assist', description: 'Expresses less than 25% of needs' }
      ],
      quickNotes: {
        '7': ['Expresses all needs clearly', 'No communication difficulty'],
        '6': ['Uses communication device effectively', 'Expresses needs with modifications'],
        '5': ['Needs occasional prompting', 'Generally communicates well'],
        '4': ['Needs frequent prompting', 'Some expression deficits'],
        '3': ['Moderate expression deficits', 'Needs significant help'],
        '2': ['Severe expression deficits', 'Very limited communication'],
        '1': ['Minimal expression', 'Cannot communicate most needs']
      }
    },
    {
      id: 'socialInteraction',
      title: 'Social Interaction',
      section: 'Social Cognition',
      description: 'Skills related to getting along with others',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Interacts appropriately in all situations' },
        { value: '6', label: 'Modified Independence', description: 'Interacts appropriately with extra time' },
        { value: '5', label: 'Supervision', description: 'Requires prompting 10% of time' },
        { value: '4', label: 'Minimal Assist', description: 'Requires prompting 10-25% of time' },
        { value: '3', label: 'Moderate Assist', description: 'Requires prompting 25-50% of time' },
        { value: '2', label: 'Maximal Assist', description: 'Requires prompting 50-75% of time' },
        { value: '1', label: 'Total Assist', description: 'Inappropriate behavior more than 75% of time' }
      ],
      quickNotes: {
        '7': ['Appropriate social interactions', 'No behavioral concerns'],
        '6': ['Generally appropriate', 'Needs extra processing time'],
        '5': ['Needs occasional redirection', 'Mostly appropriate'],
        '4': ['Needs frequent redirection', 'Some social deficits'],
        '3': ['Moderate social deficits', 'Needs significant guidance'],
        '2': ['Severe social deficits', 'Frequent inappropriate behavior'],
        '1': ['Very poor social interaction', 'Constantly inappropriate']
      }
    },
    {
      id: 'problemSolving',
      title: 'Problem Solving',
      section: 'Social Cognition',
      description: 'Skills related to solving problems of daily living',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Solves problems independently' },
        { value: '6', label: 'Modified Independence', description: 'Solves with extra time or strategies' },
        { value: '5', label: 'Supervision', description: 'Requires prompting 10% of time' },
        { value: '4', label: 'Minimal Assist', description: 'Requires prompting 10-25% of time' },
        { value: '3', label: 'Moderate Assist', description: 'Requires prompting 25-50% of time' },
        { value: '2', label: 'Maximal Assist', description: 'Requires prompting 50-75% of time' },
        { value: '1', label: 'Total Assist', description: 'Unable to solve problems more than 75% of time' }
      ],
      quickNotes: {
        '7': ['Solves daily problems independently', 'Good problem-solving skills'],
        '6': ['Solves problems with extra time', 'Generally effective'],
        '5': ['Needs occasional assistance', 'Mostly independent'],
        '4': ['Needs frequent assistance', 'Some problem-solving deficits'],
        '3': ['Moderate problem-solving deficits', 'Needs significant help'],
        '2': ['Severe problem-solving deficits', 'Very limited ability'],
        '1': ['Unable to problem solve', 'Requires constant direction']
      }
    },
    {
      id: 'memory',
      title: 'Memory',
      section: 'Social Cognition',
      description: 'Skills related to recognizing and remembering',
      options: [
        { value: '7', label: 'Complete Independence', description: 'Remembers and recognizes independently' },
        { value: '6', label: 'Modified Independence', description: 'Uses memory aids effectively' },
        { value: '5', label: 'Supervision', description: 'Requires prompting 10% of time' },
        { value: '4', label: 'Minimal Assist', description: 'Requires prompting 10-25% of time' },
        { value: '3', label: 'Moderate Assist', description: 'Requires prompting 25-50% of time' },
        { value: '2', label: 'Maximal Assist', description: 'Requires prompting 50-75% of time' },
        { value: '1', label: 'Total Assist', description: 'Fails to remember more than 75% of time' }
      ],
      quickNotes: {
        '7': ['Excellent memory function', 'No memory concerns'],
        '6': ['Uses calendar/reminders effectively', 'Compensates well'],
        '5': ['Needs occasional reminders', 'Mostly remembers'],
        '4': ['Needs frequent reminders', 'Some memory deficits'],
        '3': ['Moderate memory deficits', 'Needs significant cueing'],
        '2': ['Severe memory deficits', 'Very limited recall'],
        '1': ['Profound memory impairment', 'Cannot recall daily information']
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
    if (score >= 108) return 'Complete independence - no helper required';
    if (score >= 90) return 'Modified independence - device needed but no physical help';
    if (score >= 54) return 'Minimal to moderate assistance - patient performs 50-99% of tasks';
    if (score >= 36) return 'Moderate to maximal assistance - patient performs 25-74% of tasks';
    return 'Maximal to total assistance - patient performs less than 50% of tasks';
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
    alert(`Assessment Complete!\nFIM Score: ${finalScore}/126\n${getScoreInterpretation(finalScore)}`);
  };

  const renderPatientInfo = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-light text-neutral-900 mb-2">Patient Information</h2>
        <p className="text-neutral-500 font-light">Enter the patient details to begin the FIM assessment</p>
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
            {category.section} - Step {currentStep} of {assessmentCategories.length}
          </div>
          <h2 className="text-3xl font-light text-neutral-900 mb-2">{category.title}</h2>
          <p className="text-neutral-500 font-light">{category.description}</p>
        </div>

        <div className="space-y-2">
          {category.options.map((option) => (
            <label
              key={option.value}
              className={`block p-4 border-2 cursor-pointer transition-all hover:bg-emerald-50/30 ${
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
          <p className="text-neutral-500 font-light">Review the FIM results before submitting</p>
        </div>

        <div className="bg-emerald-50 border-l-4 border-emerald-600 p-6">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="text-emerald-600" size={24} />
            <h3 className="text-xl font-medium text-neutral-900">Assessment Complete</h3>
          </div>
          <div className="text-3xl font-light text-emerald-600 mt-4">
            FIM Score: {score}/126
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
          <h3 className="text-lg font-light text-neutral-900">Assessment Results by Category</h3>

          {['Self-Care', 'Sphincter Control', 'Mobility', 'Communication', 'Social Cognition'].map((section) => {
            const sectionCategories = assessmentCategories.filter(cat => cat.section === section);
            const sectionScore = sectionCategories.reduce((total, cat) => total + (parseInt(formData[cat.id]) || 0), 0);
            const maxSectionScore = sectionCategories.reduce((total, cat) => total + parseInt(cat.options[0].value), 0);

            return (
              <div key={section} className="border border-neutral-200 p-4">
                <div className="flex items-center justify-between mb-4 pb-2 border-b border-neutral-200">
                  <h4 className="font-medium text-neutral-900">{section}</h4>
                  <span className="text-emerald-600 font-medium">{sectionScore}/{maxSectionScore}</span>
                </div>
                <div className="space-y-3">
                  {sectionCategories.map((cat) => (
                    <div key={cat.id}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-light text-neutral-700">{cat.title}</span>
                        <span className="text-sm text-emerald-600 font-medium">
                          {formData[cat.id]}/7
                        </span>
                      </div>
                      {formData[`${cat.id}Notes`] && (
                        <div className="mt-1 pl-4 border-l-2 border-neutral-200">
                          <p className="text-xs text-neutral-600 font-light">{formData[`${cat.id}Notes`]}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
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
                <h1 className="text-2xl font-light tracking-tight text-neutral-900">FIM Assessment</h1>
                <p className="text-sm text-emerald-600 font-light">Functional Independence Measure</p>
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

export default FIMAssessment;
