import streamlit as st


def apply_global_style():
    st.markdown(
        """
        <style>
        /* Main background */
        .stApp {
            background-color: #0E1117;
        /* Accent red */
        :root {
            --f1-red: #E10600;
        }

        /* Accent line under title */
        .accent-line {
            height: 3px;
            width: 60px;
            background-color: var(--f1-red);
            margin-top: 10px;
            margin-bottom: 20px;
        }

        /* Sidebar section headers */
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF;
            font-weight: 600;
        }

        /* Metric style future-proofing */
        .metric-card {
            background-color: #151922;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #1F2430;
        }
        }

        /* Remove excessive top padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #11151C;
        }

        /* Header title styling */
        .main-title {
            font-size: 42px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .sub-title {
            font-size: 18px;
            color: #A0A6B3;
            margin-top: -10px;
        }

        /* Divider */
        .custom-divider {
            border-top: 1px solid #2A2F3A;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )