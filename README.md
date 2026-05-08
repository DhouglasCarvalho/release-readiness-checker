**Streamlit:** https://release-readiness-checker-grj4kao8bht3wybfe9rndn.streamlit.app/


# Release Readiness Checker

A Streamlit-based product delivery case study that assesses launch readiness for features in a simulated web-based client platform.

## Overview

This project demonstrates how Python can help Product Managers and delivery teams evaluate whether features are ready for production release.

The app reads synthetic release data from a CSV file, calculates a readiness score, classifies each release as Ready, At Risk, or Blocked, and identifies missing launch-readiness items.

## Case Study Scenario

This project simulates a release readiness review for a B2B client-facing platform.

Each release item is evaluated across common delivery governance criteria, including QA status, product approval, risk review, documentation, rollback planning, stakeholder signoff, dependency status, and known issues.

## Portfolio Note

This project uses synthetic data created for demonstration purposes. It is designed to resemble realistic product delivery and release governance without using confidential or proprietary data.

## Product Management Use Case

Product Managers often need to assess whether features are truly ready for launch. This tool supports release governance by identifying incomplete readiness criteria, surfacing blocked or at-risk items, and producing an executive summary for stakeholders.

## Features

- Loads release readiness data from CSV
- Calculates readiness score by release item
- Classifies releases as Ready, At Risk, or Blocked
- Identifies missing readiness items
- Summarizes release status counts
- Summarizes readiness by product area
- Highlights blocked and at-risk releases
- Generates recommended product actions

## Technologies Used

- Python
- Pandas
- Streamlit

## How to Run Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the app:

```bash
python3 -m streamlit run app.py
```

## Live Demo

Streamlit App: paste-your-streamlit-url-here

## Project Purpose

This project demonstrates beginner Python skills applied to a realistic product management use case: release readiness, launch governance, and delivery risk tracking.
