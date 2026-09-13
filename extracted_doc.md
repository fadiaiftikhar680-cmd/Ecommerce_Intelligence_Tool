PROJECT DOCUMENTATION

E-Commerce Intelligence Dashboard Tool

Pakistan Market

SaaS-Based Event & Profit Intelligence Platform

Consolidated Reference  —  PRD · Architecture · Diagrams · Rules · Phases · Design · Memory Log

Document Type:  Technical & Product Documentation

Project Stage:  Frontend & Mock Data Layer Complete (Layer 1–2)

Version:  1.0

Prepared:  September 2026

Table of Contents

1.  Product Requirements Document	3

1.1  What to Build	3

1.2  Target User	3

1.3  Core Features & Modules	3

1.4  Priority Tiers	3

2.  Architecture Documentation	4

2.1  System Architecture	4

2.2  Project Directory Structure	4

2.3  Technology Stack	4

2.4  Languages & Libraries Used	4

3.  Project Rules	6

3.1–3.6  What to Use · Avoid · Dependencies · Error Handling · AI Boundaries · General Rules	6

4.  Implementation Phases	7

4.1  Implementation Roadmap (Phases 1–7)	7

4.2  Mapping to Standard Project Phase Categories	8

5.  Design Documentation	9

5.1–5.3  UI/UX · Color & Theme · Font & Typography	9

6.  Project Memory Log	10

6.1–6.4  Purpose · What Happened · Currently Working On · Updates	10

1.  Product Requirements Document

1.1  What to Build

A Smart Event & Profit Intelligence Tool designed for the Pakistani e-commerce market. E-commerce sales in Pakistan peak around seasonal events — Ramadan, Eid-ul-Fitr, Eid-ul-Adha, the wedding season, 14th August (Independence Day), and Blessed Friday (11.11).

The tool gives sellers event alerts, winning-product suggestions, safe pricing guidance, and COD (Cash on Delivery) return-risk assessment — enabling data-backed decisions that minimize losses.

Project Type:  Frontend-First Web Application

1.2  Target User

Target Market:  Pakistani E-Commerce Sellers

The platform is built as a SaaS-based Event & Profit Intelligence Platform for this seller base, aligned with Pakistan-specific seasonal demand patterns and COD-related risk — COD being the dominant payment method in this market.

1.3  Core Features & Modules

Module

Purpose & Functionality

1. Event Calendar & Alert System

Synchronizes Hijri and Gregorian calendars; sends demand alerts 30–45 days ahead of Ramadan, Eid, the wedding season, and 14th August.

2. Hot Product & Demand Finder

Identifies high-demand winning products aligned with the upcoming event, along with an opportunity score (0–100%).

3. Smart Price & Margin Protector

Calculates the safe selling price and maximum allowable discount after deducting cost, courier fees, ad spend, and packaging.

4. COD Return (RTO) Risk Predictor

Generates a return-risk score (Low / Medium / High) based on product category, price point, and region.

5. Store Inventory Predictor

Syncs with Shopify/WooCommerce stores to identify event-specific best-sellers within existing stock.

6. Actionable Insights Dashboard

Presents all metrics, charts, and recommendations through simple visual cards and tables.

1.4  Priority Tiers

Tier

Modules

Tier 1 — Must Have

Event Calendar, Hot Product Finder, Price Suggestion Engine, Store Predictor, COD Return Risk, Margin Protector

Tier 2 — Good to Have

City Demand Heatmap, Competitor Tracker, Dead Stock Liquidation, Smart Product Bundling

Tier 3 — Future

Local Wholesale Sourcing Estimator, Courier Cut-Off Planner, Influencer Matcher

2.  Architecture Documentation

2.1  System Architecture

The system is divided into three distinct layers. Current focus is on Layer 1 and Layer 2 (Frontend + Mock Data); Layer 3 (the real backend) will be attached in Phase 2 without any UI changes.

Layer 1 — Frontend UI: Streamlit (Python), Plotly, Pandas

Layer 2 — Mock Data & Service Client: mock/data.py (fixtures) + utils/api_client.py

Layer 3 — Backend & Scrapers (Phase 2): FastAPI, PostgreSQL, Scikit-learn, Store REST APIs

┌─────────────────────────────────────────────────────┐│               LAYER 1 · FRONTEND UI                  ││        Streamlit (Python) · Plotly · Pandas          │└───────────────────────────┬───────────────────────────┘                            │┌───────────────────────────▼───────────────────────────┐│         LAYER 2 · MOCK DATA & SERVICE CLIENT          ││    mock/data.py (fixtures)  +  utils/api_client.py    │└───────────────────────────┬───────────────────────────┘                            │  (future API bridge)┌───────────────────────────▼───────────────────────────┐│        LAYER 3 · BACKEND & SCRAPERS  (Phase 2)        ││  FastAPI · PostgreSQL · Scikit-learn · Store REST APIs │└─────────────────────────────────────────────────────┘

2.2  Project Directory Structure

ecommerce-intelligence/├── app.py                        # Streamlit entry point (Overview)├── pages/│   ├── 1_Event_Intelligence.py   # Event Calendar & Alerts│   ├── 2_Winning_Products.py     # Hot Product Finder & Pricing│   ├── 3_COD_Risk_Calculator.py  # COD Return Risk Predictor│   └── 4_My_Store.py             # Store Inventory Predictor├── components/                   # Reusable UI components (cards, charts)├── mock/│   └── data.py                   # Mock dataset (Pakistan events & products)├── utils/│   └── api_client.py             # Service functions (mock now, real API later)├── .streamlit/│   └── config.toml               # Theme & app configuration├── requirements.txt└── README.md

Mock Data Layer — Purpose

The Mock Layer is a temporary bridge that makes the frontend fully functional using dummy data before the real backend is built. Once the backend is ready, only the request calls inside utils/api_client.py are updated — the Streamlit UI itself requires no changes.

2.3  Technology Stack

Frontend (Streamlit App)

Technology

Version

Purpose

Python

3.13.x

Core language for the frontend application

Streamlit

Latest

Web app framework used to build and render the dashboard UI

Pandas

Latest

Handling and structuring mock/tabular data

Plotly

Latest

Analytics charts and trend visualization

streamlit-option-menu

Latest

Sidebar navigation menu

Pillow

Latest

Icon and image handling within the UI

Future Backend & Storage (Phase 2)

Technology

Version

Purpose

Python

3.13.x

Core backend language

FastAPI

0.111+

Async REST API framework

PostgreSQL

16

Primary relational database

SQLAlchemy

2.0+

Python ORM for database operations

Scikit-learn

1.5+

COD return risk & demand scoring models

BeautifulSoup / Scrapy

Latest

Market price & trend scraping

Workspace & Tooling

Tool

Purpose

pip / venv

Python dependency and virtual-environment management

Git & GitHub

Version control and code hosting

Docker

Containerization for database & backend runtimes

Streamlit Community Cloud

Frontend (Streamlit) production deployment

Render / Railway

Backend (FastAPI) production deployment

Neon.tech / Supabase

Serverless PostgreSQL hosting

2.4  Languages & Libraries Used

Summary of the programming languages and libraries used to build this tool, across the current frontend build and the planned backend (Phase 2).

Languages

Language

Used For

Python

Frontend app (Streamlit) and, in Phase 2, the backend (FastAPI), data scraping, and ML models

SQL

Database queries against PostgreSQL (Phase 2)

TOML

Streamlit app configuration (.streamlit/config.toml)

3.  Project Rules

3.1  What to Use

Python 3.13.x, Streamlit, Pandas, Plotly, streamlit-option-menu, Pillow — current frontend

FastAPI, PostgreSQL, SQLAlchemy, Scikit-learn, BeautifulSoup / Scrapy — Phase 2 backend

pip / venv, Git & GitHub, Docker — tooling

Streamlit Community Cloud, Render / Railway, Neon.tech / Supabase — deployment

3.2  What to Avoid

Not defined in source documentation:  no explicit "what to avoid" guideline exists yet. This section should be filled in with project-owner or team input.

3.3  Libraries and Dependencies

Library

Purpose

Streamlit

Core framework for building and rendering the dashboard UI

Pandas

Structuring and manipulating mock/tabular data

Plotly

Interactive charts and trend visualizations

streamlit-option-menu

Sidebar navigation menu

Pillow

Icon and image handling within the UI

FastAPI (Phase 2)

Async REST API framework

SQLAlchemy (Phase 2)

Python ORM for database operations

Scikit-learn (Phase 2)

COD return risk & demand scoring models

BeautifulSoup / Scrapy (Phase 2)

Market price & trend scraping

3.4  Error Handling

Not defined in source documentation:  no error-handling policy or standard has been defined. This should be added once the team agrees on an approach.

3.5  Boundaries of AI

Not defined in source documentation:  the scope and boundaries of AI usage on this project are not yet defined and should be scoped separately.

3.6  General Rules

No standalone "general rules" section exists yet. The one architectural principle stated directly in the source material is:

Once the backend is attached (Phase 2), only the request calls inside utils/api_client.py will be updated — the Streamlit UI itself will not change (source: “Mock Data Layer” section).

4.  Implementation Phases

4.1  Implementation Roadmap

Phase 1 — Project & Workspace Setup

Initialize the repository, set up a Python virtual environment, and install Streamlit along with the base project dependencies.

Phase 2 — UI Component Library Integration

Install and configure Plotly, streamlit-option-menu, and Pandas for charts, navigation, and data handling.

Phase 3 — Mock Data Layer Implementation

Define the mock dataset structure (mock/data.py) using Pakistan-specific events and sample products.

Phase 4 — Dashboard Layout & Navigation

Build the multipage Streamlit app structure — sidebar navigation, header, and main shell layout.

Phase 5 — Core Screens Development

Complete the Overview, Event Intelligence, Product Finder, Pricing Calculator, and COD Risk pages using mock data.

Phase 6 — Backend Integration (Future)

Set up FastAPI + PostgreSQL, attach real scrapers and ML models, and build Shopify/WooCommerce store connectors.

Phase 7 — Deployment & Launch

Deploy the frontend on Streamlit Community Cloud, the backend on Render/Railway, and the database on Neon/Supabase.

4.2  Mapping to Standard Project Phase Categories

1. Login and Authentication

Not defined in source documentation:  no login/authentication module or phase is mentioned. This phase is undefined and needs to be scoped separately.

2. Dashboard

Maps to Phase 4 (Dashboard Layout & Navigation) and Phase 5 (Core Screens Development):

Multipage Streamlit app structure — sidebar navigation, header, main shell layout (Phase 4)

Overview, Event Intelligence, Product Finder, Pricing Calculator, and COD Risk pages using mock data (Phase 5)

Actionable Insights Dashboard module — metrics, charts, and recommendations via visual cards and tables

3. CRUD Operations

Not defined in source documentation:  no explicit Create / Read / Update / Delete operations are defined. The closest related content is Phase 3 (Mock Data Layer Implementation), where data is read from mock/data.py — but Create, Update, and Delete are not addressed.

4. Additional Features

Maps to Phase 6 (Backend Integration — Future) and the Tier 2 / Tier 3 priority modules:

Backend Integration: FastAPI + PostgreSQL, real scrapers and ML models, Shopify/WooCommerce store connectors (Phase 6)

Tier 2 — Good to Have: City Demand Heatmap, Competitor Tracker, Dead Stock Liquidation, Smart Product Bundling

Tier 3 — Future: Local Wholesale Sourcing Estimator, Courier Cut-Off Planner, Influencer Matcher

5. Testing and Quality

Not defined in source documentation:  no testing or QA process is mentioned. This phase needs to be defined separately.

6. Deployment and Maintenance

Maps to Phase 7 (Deployment & Launch) and the deployment strategy below:

Environment

URL Type

Used By

Development

Local URL

Developer only — localhost:8501

Production

Live Public URL

Companies / clients — yourtool.streamlit.app

For real client services, the backend must also be deployed — both the frontend (Streamlit Community Cloud) and the backend (Render/Railway) + database (Neon/Supabase) must be live.

LIVE FRONTEND (Streamlit)   →   Streamlit Community Cloud  https://yourtool.streamlit.app                     │  HTTPS API calls                     ▼  LIVE BACKEND (FastAPI)   →   Render / Railway  https://api.yourtoolname.com                     │  Encrypted DB connection                     ▼  LIVE DATABASE (PostgreSQL)   →   Neon.tech / Supabase

Not defined in source documentation:  post-launch maintenance (monitoring, updates, bug-fixing cadence) is not explicitly covered — only the initial deployment strategy is documented.

5.  Design Documentation

5.1  UI / UX

Framework: Streamlit (Python) — used to build and render the dashboard UI

Navigation: streamlit-option-menu provides the sidebar navigation menu

Structure: Multipage app — Overview (app.py) plus separate pages for Event Intelligence, Winning Products, COD Risk Calculator, and My Store

Components: components/ folder holds reusable UI building blocks — cards, tables, chart wrappers — shared across pages

Visuals: Plotly — used for analytics charts and trend visualization

Presentation style: the “Actionable Insights Dashboard” module presents metrics, charts, and recommendations through simple visual cards and tables

5.2  Color and Theme

Not defined in source documentation:  no specific color palette or theme values (hex codes, primary/secondary colors) are defined. The theme configuration file (.streamlit/config.toml) is part of the project structure and is where actual color and theme values are meant to be set — but those values are not yet specified in the source material.

5.3  Font and Typography

Not defined in source documentation:  no font family, sizes, or typography scale are documented. Streamlit's default typography applies until explicitly overridden in .streamlit/config.toml.

6.  Project Memory Log

6.1  Purpose

This section is the project's running memory log — it lets future sessions (AI or team members) see what has happened so far, what is currently in progress, and what comes next. It should be refreshed after every update.

6.2  What Happened

Date

Entry

Source Documentation

Technical System Documentation created — Executive Summary, Core Features & Modules, Technology Stack, System Architecture (3 layers), Project Directory Structure, Mock Data Layer, Deployment Strategy, and the 7-phase Implementation Roadmap were defined.

This Revision

The two prior documents — the six-chapter PRD-style reference and the original nine-section technical spec — were merged into this single master document. It keeps the project-management chapters (Rules, Phase-mapping, Design, Memory Log) and restores the visual architecture and deployment diagrams and the Languages & Libraries breakdown, with no new facts invented.

6.3  Currently Working On

Per the source documentation, current focus is:

Layer 1 — Frontend UI (Streamlit, Plotly, Pandas)

Layer 2 — Mock Data & Service Client (mock/data.py + utils/api_client.py)

This corresponds to Phases 1–5 of the roadmap (Project Setup → UI Components → Mock Data → Dashboard Layout → Core Screens). Layer 3 (the real backend — FastAPI / PostgreSQL) will be attached in Phase 2 of the roadmap, with no change required to the Streamlit UI.

6.4  Updates

Date

Update

—

(record each new update here, e.g. “[Date] — what changed, what was completed, what is blocked.”)