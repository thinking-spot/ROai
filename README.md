# ROai - AI ROI Analytics for Businesses

A comprehensive SaaS platform that helps businesses measure and demonstrate ROI from AI tool implementations.

An AI-agnostic analytics platform that:
- Integrates with existing business tools (GSuite, Microsoft 365, Jira, CRM, etc.)
- Tracks AI tool usage and correlates with productivity metrics
- Provides statistical attribution to prove causality
- Delivers role-based dashboards for different stakeholders
- Measures both human-using-AI and AI-agent scenarios

## Key Features

### 1. Data Integration
- Business productivity tools (Gmail, Outlook, Docs, Sheets)
- Project management (Jira, Asana, Monday)
- Development tools (GitHub, GitLab)
- AI platforms (OpenAI, Anthropic, GitHub Copilot, etc.)
- CRM & Support (Salesforce, Zendesk)

### 2. Attribution Engine
- Matched cohort analysis (AI users vs. non-users)
- Time-series baseline comparisons
- Incremental contribution modeling
- A/B testing framework
- Statistical significance testing

### 3. Multi-View Dashboards
- **CFO View**: ROI, payback period, cost analysis
- **CHRO View**: Adoption curves, training effectiveness, headcount impact
- **CIO View**: License utilization, tool redundancy, cost optimization
- **Department Head View**: Team performance, individual insights, recommendations

### 4. Measurement Scenarios
- **Humans using AI tools**: Copilot productivity gains
- **AI agents using business tools**: Autonomous task completion, quality metrics

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ CFO View │  │CHRO View │  │ CIO View │  │ Dept View│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI/Python)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Integration  │  │ Attribution  │  │  Analytics   │     │
│  │   Layer      │  │   Engine     │  │   Engine     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│     PostgreSQL + TimescaleDB (Time-series metrics)          │
│              Redis (Cache + Background Jobs)                │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              External Integrations                          │
│  GSuite │ Microsoft 365 │ Jira │ GitHub │ Salesforce │     │
│  OpenAI │ Anthropic │ Zendesk │ Slack │ More...            │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
roai/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration, security
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   │   ├── integrations/ # External API connectors
│   │   │   ├── analytics/    # ROI calculation engine
│   │   │   └── attribution/  # Statistical attribution
│   │   └── schemas/          # Pydantic schemas
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Next.js pages
│   │   ├── services/        # API client
│   │   └── views/           # Dashboard views
│   └── package.json
├── infrastructure/
│   ├── docker/
│   └── kubernetes/
└── docs/
    ├── api/
    ├── integrations/
    └── deployment/
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure setup
- [ ] Database schema design
- [ ] Authentication system
- [ ] Basic API framework

### Phase 2: Integration Layer
- [ ] GSuite connector (Gmail, Calendar, Docs)
- [ ] Microsoft 365 connector
- [ ] AI platform APIs (OpenAI, Anthropic)
- [ ] Jira/Project management integration

### Phase 3: Analytics Engine
- [ ] Metrics collection and storage
- [ ] Statistical attribution models
- [ ] Cohort analysis implementation
- [ ] A/B testing framework

### Phase 4: Dashboard & Reporting
- [ ] Multi-tenant frontend
- [ ] Role-based dashboard views
- [ ] Real-time metrics
- [ ] Export capabilities

### Phase 5: Scale & Optimization
- [ ] Performance optimization
- [ ] Advanced analytics features
- [ ] Custom integration framework
- [ ] API for external tools

## Target Market

**Primary**: Mid-market to enterprise (500-10,000 employees)
- Multiple AI tools deployed (5+ different platforms)
- Facing AI budget scrutiny
- Need to justify renewals or expansion

**Use Cases**:
1. AI Portfolio Optimization - Rationalize 15+ AI subscriptions
2. Productivity Intelligence - Prove AI ROI with statistical rigor
3. Change Management - Identify adoption gaps and training needs
4. Cost Forecasting - Predictable AI cost modeling

## Business Model

- **Pricing**: Usage-based SaaS (per employee + per integration)
- **ACV Target**: $50K-$500K depending on company size
- **Initial Focus**: Customer Support + AI chatbot/copilot (highly measurable)

## License

Proprietary - All rights reserved

## Contact

James - james.matthew.ladd@gmail.com
