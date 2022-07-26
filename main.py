class Main():

    ###############
    # Main Script #
    ###############
    
    def __init__(self):

        abspath_file = os.path.abspath(__file__)
        self.abspath, _ = os.path.split(abspath_file)
        self.abspath += '/'
                
        parser = argparse.ArgumentParser()
        parser.add_argument('--game', required=True)

        args = parser.parse_args()
        self.game = args.game
        self.statistics = self.get_statistics()
        self.video_count = self.statistics['video_count']
        
        youtube_api = self.connect_to_youtube()
        twitch_api = self.connect_to_twitch()
        self.all_clips_url = twitch_api.get_clip_url_of(self.game.upper(), self.statistics['i_max'] + 2)

        def execute_program():
            self.current_i += 2

            if self.current_i > self.i_max:
                self.current_i = 0

            self.create_and_export_video(i=self.current_i)
            self.create_and_export_thumbnail()
            
            youtube_api.upload(
                media_path=self.abspath + 'assets/output/video.mp4',
                thumbnail_path=self.abspath + 'assets/output/thumbnail.png',
                game_name=self.game.capitalize(),
                video_count=self.video_count
            )

        self.current_i, self.i_max = self.statistics['current_i'], self.statistics['i_max']

        execute_program()

        self.save_statistics()
                        
        print('[PROG] End')


    #############
    # Functions #
    #############
    
    def connect_to_twitch(self):
        twitch_api = clips.TwitchAPI()
        twitch_api.load_session(self.abspath + 'assets/tools/tokens/twitch_token.json')
        
        return twitch_api
    
    
    def connect_to_youtube(self):
        youtube_api = upload.Uploader()
        youtube_api.login(
            client_secrets_path=self.abspath + 'assets/tools/tokens/youtube_secret.json',
            token_file=self.abspath + 'assets/tools/tokens/youtube_token.json'
        )
        youtube_api.save_session(self.abspath + 'assets/tools/tokens/youtube_token.json')
        
        return youtube_api

    
    def create_and_export_video(self, i):
        video_editor = editor.VideoEditor()
        compiled_video = video_editor.compileClips(self.all_clips_url[i:i+2], transition_path=self.abspath + 'assets/tools/videos/transition.mp4')
        # del self.all_clips_url

        video_editor.exportVideo(self.abspath + 'assets/output/video', compiled_video)
 
 
    def create_and_export_thumbnail(self):
        thumbnail_maker = thumbnail_editor.ThumbnailMaker(self.abspath)
        thumbnail_maker.create_and_export_thumbnail()

    
    def get_statistics(self):
        with open(self.abspath + 'assets/tools/other/statistics.json', 'r') as file:
            json_file = json.load(file)
            # video_count = json_file[self.game.lower()]['video_count']
        return json_file[self.game.lower()]


    def save_statistics(self):
        with open(self.abspath + 'assets/tools/other/statistics.json', 'r') as file:
            json_file = json.load(file)
            
        with open(self.abspath + 'assets/tools/other/statistics.json', 'w') as file:
            json_file[self.game.lower()]['video_count'] = self.video_count + 1
            json_file[self.game.lower()]['current_i'] = self.current_i
            json_file[self.game.lower()]['i_max'] = self.i_max
            json.dump(json_file, file, indent=4)


if __name__ == '__main__':    
    from python_scripts import editor, clips, upload, thumbnail_editor, discord_alert
    import argparse, json, traceback, os
    
    try:
        Main()

    except Exception:
        file_path = os.path.abspath(__file__)
        project_path, _ = os.path.split(file_path)
        project_path += '/'
        error = traceback.format_exc()

        discord_alert.SendAlert(error, project_path)
