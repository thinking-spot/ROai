# API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

### Register User

```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "organization_name": "Example Corp"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "org_admin",
  "organization_id": 1,
  "is_active": true,
  "is_verified": false
}
```

### Login

```http
POST /auth/login
```

**Request Body (form-data):**
```
username: user@example.com
password: securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Get Current User

```http
GET /auth/me
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "org_admin",
  "organization_id": 1,
  "is_active": true
}
```

## Organizations

### List Organizations

```http
GET /organizations
Authorization: Bearer {token}
```

### Get Organization

```http
GET /organizations/{organization_id}
Authorization: Bearer {token}
```

### Update Organization

```http
PATCH /organizations/{organization_id}
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "name": "Updated Corp Name",
  "employee_count": 500,
  "subscription_tier": "professional"
}
```

## AI Tools

### List AI Tools

```http
GET /ai-tools
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "GitHub Copilot",
    "vendor": "GitHub",
    "category": "code_assistant",
    "is_active": true,
    "monthly_cost": 1900.00,
    "active_users": 45,
    "deployment_date": "2024-01-15T00:00:00Z"
  }
]
```

### Get AI Tool Usage

```http
GET /ai-tools/{ai_tool_id}/usage?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer {token}
```

### Get AI Tool ROI

```http
GET /ai-tools/{ai_tool_id}/roi
Authorization: Bearer {token}
```

**Response:**
```json
{
  "ai_tool_id": 1,
  "ai_tool_name": "GitHub Copilot",
  "monthly_cost": 1900.00,
  "value_generated": 8750.00,
  "net_benefit": 6850.00,
  "roi_percentage": 260.5,
  "payback_period_months": 0.22,
  "productivity_metrics": {
    "baseline_mean": 45.2,
    "current_mean": 32.8,
    "percentage_change": -27.4,
    "is_significant": true
  }
}
```

## Metrics

### List Metrics

```http
GET /metrics
Authorization: Bearer {token}
```

### Create Metric

```http
POST /metrics
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "name": "Pull Request Completion Time",
  "metric_type": "pull_requests",
  "source": "github",
  "unit": "hours",
  "aggregation_method": "avg",
  "is_higher_better": false
}
```

### Get Metric Snapshots

```http
GET /metrics/{metric_id}/snapshots?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer {token}
```

## Analytics

### Dashboard Data

```http
GET /analytics/dashboard?view=cfo
Authorization: Bearer {token}
```

**Query Parameters:**
- `view`: One of `cfo`, `chro`, `cio`, `department`

**Response (CFO View):**
```json
{
  "view": "cfo",
  "summary": {
    "total_ai_spend": 45000.00,
    "total_value_generated": 156000.00,
    "net_benefit": 111000.00,
    "overall_roi": 246.7,
    "fte_equivalent_saved": 2.8
  },
  "ai_tools": [
    {
      "id": 1,
      "name": "GitHub Copilot",
      "monthly_cost": 1900.00,
      "roi_percentage": 260.5,
      "status": "positive"
    }
  ],
  "cost_breakdown": {
    "by_category": {
      "code_assistant": 5700.00,
      "writing_assistant": 3200.00
    }
  }
}
```

### ROI Summary

```http
GET /analytics/roi-summary
Authorization: Bearer {token}
```

### Attribution Analysis

```http
GET /analytics/attribution?metric_id=1&ai_tool_id=1
Authorization: Bearer {token}
```

**Response:**
```json
{
  "metric_id": 1,
  "metric_name": "Code Commits",
  "ai_tool_id": 1,
  "ai_tool_name": "GitHub Copilot",
  "analysis": {
    "correlation": 0.78,
    "causality_score": 0.85,
    "confidence_level": 0.95,
    "p_value": 0.001,
    "effect_size": 1.2,
    "interpretation": "Strong positive causal relationship"
  },
  "cohort_comparison": {
    "ai_users": {
      "mean": 45.2,
      "std": 8.3,
      "n": 42
    },
    "non_users": {
      "mean": 32.1,
      "std": 7.8,
      "n": 38
    },
    "difference": 13.1,
    "percentage_improvement": 40.8
  }
}
```

### Cohort Analysis

```http
GET /analytics/cohort-analysis
Authorization: Bearer {token}
```

### Adoption Metrics

```http
GET /analytics/adoption
Authorization: Bearer {token}
```

**Response:**
```json
{
  "overall_adoption_rate": 67.5,
  "tools": [
    {
      "ai_tool_id": 1,
      "name": "GitHub Copilot",
      "total_licenses": 50,
      "active_users": 45,
      "adoption_rate": 90.0,
      "avg_usage_hours_per_week": 12.5,
      "trend": "increasing"
    }
  ],
  "adoption_by_department": {
    "Engineering": 95.0,
    "Product": 72.0,
    "Marketing": 45.0
  }
}
```

## Integrations

### List Integrations

```http
GET /integrations
Authorization: Bearer {token}
```

### Connect Integration

```http
POST /integrations/{integration_type}/connect
Authorization: Bearer {token}
```

**Supported Types:**
- `google_workspace`
- `microsoft_365`
- `github`
- `jira`
- `salesforce`
- `openai`
- `anthropic`

### Sync Integration

```http
POST /integrations/{integration_id}/sync
Authorization: Bearer {token}
```

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Standard tier: 1000 requests per hour
- Professional tier: 5000 requests per hour
- Enterprise tier: Unlimited

## Pagination

List endpoints support pagination:

```http
GET /endpoint?skip=0&limit=100
```

**Response includes:**
```json
{
  "items": [...],
  "total": 250,
  "skip": 0,
  "limit": 100
}
```
