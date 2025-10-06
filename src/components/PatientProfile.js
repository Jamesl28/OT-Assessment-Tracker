import React from 'react';
import { ArrowLeft, Calendar, TrendingUp, FileText, User } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PatientProfile = ({ patient, onBack }) => {
  // Mock assessment history data
  const assessmentHistory = [
    { date: '2024-01-01', barthel: 65, fim: 85, katz: 4 },
    { date: '2024-01-08', barthel: 70, fim: 90, katz: 4 },
    { date: '2024-01-15', barthel: 85, fim: 98, katz: 5 }
  ];

  const recentNotes = [
    {
      date: '2024-01-15',
      type: 'Barthel Index',
      score: 85,
      note: 'Significant improvement in transfers and mobility. Patient demonstrates increased confidence.'
    },
    {
      date: '2024-01-08',
      type: 'FIM',
      score: 90,
      note: 'Continued progress in self-care activities. Requires minimal assistance with bathing.'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft size={20} />
            Back to Dashboard
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{patient?.name || 'Patient Profile'}</h1>
              <p className="text-sm text-gray-500 mt-1">
                {patient?.age} years • {patient?.diagnosis}
              </p>
            </div>
            <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">
              New Assessment
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Patient Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-blue-100 p-3 rounded-lg">
                <User className="text-blue-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">Patient ID</p>
                <p className="font-semibold text-gray-900">PT-{patient?.id || '001'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-emerald-100 p-3 rounded-lg">
                <Calendar className="text-emerald-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">Next Session</p>
                <p className="font-semibold text-gray-900">{patient?.nextSession || 'Not scheduled'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-green-100 p-3 rounded-lg">
                <TrendingUp className="text-green-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">Recent Score</p>
                <p className="font-semibold text-gray-900">{patient?.recentScore || 'N/A'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-purple-100 p-3 rounded-lg">
                <FileText className="text-purple-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Assessments</p>
                <p className="font-semibold text-gray-900">12</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Progress Chart */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Progress Over Time</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={assessmentHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="barthel" stroke="#10b981" name="Barthel Index" strokeWidth={2} />
                  <Line type="monotone" dataKey="fim" stroke="#3b82f6" name="FIM" strokeWidth={2} />
                  <Line type="monotone" dataKey="katz" stroke="#8b5cf6" name="Katz ADL" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Recent Notes */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Assessment Notes</h2>
              <div className="space-y-4">
                {recentNotes.map((note, index) => (
                  <div key={index} className="border-l-4 border-emerald-500 pl-4 py-2">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <span className="font-medium text-gray-900">{note.type}</span>
                        <span className="text-sm text-gray-500 ml-2">Score: {note.score}</span>
                      </div>
                      <span className="text-sm text-gray-500">{note.date}</span>
                    </div>
                    <p className="text-sm text-gray-600">{note.note}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Assessment Summary */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Current Status</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Barthel Index</span>
                    <span className="text-sm font-semibold text-emerald-600">85/100</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-emerald-600 h-2 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">FIM</span>
                    <span className="text-sm font-semibold text-blue-600">98/126</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full" style={{ width: '78%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Katz ADL</span>
                    <span className="text-sm font-semibold text-purple-600">5/6</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-purple-600 h-2 rounded-full" style={{ width: '83%' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Goals */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Treatment Goals</h2>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <input type="checkbox" className="mt-1" defaultChecked />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Improve bathing independence</p>
                    <p className="text-xs text-gray-500">Target: Independent by Feb 1</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <input type="checkbox" className="mt-1" defaultChecked />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Increase transfer safety</p>
                    <p className="text-xs text-gray-500">Target: Minimal assist by Jan 25</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <input type="checkbox" className="mt-1" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Independent dressing</p>
                    <p className="text-xs text-gray-500">Target: Independent by Feb 15</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientProfile;
