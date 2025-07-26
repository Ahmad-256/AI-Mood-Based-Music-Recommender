import streamlit as st
import pandas as pd
import joblib

# Load model and dataset
model = joblib.load("knn_model.pkl")
df = pd.read_csv("music_dataset.csv")

# Mood icons
mood_icons = {
    "Calm": ("🧘‍♂️", "#6c5ce7"),
    "Happy": ("😊", "#00b894"),
    "Energetic": ("⚡", "#fdcb6e"),
    "Neutral": ("🙂", "#636e72"),
    "Sad": ("😢", "#74b9ff")
}

# Session state setup
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None
if "page" not in st.session_state:
    st.session_state.page = 0

# Sidebar mood selection
st.sidebar.markdown("<h3>🎭 Select Your Mood</h3>", unsafe_allow_html=True)
for mood, (emoji, _) in mood_icons.items():
    if st.sidebar.button(f"{emoji} {mood}", key=mood):
        st.session_state.selected_mood = mood
        st.session_state.page = 0  # Reset to page 0 on mood change

selected_mood = st.session_state.selected_mood

# Page title
st.markdown("""
<div class="title-bar" style="background: linear-gradient(90deg, #4e54c8, #8f94fb); padding: 1rem; border-radius: 10px; text-align:center; color:white;">
    <h2 style="margin-bottom:0.2rem;">🎵 AI Mood-Based Music Recommender</h2>
    <p style="margin:0;">Get music that matches your current vibe.</p>
</div>
""", unsafe_allow_html=True)

# Recommendations
if selected_mood:
    st.success(f"Showing songs for: {selected_mood}")
    filtered = df[df['mood'].str.lower() == selected_mood.lower()].reset_index(drop=True)

    songs_per_page = 5
    total_pages = max(1, (len(filtered) - 1) // songs_per_page + 1)

    # Get songs for current page
    start = st.session_state.page * songs_per_page
    end = start + songs_per_page
    current_songs = filtered.iloc[start:end]

    # Show songs
    for _, row in current_songs.iterrows():
        total_seconds = int(row['duration_min'] * 60)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        st.markdown(f"""
            <div style="background:white; padding:1rem; border-radius:10px; margin:1rem 0; box-shadow:0 4px 12px rgba(0,0,0,0.07);">
                <h4 style="display: flex; justify-content: space-between; align-items: center;">
    🎶 {row['track_name']}
    <span style="font-size:16px; color: gold;">{'★' * int(row['popularity'] // 20)}{'☆' * (5 - int(row['popularity'] // 20))}</span>
</h4>
                <p><b>Artist 🎙:</b> {row['artist_name']}</p>
                <p><b>Type 🎬:</b> {row['genre']}</p>
                <p><b>Duration ⏱:</b> {minutes} min {seconds} sec</p>
            </div>
        """, unsafe_allow_html=True)

    # Pagination controls at bottom
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Prev", key="prev_btn") and st.session_state.page > 0:
            st.session_state.page -= 1
    with col3:
        if st.button("Next ➡️", key="next_btn") and st.session_state.page < total_pages - 1:
            st.session_state.page += 1
    with col2:
        st.markdown(
            f"<div style='text-align:center;'>Page {st.session_state.page + 1} of {total_pages}</div>",
            unsafe_allow_html=True
        )

else:
    st.info("👈 Choose a mood from the sidebar to see song suggestions.")
