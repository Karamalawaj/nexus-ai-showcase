# Nexus AI

> Private AI-enabled SaaS backend and e-commerce assistant platform.

## Product Preview

### Multi-tenant Admin Dashboard
The admin interface manages connected client stores, activation state, store type, AI persona, WooCommerce endpoint, and generated API access.

![Nexus AI Admin Dashboard](assets/nexus-admin.jpg)

### AI Commerce Robot Demo
The project includes an interactive robot persona designed to react to product attention and present contextual marketing prompts inside an e-commerce experience.

![Nexus AI Robot Demo](assets/nexus-robot-demo.jpg)

### Client Store Integration
A separate demo storefront illustrates the client-side integration model: the store activates a Nexus AI assistant and receives an embedded commerce-support experience.

![Nexus AI Client Store](assets/nexus-client-store.jpg)

> **Privacy note:** The public previews use demonstration stores, placeholder URLs, and non-production API values. No real WooCommerce credentials, client secrets, or private customer data are published.

## Overview
Nexus AI explores a centralized AI service for multiple e-commerce clients. Each connected store can be represented as an independent tenant with its own configuration, store type, AI persona, API access, and commerce integration.

## Engineering Areas
- FastAPI-based central backend
- Multi-tenant store configuration
- SQLAlchemy persistence with local SQLite fallback and PostgreSQL-ready configuration
- Store-specific API-key access
- Dynamic AI persona selection
- WooCommerce-oriented integration layer
- Embeddable client-side AI widget architecture
- Rate-limited chat API and origin-aware request handling
- Admin and demonstration interfaces

## Tech Stack
`Python` · `FastAPI` · `SQLAlchemy` · `SQLite / PostgreSQL` · `Jinja2` · `JavaScript` · `Google GenAI` · `WooCommerce`

## Architecture Snapshot

```text
Client Store
    │
    ├── Embedded Nexus AI Widget
    │        │
    │        ▼
    └── Nexus AI Central API
             │
             ├── Tenant / Store Configuration
             ├── AI Persona & Session Logic
             ├── Commerce Integration Layer
             └── Persistent Store Data
```

This diagram intentionally stays at a portfolio-safe level and does not expose private infrastructure, secrets, internal deployment configuration, or proprietary implementation details.

## Project Status
**Active development · Private source · Portfolio showcase**

The working source repository remains private and protected.

## Source Policy
**Portfolio showcase only. Source code, credentials, production infrastructure details, proprietary logic, private integrations, and security-sensitive implementation details are intentionally not published.**

## Rights
© Karam Alawaj. All rights reserved. No license is granted to copy, redistribute, reuse, or republish proprietary source or implementation details.
