from .main import SpotifyAPI

# spotify_client = SpotifyAPI()
# playlists = spotify_client.get_user_playlists()

# # Print playlists
# for playlist in playlists:
#     print(f"Name: {playlist['name']}, ID: {playlist['id']}")

# spotify_api = SpotifyAPI()
# playlists = spotify_api.get_user_playlists()
# for playlist in playlists:
#     print(f"Name: {playlist['name']}")
# playlist_id = playlists[0]['id']
# spotify_api.start_playback(playlist_id)

# Check available devices before starting playback
# devices = spotify_api.get_available_devices()
# if not devices:
#     print("No active devices found. Please ensure you have a device available for playback.")
# else:
#     # Assuming you want to start playback of the first playlist
#     if playlists:
#         playlist_id = playlists[0]['id']
#         print(f"Attempting to start playback for playlist ID: {playlist_id}")
#         try:
#             spotify_api.start_playback(playlist_id)
#             print("Playback started successfully!")
#         except Exception as e:
#             print(f"Error starting playback: {e}")
#     else:
#         print("No playlists available.")

