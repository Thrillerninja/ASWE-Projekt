from api.api_factory import APIFactory
from config.config import CONFIG

factory = APIFactory(CONFIG)
spotify = factory.create_api('spotify')
playlists = spotify.get_user_playlists()
for playlist in playlists:
    print(f"Name: {playlist['name']}")
devices = spotify.get_available_devices()
for device in devices:
    print(device)
# lars_laptop_device_id = "f53c0d6c8f3de3c02c0bbfbd46aedcd5c275e37c"
lars_phone_device_id = "617cac45b44cc1d8ce6dcdccc8446f89801bf05d"
spotify.start_playback(playlists[0], lars_phone_device_id)