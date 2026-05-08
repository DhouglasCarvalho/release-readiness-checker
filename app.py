import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Release Readiness Checker",
    page_icon="🚦",
    layout="wide"
)

st.title("Release Readiness Checker")
st.write(
    "A simulated product delivery case study that assesses launch readiness "
    "for features in a web-based client platform."
)

st.info(
    "Note: This project uses synthetic release data created for portfolio demonstration purposes. "
    "It is designed to resemble realistic product delivery governance without using confidential data."
)

release_data = pd.read_csv("data/release_readiness.csv")

st.subheader("Raw Release Readiness Data")
st.dataframe(release_data, width="stretch")

readiness_checks = [
    "QA_Status",
    "Product_Approval",
    "Risk_Review",
    "Documentation_Status",
    "Rollback_Plan",
    "Stakeholder_Signoff",
    "Dependency_Status"
]


def check_complete(row, field):
    value = str(row[field]).strip()

    if field == "QA_Status":
        return value == "Passed"

    if field in ["Product_Approval", "Stakeholder_Signoff"]:
        return value == "Yes"

    if field in ["Risk_Review", "Documentation_Status", "Rollback_Plan"]:
        return value == "Complete"

    if field == "Dependency_Status":
        return value == "Clear"

    return False


def calculate_readiness_score(row):
    completed_checks = 0

    for field in readiness_checks:
        if check_complete(row, field):
            completed_checks += 1

    return round((completed_checks / len(readiness_checks)) * 100, 1)


def identify_missing_items(row):
    missing_items = []

    for field in readiness_checks:
        if not check_complete(row, field):
            missing_items.append(field)

    if row["Known_Issues"] > 0:
        missing_items.append("Known_Issues")

    return ", ".join(missing_items) if missing_items else "None"


def classify_release_status(row):
    score = row["Readiness_Score"]
    known_issues = row["Known_Issues"]
    dependency_status = row["Dependency_Status"]
    qa_status = row["QA_Status"]

    if dependency_status == "Blocked" or qa_status == "Failed" or score < 60:
        return "Blocked"

    if score < 100 or known_issues > 0:
        return "At Risk"

    return "Ready"


release_data["Readiness_Score"] = release_data.apply(calculate_readiness_score, axis=1)
release_data["Missing_Items"] = release_data.apply(identify_missing_items, axis=1)
release_data["Release_Status"] = release_data.apply(classify_release_status, axis=1)

st.subheader("Analyzed Release Readiness")
st.dataframe(
    release_data[
        [
            "Release_ID",
            "Feature",
            "Product_Area",
            "Owner",
            "Release_Date",
            "Priority",
            "Readiness_Score",
            "Release_Status",
            "Known_Issues",
            "Missing_Items"
        ]
    ],
    width="stretch"
)

st.subheader("Executive Summary")

total_releases = len(release_data)
ready_count = len(release_data[release_data["Release_Status"] == "Ready"])
at_risk_count = len(release_data[release_data["Release_Status"] == "At Risk"])
blocked_count = len(release_data[release_data["Release_Status"] == "Blocked"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Releases", total_releases)
col2.metric("Ready", ready_count)
col3.metric("At Risk", at_risk_count)
col4.metric("Blocked", blocked_count)

st.subheader("Release Status Breakdown")

status_summary = (
    release_data.groupby("Release_Status")
    .agg(
        Release_Count=("Release_ID", "count"),
        Average_Readiness=("Readiness_Score", "mean"),
        Total_Known_Issues=("Known_Issues", "sum")
    )
    .reset_index()
)

status_summary["Average_Readiness"] = status_summary["Average_Readiness"].round(1)

st.dataframe(status_summary, width="stretch")

st.subheader("Readiness by Product Area")

area_summary = (
    release_data.groupby("Product_Area")
    .agg(
        Release_Count=("Release_ID", "count"),
        Average_Readiness=("Readiness_Score", "mean"),
        Blocked_Count=("Release_Status", lambda x: (x == "Blocked").sum()),
        At_Risk_Count=("Release_Status", lambda x: (x == "At Risk").sum())
    )
    .reset_index()
)

area_summary["Average_Readiness"] = area_summary["Average_Readiness"].round(1)
area_summary = area_summary.sort_values(
    by=["Blocked_Count", "At_Risk_Count", "Average_Readiness"],
    ascending=[False, False, True]
)

st.dataframe(area_summary, width="stretch")

st.subheader("Blocked or At-Risk Releases")

risk_items = release_data[release_data["Release_Status"].isin(["Blocked", "At Risk"])]

if len(risk_items) > 0:
    st.warning("The following releases require attention before launch.")

    st.dataframe(
        risk_items[
            [
                "Release_ID",
                "Feature",
                "Product_Area",
                "Owner",
                "Release_Date",
                "Priority",
                "Release_Status",
                "Readiness_Score",
                "Known_Issues",
                "Missing_Items"
            ]
        ],
        width="stretch"
    )
else:
    st.success("All releases are ready.")

st.subheader("Recommended Product Actions")

for _, row in risk_items.iterrows():
    st.write(
        f"- **{row['Feature']}** is **{row['Release_Status']}** "
        f"with a readiness score of {row['Readiness_Score']}%. "
        f"Owner: {row['Owner']}. Missing or unresolved items: {row['Missing_Items']}."
    )

st.subheader("Case Study Takeaway")

st.write(
    "This simulated release review highlights how product teams can use structured readiness checks "
    "to identify launch blockers, incomplete governance steps, and operational risks before production deployment."
)
