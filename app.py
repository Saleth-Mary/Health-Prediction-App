
import streamlit as st
import pandas as pd

from database import (
    create_table,
    add_patient,
    get_all_patients,
    update_patient_email,
    delete_patient,
    get_patient_by_id,
    update_patient_remarks,
    add_failed_record,
    get_failed_records
)

from validation import validate_patient, validate_email
from ai_service import generate_health_remarks


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Patient Health Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()


# --------------------------------------------------
# 2. CUSTOM CSS - PREMIUM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F7F8F6;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background-color: #172B3A;
}

[data-testid="stSidebar"] * {
    color: #F5F7F6;
}

[data-testid="stSidebar"] hr {
    border-color: #40515D;
}

.main-title {
    font-family: 'Playfair Display', serif;
    color: #172B3A;
    font-size: 34px;
    font-weight: 700;
}

.subtitle {
    color: #71808A;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-title {
    color: #172B3A;
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
}

.section-description {
    color: #78858C;
    font-size: 13px;
}

.metric-card {
    background-color: #FFFFFF;
    padding: 22px;
    border: 1px solid #E6EBE8;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(23, 43, 58, 0.03);
}

.metric-label {
    color: #74818A;
    font-size: 13px;
    font-weight: 500;
}

.metric-value {
    color: #172B3A;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.form-card {
    background-color: #FFFFFF;
    padding: 22px;
    border: 1px solid #E5EAE7;
    border-radius: 12px;
    margin-bottom: 18px;
}

div[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 1px solid #E5EAE7;
    border-radius: 12px;
    padding: 25px;
}

.stButton > button,
.stFormSubmitButton > button {
    background-color: #247F78;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #195F5A;
    color: white;
    border: none;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 7px;
}

.footer {
    color: #89949A;
    font-size: 12px;
    text-align: center;
    padding-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------

def get_records():
    return get_all_patients()


def show_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🏥 HEALTHCARE")

    st.caption("PATIENT MANAGEMENT SYSTEM")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Add Patient",
            "Patient Records",
            "Failed Records",
            "Manage Patients"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.caption("AI-ASSISTED HEALTH ANALYTICS")

    st.caption("Version 1.0")


# --------------------------------------------------
# 5. FETCH DATABASE RECORDS
# --------------------------------------------------

records = get_records()
failed_records = get_failed_records()


# --------------------------------------------------
# 6. DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Patient Health Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Monitor patient registrations and AI-assisted interpretations.</div>',
        unsafe_allow_html=True
    )

    total_patients = len(records)

    ai_completed = sum(
        1 for r in records
        if r["remarks"]
        and not r["remarks"].startswith(
            "AI interpretation is currently unavailable"
        )
    )

    pending = total_patients - ai_completed

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric("TOTAL PATIENT RECORDS", total_patients)

    with col2:
        show_metric("AI INTERPRETATIONS", ai_completed)

    with col3:
        show_metric("PENDING INTERPRETATIONS", pending)

    st.write("")

    st.markdown(
        '<div class="section-title">Recent Patient Registrations</div>',
        unsafe_allow_html=True
    )

    if records:

        df = pd.DataFrame(records)

        display_columns = [
            "id",
            "full_name",
            "dob",
            "email",
            "glucose",
            "haemoglobin",
            "cholesterol"
        ]

        st.dataframe(
            df[display_columns].tail(5).iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No patient records available yet.")

    st.markdown(
        '<div class="footer">Patient Health Prediction System | Educational use only</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 7. ADD PATIENT
# --------------------------------------------------

elif page == "Add Patient":

    st.markdown(
        '<div class="main-title">Patient Registration</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Enter patient information and laboratory test results.</div>',
        unsafe_allow_html=True
    )

    # Patient registration form
    with st.form("patient_form"):

        st.markdown("### Personal Information")

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input(
                "Full Name *",
                placeholder="Enter full name"
            )

            email = st.text_input(
                "Email Address *",
                placeholder="example@email.com"
            )

        with col2:

            dob = st.text_input(
                "Date of Birth *",
                placeholder="DD/MM/YYYY"
            )

        st.divider()

        st.markdown("### Blood Test Information")

        st.caption(
            "Enter the values exactly as reported by the laboratory. "
            "Confirm units and reference ranges before clinical interpretation."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            glucose = st.text_input(
                "Glucose *",
                placeholder="e.g. 95"
            )

        with col2:

            haemoglobin = st.text_input(
                "Haemoglobin *",
                placeholder="e.g. 13.5"
            )

        with col3:

            cholesterol = st.text_input(
                "Cholesterol *",
                placeholder="e.g. 180"
            )

        st.write("")

        submitted = st.form_submit_button(
            "Save Patient Record",
            use_container_width=True
        )

    # --------------------------------------------------
    # SAVE PATIENT WITHOUT CALLING GEMINI
    # --------------------------------------------------

    if submitted:

        # Clear previously selected patient for this registration attempt.
        st.session_state.pop("saved_patient_id", None)

        patient = {
            "full_name": full_name,
            "dob": dob,
            "email": email,
            "glucose": glucose,
            "haemoglobin": haemoglobin,
            "cholesterol": cholesterol
        }

        # Preserve original values before validation.
        original_patient = patient.copy()

        errors = validate_patient(patient)

        if errors:

            # Determine test number.
            test_number = len(records) + len(failed_records) + 1

            # Store rejected record separately.
            add_failed_record(
                test_number,
                original_patient["full_name"],
                original_patient["dob"],
                original_patient["email"],
                original_patient["glucose"],
                original_patient["haemoglobin"],
                original_patient["cholesterol"],
                "; ".join(errors)
            )

            st.error(
                "This patient record was rejected because validation failed."
            )

            for error in errors:
                st.warning(error)

            st.info(
                f"Test {test_number} has been saved in Failed Records. "
                "It has not been added to the patient database."
            )

        else:

            try:

                # Save patient with empty AI remarks.
                patient_id = add_patient(
                    patient["full_name"],
                    patient["dob"],
                    patient["email"],
                    patient["glucose"],
                    patient["haemoglobin"],
                    patient["cholesterol"],
                    None
                )

                # Remember the saved patient's ID.
                st.session_state["saved_patient_id"] = patient_id

                st.success(
                    f"Patient record saved successfully! Patient ID: {patient_id}"
                )

                st.info(
                    "Your patient record is now stored in SQLite. "
                    "You can generate the AI interpretation separately below."
                )

            except Exception as e:

                st.error(f"Unable to save patient record: {e}")

    # --------------------------------------------------
    # GENERATE AI INTERPRETATION SEPARATELY
    # --------------------------------------------------

    saved_patient_id = st.session_state.get("saved_patient_id")

    if saved_patient_id is not None:

        saved_patient = get_patient_by_id(saved_patient_id)

        if saved_patient:

            st.divider()

            st.markdown("### AI Health Interpretation")

            st.write(
                f"Patient: **{saved_patient['full_name']}** "
                f"(ID: {saved_patient_id})"
            )

            current_remarks = saved_patient["remarks"]

            if (
                current_remarks
                and not current_remarks.startswith(
                    "AI interpretation is currently unavailable"
                )
            ):

                st.success("AI interpretation is already available.")

                st.info(current_remarks)

            else:

                st.caption(
                    "Click the button below when you want Gemini to interpret "
                    "the patient's blood test values."
                )

                if st.button(
                    "Generate AI Interpretation",
                    use_container_width=True,
                    key="generate_ai_interpretation"
                ):

                    try:

                        with st.spinner(
                            "Generating AI-assisted health interpretation..."
                        ):

                            remarks = generate_health_remarks(
                                saved_patient["glucose"],
                                saved_patient["haemoglobin"],
                                saved_patient["cholesterol"]
                            )

                        # Update existing patient record.
                        update_patient_remarks(
                            saved_patient_id,
                            remarks
                        )

                        st.success(
                            "AI interpretation generated and saved successfully!"
                        )

                        st.rerun()

                    except Exception as e:

                        # Store failure message so the user can retry.
                        fallback_remarks = (
                            "AI interpretation is currently unavailable. "
                            "Please retry later."
                        )

                        update_patient_remarks(
                            saved_patient_id,
                            fallback_remarks
                        )

                        st.error(
                            "Gemini is temporarily unavailable. "
                            "Your patient record is safe. You can retry later."
                        )

                        st.caption(str(e))


# --------------------------------------------------
# 8. PATIENT RECORDS
# --------------------------------------------------

elif page == "Patient Records":

    st.markdown(
        '<div class="main-title">Patient Records</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View and search all registered patient records.</div>',
        unsafe_allow_html=True
    )

    if records:

        search = st.text_input(
            "Search by patient name or email",
            placeholder="Enter patient name or email"
        )

        df = pd.DataFrame(records)

        if search:

            df = df[
                df["full_name"].str.contains(
                    search, case=False, na=False
                )
                |
                df["email"].str.contains(
                    search, case=False, na=False
                )
            ]

        st.write(f"Records found: {len(df)}")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No patient records found. Please register a patient first."
        )


# --------------------------------------------------
# 9. FAILED RECORDS
# --------------------------------------------------

elif page == "Failed Records":

    st.markdown(
        '<div class="main-title">Failed Records</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View rejected entries and their validation reasons. These records are stored separately and are not included in patient records.</div>',
        unsafe_allow_html=True
    )

    failed_records = get_failed_records()

    if failed_records:

        failed_df = pd.DataFrame(failed_records)

        display_columns = [
            "test_number",
            "full_name",
            "dob",
            "email",
            "glucose",
            "haemoglobin",
            "cholesterol",
            "error_reason"
        ]

        st.write(f"Rejected records: {len(failed_df)}")

        st.dataframe(
            failed_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No failed records have been recorded yet.")


# --------------------------------------------------
# 10. MANAGE PATIENTS
# --------------------------------------------------

elif page == "Manage Patients":

    st.markdown(
        '<div class="main-title">Manage Patients</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Update patient email addresses or remove records.</div>',
        unsafe_allow_html=True
    )

    if records:

        patient_options = {
            f'ID {r["id"]} - {r["full_name"]} ({r["email"]})': r["id"]
            for r in records
        }

        selected_patient = st.selectbox(
            "Select Patient",
            list(patient_options.keys())
        )

        patient_id = patient_options[selected_patient]

        patient = get_patient_by_id(patient_id)

        if patient:

            st.markdown("### Patient Information")

            st.write("**Name:**", patient["full_name"])
            st.write("**Date of Birth:**", patient["dob"])
            st.write("**Current Email:**", patient["email"])

            st.divider()

            # Retry AI interpretation if unavailable or not generated.
            if (
                not patient["remarks"]
                or patient["remarks"].startswith(
                    "AI interpretation is currently unavailable"
                )
            ):

                st.markdown("### AI Interpretation")

                if st.button("Generate / Retry AI Interpretation"):

                    try:

                        with st.spinner(
                            "Generating AI interpretation..."
                        ):

                            remarks = generate_health_remarks(
                                patient["glucose"],
                                patient["haemoglobin"],
                                patient["cholesterol"]
                            )

                        update_patient_remarks(patient_id, remarks)

                        st.success(
                            "AI interpretation generated successfully!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            "Gemini is still unavailable. Please try again later."
                        )

                        st.caption(str(e))

            elif patient["remarks"]:

                st.markdown("### AI-Generated Remarks")

                st.info(patient["remarks"])

            st.divider()

            # Update patient email
            st.markdown("### Update Email Address")

            with st.form("edit_patient_form"):

                new_email = st.text_input(
                    "New Email Address",
                    value=patient["email"]
                )

                update_button = st.form_submit_button(
                    "Update Email Address"
                )

            if update_button:

                valid, message = validate_email(new_email)

                if valid:

                    update_patient_email(
                        patient_id,
                        new_email
                    )

                    st.success(
                        "Patient email updated successfully!"
                    )

                    st.rerun()

                else:

                    st.error(message)

            st.divider()

            # Delete patient
            st.markdown("### Delete Patient")

            confirm_delete = st.checkbox(
                "I confirm that I want to permanently delete this patient record."
            )

            if st.button("Delete Patient", type="secondary"):

                if confirm_delete:

                    delete_patient(patient_id)

                    # Clear session reference if this patient was selected.
                    if st.session_state.get("saved_patient_id") == patient_id:
                        st.session_state.pop("saved_patient_id", None)

                    st.success(
                        "Patient record deleted successfully!"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please confirm before deleting the record."
                    )

    else:

        st.info("No patient records available to manage.")


# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">Patient Health Prediction System | Powered by Python, SQLite and Google Gemini</div>',
    unsafe_allow_html=True
)
