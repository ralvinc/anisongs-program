from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

# Necessary scopes for YouTube API access
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# OAuth Section
def authenticate():
    # OAuth 2.0 flow setup
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES
    )
    
    # Run the OAuth flow at localhost:8000
    credentials = flow.run_local_server(port=8000)
    
    # Return authenticated YouTube API client
    return build('youtube', 'v3', credentials=credentials)

# JIKAN API Section
def search_anime(query):
    base_url = 'https://api.jikan.moe/v4'
    response = requests.get(
                f"{base_url}/anime",
                params = {
                    "q": query,
                    "order_by": 'popularity',
                    "limit": 25,
                    "sfw": 'true'
                }
    )
    data = response.json()

    results = data['data']
    approved_results = [result for result in results if result.get('approved', False)]
    
    return approved_results

def display_anime_results(results):
    print("\nSearch results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")

def select_anime(results):
    while True:
        choice = input("\nEnter the number of the anime you want to select: ")

        if not choice.isdigit():
            print("Invalid choice. Please enter a number within the range of results.")
            continue

        choice = int(choice)

        if choice < 1 or choice > len(results):
            print("Invalid choice. Please enter a number within the range of results.")
            continue

        return results[choice - 1]

def get_theme_songs(anime_id):
    def sort_theme_songs(themes):
        themes.sort(key=lambda theme: int(theme.split(":")[0]) if ':' in theme else float("inf"))

    base_url = 'https://api.jikan.moe/v4'
    response = requests.get(
                f"{base_url}/anime/{anime_id}/themes"
    )
    data = response.json()

    themes = data['data']
    openings = themes['openings']
    endings = themes['endings']

    sort_theme_songs(openings)
    sort_theme_songs(endings)

    return openings, endings

def display_theme_songs(openings, endings):
    def clean_theme_songs_title(title):
        colon_index = title.find(':')
        if colon_index != -1 and colon_index < 3:
            title = title[colon_index + 1:].strip()
        
        return title

    print("\nOpenings:")
    if not openings:
        print("No results found.")
    else:
        for i, opening in enumerate(openings, 1):
            opening = clean_theme_songs_title(opening)
            print(f"{i}. {opening}")

    print("\nEndings:")
    if not endings:
        print("No results found.")
    else:
        for i, ending in enumerate(endings, len(openings) + 1):
            ending = clean_theme_songs_title(ending)
            print(f"{i}. {ending}")

def select_theme_song(openings, endings):
    while True:
        choice = input("\nEnter the number of the theme song you want to select: ")

        if not choice.isdigit():
            print("Invalid choice. Please enter a number within the range of results.")
            continue

        choice = int(choice)

        if choice < 1 or choice > (len(openings) + len(endings)):
            print("Invalid choice. Please enter a number within the range of results.")
            continue

        if choice <= len(openings):
            return openings[choice - 1]
        else:
            return endings[choice - len(openings) - 1]

# YouTube API Section
def search_video(query):
    search_response = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=1,
        type='video'
    ).execute()
    
    # Get video ID of the search result
    if search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
    
        return video_id
    else:
        return -1

def get_playlists():
    # Get authenticated user's playlists
    playlists_response = youtube.playlists().list(
        part='snippet',
        mine=True
    ).execute()
    
    return playlists_response['items']

def create_playlist(playlist_title):
    # Create a private playlist
    playlist = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': playlist_title
            },
            'status': {
                'privacyStatus': 'private'  
            }
        }
    ).execute()
    
    # Get playlist ID
    playlist_id = playlist['id']
    
    return playlist_id

def insert_video_into_playlist(video_id, playlist_id):
    # Insert video into the selected playlist
    youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    ).execute()

# Authenticate user's YouTube account
youtube = authenticate()

while True:
    # Request for an anime title
    while True:
        anime_title = input("\nEnter the title of an anime: ")
        anime_results = search_anime(anime_title)

        if not anime_results:
            print("No results found. Try using the anime's Japanese name if the English name does not work and vice versa.")
            continue

        break  

    # Display and select anime
    display_anime_results(anime_results)
    selected_anime = select_anime(anime_results)

    # Display and select theme song
    anime_id = selected_anime['mal_id']
    openings, endings = get_theme_songs(anime_id)

    if not openings and not endings:
        print("\nNo anime themes found.")
    else:
        display_theme_songs(openings, endings)
        selected_theme_song = select_theme_song(openings, endings)

        # Clean theme song title if needed
        colon_index = selected_theme_song.find(':')
        if colon_index != -1 and colon_index < 3:
            selected_theme_song = selected_theme_song[colon_index + 1:].strip()
        
        eps_index = selected_theme_song.find('(eps')
        if eps_index != -1:
            video_query = selected_theme_song[:eps_index]
        else:
            video_query = selected_theme_song

        # Get youtube video id 
        video_id = search_video(video_query)

        if video_id == -1:
            print("\nYouTube video not found.")
        else:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"\nYouTube video URL: {video_url}")

            add_to_playlist = input("Do you want to add this video to one of your YouTube playlists? (y/n): ")

            while add_to_playlist.lower() != 'y' and add_to_playlist.lower() != 'n':
                add_to_playlist = input("Select a valid option. (y/n): ")
            
            # Add youtube video to selected playlist
            if add_to_playlist.lower() == 'y':
                playlists = get_playlists()

                print("\nSelect a playlist to add the video to:")
                print("0. Create new playlist")
                for i, playlist in enumerate(playlists, 1):
                    print(f"{i}. {playlist['snippet']['title']}")
                
                while True:
                    selected_playlist_index = input("\nEnter the number of the playlist: ")

                    if not selected_playlist_index.isdigit():
                        print("Invalid choice. Please enter a number within the range of results.")
                        continue

                    selected_playlist_index = int(selected_playlist_index)

                    if selected_playlist_index < 0 or selected_playlist_index > len(playlists):
                        print("Invalid choice. Please enter a number within the range of results.")
                        continue

                    break

                if selected_playlist_index == 0:
                    playlist_title = input("Enter a title for the playlist: ")
                    selected_playlist_id = create_playlist(playlist_title)
                else:    
                    selected_playlist_id = playlists[selected_playlist_index - 1]['id']
                
                insert_video_into_playlist(video_id, selected_playlist_id)
                print("Video added to playlist.")

    another_action = input("\nDo you want to perform another action? (y/n): ")

    while another_action.lower() != 'y' and another_action.lower() != 'n':
        another_action = input("Select a valid option. (y/n): ")

    if another_action.lower() != 'y':
        break
