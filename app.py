import pickle
import webbrowser
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "6af5f00494464049b17c43bccddc2b45"
CLIENT_SECRET = "668ac2208a474ccfb401bbe4a9b81b4c"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_page_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_url = track['external_urls']['spotify']
        return song_url
        # Get the first result's Spotify URL
        # track = results['tracks']['items'][0]
        # album_id = track['album']['id']
        # album_page_url = f"https://open.spotify.com/album/{album_id}"
        # return album_page_url
    else:
        return None
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_url = []
    for i in distances[1:10]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_url.append(get_song_album_page_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names,recommended_music_posters,recommended_music_url

st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_music_urls = recommend(selected_song)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i in range(5):
        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
            st.success(f"Spotify URL: [Open on Spotify]({recommended_music_urls[i]})")
            if st.button("Open on Spotify"):
                webbrowser.open(recommended_music_urls[i])





