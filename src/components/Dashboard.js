import React from 'react';
import { Users, Calendar, TrendingUp, FileText, Plus } from 'lucide-react';

const Dashboard = ({ onNavigate }) => {
  const mockPatients = [
    {
      id: 1,
      name: 'John Smith',
      age: 68,
      diagnosis: 'Stroke Recovery',
      lastAssessment: '2024-01-15',
      nextSession: '2024-01-22',
      recentScore: 85,
      trend: 'up'
    },
    {
      id: 2,
      name: 'Mary Johnson',
      age: 72,
      diagnosis: 'Hip Replacement',
      lastAssessment: '2024-01-14',
      nextSession: '2024-01-21',
      recentScore: 72,
      trend: 'up'
    },
    {
      id: 3,
      name: 'Robert Williams',
      age: 55,
      diagnosis: 'TBI',
      lastAssessment: '2024-01-13',
      nextSession: '2024-01-20',
      recentScore: 68,
      trend: 'stable'
    }
  ];

  const recentAssessments = [
    { id: 1, patient: 'John Smith', type: 'Barthel Index', score: 85, date: '2024-01-15' },
    { id: 2, patient: 'Mary Johnson', type: 'FIM', score: 98, date: '2024-01-14' },
    { id: 3, patient: 'Robert Williams', type: 'Katz ADL', score: 5, date: '2024-01-13' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">OT Assessment Tracker</h1>
              <p className="text-sm text-gray-500 mt-1">Occupational Therapy Patient Management</p>
            </div>
            <button
              onClick={() => onNavigate('katz-adl')}
              className="flex items-center gap-2 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors"
            >
              <Plus size={20} />
              New Assessment
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Patients</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">24</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <Users className="text-blue-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">This Week</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">12</p>
              </div>
              <div className="bg-emerald-100 p-3 rounded-lg">
                <Calendar className="text-emerald-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Progress</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">+15%</p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <TrendingUp className="text-green-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Assessments</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">156</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <FileText className="text-purple-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Active Patients */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Active Patients</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {mockPatients.map(patient => (
                    <div
                      key={patient.id}
                      onClick={() => onNavigate('patient-profile', patient)}
                      className="border border-gray-200 rounded-lg p-4 hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{patient.name}</h3>
                          <p className="text-sm text-gray-500 mt-1">
                            {patient.age} years • {patient.diagnosis}
                          </p>
                          <div className="flex gap-4 mt-3">
                            <div className="text-sm">
                              <span className="text-gray-500">Last Assessment:</span>
                              <span className="ml-2 text-gray-900">{patient.lastAssessment}</span>
                            </div>
                            <div className="text-sm">
                              <span className="text-gray-500">Next Session:</span>
                              <span className="ml-2 text-gray-900">{patient.nextSession}</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="text-right">
                            <div className="text-2xl font-bold text-emerald-600">
                              {patient.recentScore}
                            </div>
                            <div className="text-xs text-gray-500">Recent Score</div>
                          </div>
                          {patient.trend === 'up' && (
                            <TrendingUp className="text-green-500" size={20} />
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions & Recent */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
              </div>
              <div className="p-6 space-y-3">
                <button
                  onClick={() => onNavigate('katz-adl')}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Katz ADL</div>
                  <div className="text-sm text-gray-500">Activities of Daily Living</div>
                </button>
                <button
                  onClick={() => onNavigate('barthel')}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Barthel Index</div>
                  <div className="text-sm text-gray-500">Functional Independence</div>
                </button>
                <button
                  onClick={() => onNavigate('fim')}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:border-emerald-500 hover:bg-emerald-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">FIM</div>
                  <div className="text-sm text-gray-500">Functional Independence Measure</div>
                </button>
              </div>
            </div>

            {/* Recent Assessments */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Recent Assessments</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {recentAssessments.map(assessment => (
                    <div key={assessment.id} className="border-b border-gray-100 last:border-0 pb-4 last:pb-0">
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="font-medium text-gray-900">{assessment.patient}</div>
                          <div className="text-sm text-gray-500">{assessment.type}</div>
                          <div className="text-xs text-gray-400 mt-1">{assessment.date}</div>
                        </div>
                        <div className="text-lg font-semibold text-emerald-600">
                          {assessment.score}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
