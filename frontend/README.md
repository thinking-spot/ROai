# AI ROI Analytics Platform - Frontend

Next.js frontend application for the AI ROI Analytics Platform.

## Features

- **Multi-view Dashboards**: Role-based views for different stakeholders
- **Real-time Analytics**: Live metrics and ROI calculations
- **Integration Management**: Connect and manage external services
- **Responsive Design**: Mobile-first, fully responsive UI

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- React Query (TanStack Query)
- Axios
- Recharts (for data visualization)

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── pages/          # Next.js pages
│   ├── components/     # Reusable React components
│   ├── views/         # Dashboard views (CFO, CHRO, CIO, etc.)
│   ├── services/      # API client and services
│   └── styles/        # Global styles
├── public/            # Static assets
└── package.json
```

## Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Dashboard Views

- **CFO View**: ROI, costs, payback periods
- **CHRO View**: Adoption rates, training effectiveness
- **CIO View**: License utilization, integrations
- **Department View**: Team performance, individual insights
