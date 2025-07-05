import streamlit as st
st.set_page_config(
    page_title="Smart Music Player",
    page_icon=":musical_note:",
    layout="centered"
)
import cv2
import base64
import spotipy
from fer import FER
from spotipy.oauth2 import SpotifyClientCredentials
import test
import random
from PIL import Image

# Mapping moods to background images
mood_backgrounds = {
    "Happy": './images/happy_background.jpeg',
    "Sad": './images/sad_background.png',
    "Angry": './images/angry_background.png',
    "Surprise": './images/surprise_background.png',
    "Neutral": './images/neutral_background.png'
}

# Default background
default_background = './images/mainbackground.png'
current_background = default_background

# Load and display background image
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string.decode()});
                background-size: cover;
                background-position: center;
                transition: background-image 0.5s ease-in-out;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Background image {image_file} not found. Using default.")
        with open(default_background, "rb") as default_file:
            encoded_string = base64.b64encode(default_file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string.decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Enhanced styling for better UI
def apply_custom_styles():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Rancho&display=swap');
            
            /* Main font styling */
            html, body, [class*="css"] {
                font-family: 'Rancho', cursive;
                font-size: 1.5rem;
                color: white;
            }
            
            /* Card styling for content */
            .mood-card {
                background-color: rgba(0, 0, 0, 0.6);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                backdrop-filter: blur(5px);
            }
            
            /* Button styling */
            .stButton>button {
                background-color: #1DB954;
                color: white;
                border-radius: 25px;
                border: none;
                padding: 10px 24px;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .stButton>button:hover {
                background-color: #1ED760;
                transform: scale(1.05);
            }
            
            /* Select box styling */
            .stSelectbox {
                border-radius: 25px;
            }
            
            /* Music player frame styling */
            iframe {
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                margin-bottom: 15px;
            }
            
            /* Title styling */
            h1, h2, h3 {
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            /* Add gradient overlay for text readability */
            .gradient-overlay {
                background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0));
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# Spotify API credentials
client_id = '63a99a02f8e64c88822600101409910d'
client_secret = '2f52159b3c8940ad9ae9d36cecdf7d0d'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Emotion Detector
emotion_detector = FER(mtcnn=True)

# Apply default background first
add_bg_from_local(default_background)
apply_custom_styles()



st.markdown('<div class="gradient-overlay">', unsafe_allow_html=True)
st.title('✨ Mood Music Magic ✨')
st.markdown('**Let your emotions guide your music experience**')
st.markdown('</div>', unsafe_allow_html=True)

# User input options in a card
st.markdown('<div class="mood-card">', unsafe_allow_html=True)
st.subheader("🎭 How would you like to set your mood?")
col1, col2 = st.columns(2)
with col1:
    auto_mood = st.checkbox('📷 Auto Mood Detection')
with col2:
    manual_mood = st.checkbox('🎯 Manual Selection')
st.markdown('</div>', unsafe_allow_html=True)

# Initialize variables
mood = None
playlist_id = None

# Manual mood selection with enhanced styling
if manual_mood:
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    mood = st.selectbox(
        '💭 How are you feeling today?',
        ('Select', 'Happy', 'Sad', 'Angry', 'Neutral', 'Surprise')
    )
    
    if mood and mood != 'Select':
        st.markdown(f"<h3>You're feeling: {mood} 🎵</h3>", unsafe_allow_html=True)
        
        # Update background based on mood
        current_background = mood_backgrounds.get(mood, default_background)
        add_bg_from_local(current_background)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if mood == 'Select':
        mood = None

# Automatic mood detection with enhanced UI
if auto_mood:
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    st.subheader("📸 Let's capture your mood")
    
    if st.button("Take a photo"):
        with st.spinner("Capturing..."):
            test.capture_image()
        
        img_path = './images/photo.png'
        test_img = cv2.imread(img_path)
        
        # Show captured image
        captured_img = Image.open(img_path)
        st.image(captured_img, width=300, caption="Captured Image")
        
        # Detect emotions with loading spinner
        with st.spinner("Analyzing your mood..."):
            analysis = emotion_detector.detect_emotions(test_img)
            dominant_emotion, emotion_score = emotion_detector.top_emotion(test_img)
        
        if dominant_emotion:
            mood = dominant_emotion.capitalize()
            st.success(f"✅ Detected Mood: **{mood}**")
            
            # Update background based on detected mood
            current_background = mood_backgrounds.get(mood, default_background)
            add_bg_from_local(current_background)
            
            # Show emotion scores
            st.markdown("### Emotion Analysis")
            if analysis and len(analysis) > 0:
                emotions = analysis[0]['emotions']
                # Create a bar chart for emotions
                emotion_data = {
                    'Emotion': list(emotions.keys()),
                    'Score': list(emotions.values())
                }
                st.bar_chart(emotion_data, x='Emotion', y='Score')
        else:
            st.error("😕 Emotion detection failed. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Mapping moods to Spotify playlists
mood_to_playlist = {
    "Happy": '0dCVqMbiEbqx0irSf9MiRG',
    "Sad": '3CcAgt9Et5WgV4ntXAK2gW',
    "Angry": '1EosQ12lOcxZtYX2VafShA',
    "Surprise": '13Wo7f4zf0dJRj23a23aI3',
    "Neutral": '2mrsAZIdbLVIHGOwHxidWb'
}

# Mood descriptions for better UX
mood_descriptions = {
    "Happy": "Upbeat tunes to keep your good vibes going! 🎵",
    "Sad": "Melancholic melodies that understand how you feel 🌧️",
    "Angry": "Power tracks to channel your energy 💥",
    "Surprise": "Unexpected beats for your curious mind ✨",
    "Neutral": "Balanced tunes for your relaxed state 🌊"
}

# Assign playlist based on mood
if mood:
    playlist_id = mood_to_playlist.get(mood)

# Function to fetch track IDs
def get_track_ids(playlist_id):
    try:
        music_id_list = []
        playlist = sp.playlist(playlist_id)
        for item in playlist['tracks']['items']:
            if item['track']:
                music_id_list.append(item['track']['id'])
        return music_id_list
    except Exception as e:
        st.error(f"Error fetching playlist: {e}")
        return []

# Display songs if a playlist is selected with enhanced styling
if playlist_id:
    track_ids = get_track_ids(playlist_id)

    if track_ids:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        
        # Mood-specific header
        st.subheader(f"🎧 {mood} Music Selection")
        st.markdown(mood_descriptions.get(mood, "Here are some songs that match your mood"))
        
        # Sample tracks and display with enhanced styling
        selected_tracks = random.sample(track_ids, min(5, len(track_ids)))
        
        for i, track_id in enumerate(selected_tracks):
            # Get track info for better display
            track_info = sp.track(track_id)
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            
            # Display track with numbering
            st.markdown(f"**{i+1}. {track_name}** by {artist_name}")
            st.markdown(
                f'<iframe src="https://open.spotify.com/embed/track/{track_id}" '
                'width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
                unsafe_allow_html=True
            )
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("No tracks found for the selected playlist.")
elif not mood:
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    st.info("Select or detect your mood to get personalized music recommendations")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; color: white">
    <p>Made with ❤️ | Mood Music Magic | © 2025</p>
</div>
""", unsafe_allow_html=True)