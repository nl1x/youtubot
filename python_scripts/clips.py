from datetime import timedelta, datetime
import json
import requests

class TwitchAPI:

    def __init__(self):
        self.headers = None

    def connect_to_api(self, client_id: str, client_secret: str):
        '''
        Get a Twitch API session.
        
        --------------------------------

        Parameters:
        -----------
                `client_id`: str
                `client_secret`: str
                
                --> Both of those parameters can be found on the Twitch API Console (https://dev.twitch.tv/console)
                
                --> Steps :
                    1) Register / Login to Twitch. 
                    
                    2) Create an `application` on the 'Applications' tab 
                        /!\ Your application name can't contain 'twitch'
                        /!\ OAuth redirect URL can be http://localhost
                        
                    3) Go to 'Manage' 
                    
                    4) You can find `client_id` on the section `Client Identity` 
                    
                    5) You can find `client_secret` on the section `Client Secret` by clicking on `New secret` 
        
        --------------------------------
        
        Return:
        -------
                Nothing        
        '''
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        connection_request = requests.post('https://id.twitch.tv/oauth2/token', body)
        if not connection_request.ok:
            raise requests.exceptions.RequestException(connection_request.content)

        token = connection_request.json()['access_token']
        self.headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + token
        }
        
    
    def save_session(self, file: str):
        ''' Save your session in the file.
        
        ------------------------------------------------
        
        Parameters:
        -----------
        
            `file`: str
            - Must be a `.json` file.
        '''
        assert file.endswith('.json'), "Your file must be a '.json' file."

        with open(file, 'w') as file_obj:
            json.dump(self.headers, file_obj, indent=4)

        print(f'Twitch session successfuly saved in {file}.')
        
    
    def load_session(self, file: str):
        ''' Load your session in the file.
        
        ------------------------------------------------
        
        Parameters:
        -----------
        
            `file`: str
            - Must be a `.json` file.
        '''
        assert file.endswith('.json'), "Your file must be a '.json' file."
        
        with open(file, 'r') as file_obj:
            self.headers = json.load(file_obj)
        
        print(f"Your session has been successfuly loaded from {file}.")
    
    
    def get_stream_data(self):
        # EXAMPLE OF REQUEST :
        # stream = requests.get('https://api.twitch.tv/helix/clips?broadcaster_id=70225218', headers=headers)

        # print(stream.content)
        # stream_data = stream.json()

        # print(stream_data)
        ...
    
    
    def get_game_id(self, name: str):
        ''' Get the `game_id` of a game.
        
        --------------------------------------------------
        
        Parameters:
        -----------
        
            `name`: str
            - The game you are searching its id.
        
        Returns:
        --------
        
            `game_id`: str
            - The game's identifier.
        '''
        
        game_request = requests.get(f'https://api.twitch.tv/helix/games?name={name}', headers=self.headers)
        datas = game_request.json()['data']
        
        for data in datas:
            if data['name'].lower() == name.lower():
                game_id = data['id']
                break

        return game_id


    def _get_last_week(self):
        ''' Get last week date.
        
        -----------------------------------------------
        
        Returns:
        --------
        
            `date`: datetime.date
            - The date of the last week.        
        '''
        today = datetime.utcnow()
        last_week = today
        for i in range(0,7):
            last_week = last_week - timedelta(days=i)
        
        return last_week.isoformat('T') + 'Z'


    def _get_last_day(self):
        ''' Get last day date.
        
        -----------------------------------------------
        
        Returns:
        --------
        
            `date`: datetime.date
            - The date of the last day.        
        '''
        today = datetime.utcnow()
        last_day = today
        last_day = last_day - timedelta(days=1)
        
        return last_day.isoformat('T') + 'Z'
            
    
    def get_clip_url_of(self, game_name: str, number_of_clips: int = 40):
        ''' Get videos' url of the game specified.
        
        Parameters:
        -----------
        
            `game_name`: str
            -> The game's name category.
            
            `number_of_clips`: int
            -> The number of url to return (Can't be above 100).        
        
        '''
        assert number_of_clips <= 100, "The number of clips can't be above 100."
        
        game_id = self.get_game_id(game_name)
        
        started_at = self._get_last_day()
        ended_at = datetime.utcnow().isoformat('T') + 'Z'
                
        clips_request = requests.get(f'https://api.twitch.tv/helix/clips?game_id={game_id}&started_at={started_at}&ended_at={ended_at}&first={number_of_clips}', headers=self.headers)
        
        if not clips_request.ok:
            raise requests.exceptions.RequestException(clips_request.content)
        
        datas = clips_request.json()['data']

        clips_url = []
        for data in datas:
            url = data['thumbnail_url'].replace('-preview-480x272.jpg', '.mp4')
            clips_url.append(url)

        return clips_url

if __name__ == '__main__':
    CLIENT_ID = 'hb11dao67re5s6srlqilb6ccblk9j8'
    CLIENT_SECRET = 'ms7ozyam1pmtnui8ifk9oy1m9vxwq3'

    twitch_api = TwitchAPI()
    twitch_api.connect_to_api(CLIENT_ID, CLIENT_SECRET)
    clips_url = twitch_api.get_clip_url_of('VALORANT')
    
    for clip in clips_url:
        print(clip)
