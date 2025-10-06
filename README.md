# OT Assessment Tracker

A comprehensive React application for Occupational Therapists to manage patient assessments, track progress, and streamline documentation.

## Features

- **Patient Dashboard**: Overview of all patients with quick stats and recent assessments
- **Patient Profiles**: Detailed view of individual patient progress with interactive charts
- **Multiple Assessment Tools**:
  - Katz ADL Assessment (Activities of Daily Living)
  - Barthel Index (Functional Independence)
  - FIM (Functional Independence Measure)
- **Smart Quick Notes**: Context-aware clinical note suggestions based on scores
- **Progress Tracking**: Visual charts showing patient improvement over time
- **Professional UI**: Clean, responsive design optimized for clinical workflows

## Tech Stack

- **React** - Frontend framework
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ot-assessment-tracker.git
cd ot-assessment-tracker
```

2. Install dependencies:
```bash
npm install
```

3. Initialize Tailwind CSS (if not already done):
```bash
npx tailwindcss init -p
```

4. Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## Project Structure

```
ot-assessment-tracker/
├── public/
├── src/
│   ├── components/
│   │   ├── Dashboard.js       # Main dashboard view
│   │   └── PatientProfile.js  # Individual patient view
│   ├── assessments/
│   │   ├── KatzADL.js         # Katz ADL assessment form
│   │   ├── BarthelIndex.js    # Barthel Index form
│   │   └── FIM.js             # FIM assessment form
│   ├── App.js                 # Main app component with routing
│   ├── index.css              # Tailwind directives
│   └── index.js               # App entry point
├── package.json
├── tailwind.config.js
└── README.md
```

## Assessment Tools

### Katz ADL (Activities of Daily Living)
- 6-item assessment measuring independence in basic activities
- Score range: 0-6 (6 = most independent)
- Categories: Bathing, Dressing, Toileting, Transferring, Continence, Feeding

### Barthel Index
- 10-item assessment of functional independence
- Score range: 0-100 (100 = fully independent)
- Comprehensive ADL evaluation

### FIM (Functional Independence Measure)
- 18-item assessment across multiple domains
- Score range: 18-126 (126 = complete independence)
- Categories: Self-Care, Sphincter Control, Transfers, Locomotion, Communication, Social Cognition

## Future Enhancements

- [ ] Django REST API backend
- [ ] User authentication and authorization
- [ ] PDF report generation
- [ ] Data export functionality
- [ ] Additional assessment tools
- [ ] Appointment scheduling
- [ ] Treatment plan templates
- [ ] Multi-facility support

## Contributing

Contributions are welcome! This project was created to support occupational therapy professionals in their daily work.

## License

MIT License - feel free to use this for your clinical practice or educational purposes.

## Acknowledgments

Built with love for occupational therapists everywhere 💚
