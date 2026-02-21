import streamlit as st
from supabase import create_client

# Setup Supabase (Add these to 'Settings > Secrets' on Streamlit Cloud)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🗞️ News-o-Matic Web Control")

# Voice Library (ElevenLabs IDs)
VOICES = {
    "Bill (News Anchor)": "JBFqnCBsd6RMkjVDRZzb",
    "Rachel (Calm/Strict)": "21m00T838D4wI36J7TQz",
    "Domino (Grumpy)": "AZnzlk1XhkpsbmfWCmEE",
}

persona = st.selectbox(
    "Pick a Persona", ["1950s Newsie", "Angry Drill Sergeant", "Sarcastic AI"]
)
voice_label = st.selectbox("Select Voice", list(VOICES.keys()))

if st.button("🔥 TRIGGER CATAPULT", type="primary"):
    supabase.table("catapult_status").update(
        {"status": "FIRE", "persona": persona, "voice_id": VOICES[voice_label]}
    ).eq("id", 1).execute()
    st.success("Signal sent to the local station!")
