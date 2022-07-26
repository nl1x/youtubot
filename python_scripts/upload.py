import os, datetime, json
from typing import Literal

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload



class Uploader:
    
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.is_logged_in = False
        
        self.NOT_LOGGED_IN = "You're not logged in. Use 'login()' method to login or 'get_session()' method to load a session."
    
    
    def load_session(self, file: str):
        self.credentials = Credentials.from_authorized_user_file(file, self.scopes)
    
        # if self.credentials.expired:
        #     self.credentials.refresh(Request(self.credentials))
    
        self.is_logged_in = True

        print(f"Credentials successfuly loaded from {file}.")
    
    
    def save_session(self, file: Literal['*.json']):
        assert self.is_logged_in, self.NOT_LOGGED_IN
        
        with open(file, 'w') as file_object:
            json.dump(json.loads(self.credentials.to_json()), file_object, indent=4)
            print(f"Credentials successfuly saved in {file}.")

        
    def login(self, client_secrets_path: str, token_file=None):
        """
        Login to your Youtube Channel.
        Your session will be saved in 'youtube' property.
        """
        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        
        client_secrets_file = client_secrets_path

        # Get credentials and create an API client
        if token_file:
            self.load_session(token_file)
            credentials = self.credentials
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, self.scopes
            )
            credentials = flow.run_console()
            self.credentials = credentials
            

        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        self.is_logged_in = True
        

    def upload(self, media_path: str, thumbnail_path: str, game_name: str, video_count: int):
        """
        Upload a video on Youtube
        
        ----
        
        Parameters:
        
        `media_path` : str -> Video to upload.

        `thumbnail_path` : str -> Thumbnail of the video.

        `video_count` : int -> Number of the video.
        """
        assert self.is_logged_in, self.NOT_LOGGED_IN
        
        upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

        request = self.youtube.videos().insert(
            part="snippet,status",
            notifySubscribers=True,
            body={
            'snippet': {
                'title': f'{game_name} Twitch clips of the day #{video_count}',
                'categoryId': 20,
                'description': f'{game_name} Twitch clips of the day #{video_count}.\nThis channel upload videos automatically every weeks.\n\n🌐 Join our community on discord: https://discord.gg/4BX8WSy5u5 \n❤ Subscribe: https://www.youtube.com/channel/UC24XlMIbqrd_5ItVFp04MLg?sub_confirmation=1',
                'tags': [
                    f'{game_name} twitch clips',
                    f'{game_name} twitch clips of the day',
                    f'{game_name} twitch clips {video_count}',
                    f'{game_name} twitch clips compilation',
                    f'twitch clips compilation',
                    f'twitch clips of the week',
                    f'automatic youtube channel',
                    f'automated youtube channel',
                    f'automatic channel',
                    f'automated channel',
                    f'daily upload',
                    f'automated {game_name}',
                    f'video games',
                    f'jeux videos',
                    f'gaming',
                    f'Clips twitch du jour',
                    f'Compilation de clip twitch',
                    f'{game_name}'
                ]
            },
            'status': {
                'privacyStatus': 'public',
                'pulishAt': upload_date_time,
                'selfDeclaredMadeForKids': False
            }
        },
            
            # TODO: For this request to work, you must replace "YOUR_FILE"
            #       with a pointer to the actual file you are uploading.
            media_body=MediaFileUpload(media_path)
        )
        response = request.execute()
        
        self.youtube.thumbnails().set(
            videoId=response.get('id'),
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()

        print("Your video has been succesfully uploaded !")


if __name__ == "__main__":
    """
    A tester pour valider
    """
    upload = Uploader()
    upload.login(
        "",
        # client_secrets_path='assets/tools/tokens/youtube_secret.json', 
        token_file='assets/tools/tokens/youtube_token.json'
    )
    upload.save_session('assets/tools/tokens/youtube_token.json')
    upload.load_session('assets/tools/tokens/youtube_token.json')
    upload.upload("assets/output/video.mp4", "assets/output/thumbnail.png", 'VALORANT', 5)
    print('end')
