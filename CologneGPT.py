
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load scent database
with open("scent_database.json", "r") as f:
    scent_data = json.load(f)

# Helper function to display scent profile
def display_scent_profile(selected_scents):
    if not selected_scents:
        st.warning("Please select at least one fragrance.")
        return

    # Aggregate notes
    note_counter = {}
    for scent in selected_scents:
        for note in scent_data[scent]["notes"]:
            note_counter[note] = note_counter.get(note, 0) + 1

    total = sum(note_counter.values())
    notes_df = pd.DataFrame({
        "Note": list(note_counter.keys()),
        "Percentage": [round((v/total)*100, 1) for v in note_counter.values()]
    })

    # Display pie chart
    fig, ax = plt.subplots()
    ax.pie(notes_df["Percentage"], labels=notes_df["Note"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.write("### Scent Breakdown")
    st.dataframe(notes_df)

# Streamlit App Layout
st.set_page_config(page_title="CologneGPT", layout="wide")
st.title("🧠 CologneGPT - Scent Analyzer")

# Sidebar - Select scents
all_scents = list(scent_data.keys())
selected_scents = st.sidebar.multiselect("Choose your favorite scents:", all_scents)

# Display selected profiles
if selected_scents:
    st.subheader("Selected Fragrances")
    for scent in selected_scents:
        st.markdown(f"**{scent}** by *{scent_data[scent]['brand']}*")
        st.markdown(f"- Type: {scent_data[scent]['type']}")
        st.markdown(f"- Notes: {', '.join(scent_data[scent]['notes'])}")

    display_scent_profile(selected_scents)
else:
    st.info("Select fragrances from the sidebar to begin analysis.")

# Custom Blend Input
st.subheader("🔬 Suggest a Custom Blend")
blend_1 = st.selectbox("Base Fragrance", [""] + all_scents)
blend_2 = st.selectbox("Top Fragrance", [""] + all_scents)

if blend_1 and blend_2 and blend_1 != blend_2:
    combined_notes = list(set(scent_data[blend_1]["notes"] + scent_data[blend_2]["notes"]))
    st.success(f"**{blend_1} + {blend_2}** could result in a custom hybrid with notes of: {', '.join(combined_notes)}")
