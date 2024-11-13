import streamlit as st
import requests

st.title("Academic Research Paper Assistant Application")

# Backend FastAPI URL
api_url = "http://localhost:8000"

# 1. Display Papers Section
st.header("Query Papers by Year")
start_year = st.number_input("Enter Start Year", min_value=2000, max_value=2024, value=2019)
query_button = st.button("Retrieve Papers")

# Initialize session state for selected paper ID
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

if query_button:
    response = requests.get(f"{api_url}/get_papers/", params={"start_year": start_year})
    if response.status_code == 200:
        papers = response.json()
        paper_id_options = {paper["title"]: paper["paper_id"] for paper in papers}
        selected_title = st.selectbox("Select a Paper", list(paper_id_options.keys()))
        st.session_state.selected_id = paper_id_options[selected_title]  # Store in session state
        st.write("Selected Paper ID:", st.session_state.selected_id)
    else:
        st.error("Error retrieving papers.")

# 2. Q&A Section
st.header("Question and Answer on Papers")
question = st.text_input("Enter Your Question")
qa_button = st.button("Get Answer")

# Use selected_id from session state for Q&A if it’s not None
if qa_button:
    if st.session_state.selected_id:
        response = requests.post(
            f"{api_url}/answer_question/",
            json={"question": question, "paper_id": st.session_state.selected_id}  # Pass paper_id as string
        )
        if response.status_code == 200:
            st.write("Answer:", response.json()["answer"])
        else:
            st.error("Error in processing the question.")
            st.write("Response content:", response.text)
    else:
        st.warning("Please select a paper before asking a question.")

# 3. Future Works Section
st.header("Generate Future Research Directions")
generate_button = st.button("Generate Future Works")

if generate_button:
    if st.session_state.selected_id:
        response = requests.post(f"{api_url}/generate_future_works/", json={"paper_id": st.session_state.selected_id})
        if response.status_code == 200:
            st.write("Future Research Suggestions:")
            st.write(response.json()["future_work"])
        else:
            st.error("Failed to generate future research directions.")
    else:
        st.warning("Please select a paper before generating future works.")


# 4. Summarize Findings Section
st.header("Summarize Findings Over a Timeframe")
year = st.number_input("Enter Year for Summary", min_value=2000, max_value=2024, value=2019)
summarize_button = st.button("Summarize Findings")

if summarize_button:
    response = requests.post(f"{api_url}/summarize_findings/", json={"year": year})
    if response.status_code == 200:
        st.write("Summary of Findings:")
        st.write(response.json()["findings_summary"])
    else:
        st.error("Failed to summarize findings.")

# 5. Generate Future Works from Summaries Section
st.header("Generate Future Work Suggestions for Papers Over a Year")
year_for_future_work = st.number_input("Enter Year for Future Work Suggestions", min_value=2000, max_value=2024, value=2019)
generate_future_works_button = st.button("Generate Future Works for the Year")

if generate_future_works_button:
    response = requests.post(f"{api_url}/generate_future_works_from_year/", json={"year": year_for_future_work})
    if response.status_code == 200:
        st.write("Suggested Future Work Areas:")
        st.write(response.json()["future_works_summary"])
    else:
        st.error("Failed to generate future work suggestions.")

# 6. Extract Key Points Section
st.header("Extract Key Points from Papers Over a Year")
year_for_key_points = st.number_input("Enter Year for Key Points Extraction", min_value=2000, max_value=2024, value=2019)
extract_key_points_button = st.button("Extract Key Points")

if extract_key_points_button:
    response = requests.post(f"{api_url}/extract_key_points/", json={"year": year_for_key_points})
    if response.status_code == 200:
        st.write("Key Points from Papers:")
        for item in response.json()["key_points"]:
            st.subheader(item["title"])
            st.write(item["key_points"])
    else:
        st.error("Failed to extract key points.")

