from moviepy.editor import CompositeVideoClip, VideoFileClip, VideoClip, vfx
import colorama


class VideoEditor:
    
    def loadClip(self, url: str) -> VideoFileClip:
        print(f"{colorama.Fore.YELLOW}[.]\tCHARGEMENT DU CLIP: \t " + url, end="\r")
        clip = VideoFileClip(url).resize((1280, 720))
        print(f"{colorama.Fore.GREEN}[+]\tCLIP PRÊT: \t \t " + url)
        return clip


    def exportVideo(self, name: str, video: VideoFileClip) -> None:
        print(f"{colorama.Fore.YELLOW}[.]\tEXPORTATION DE LA VIDÉO", end='\r')
        video.write_videofile(name + '.mp4', fps=50, codec='libx264')
        print(f"{colorama.Fore.GREEN}[+]\tEXPORTATION TERMINÉE\t \t \t ")


    def compileClips(self, all_clips_url: list, transition_path: str) -> CompositeVideoClip:
        print(f"{colorama.Fore.YELLOW}[.]\tCOMPILATION DE LA VIDÉO", end="\r")

        self.transition_clip = self.loadClip(transition_path)
        self.transition_clip = vfx.mask_color(self.transition_clip, color=[0,211,0], thr=100, s=5)
        
        transition_starting_point: float = 0.55
        transition_ending_point: float = 0.55
                
        def __add_transition(video_duration, transition_clips):
            transition_clip = self.transition_clip.set_start(video_duration - transition_starting_point, change_end=True)

            transition_clips.append(transition_clip)
            video_duration += transition_ending_point
            
            return video_duration


        def __add_clip(clip: VideoClip, video_duration, final_clips):
            new_clip = clip.set_start(video_duration, change_end=True)
            final_clips.append(new_clip)
            video_duration += clip.duration

            return video_duration


        video_duration: int = 0
        final_clips: list = []
        transition_clips: list = []
        
        isFirstClip: bool = True
        clips = [self.loadClip(all_clips_url[i]) for i in range(len(all_clips_url))]
        
        for i in range(len(all_clips_url)):
            print(f"{colorama.Fore.YELLOW}[/] Ajout du clip #{i}", end='\r')
            if isFirstClip: isFirstClip = False
            else: video_duration = __add_transition(video_duration, transition_clips)

            video_duration = __add_clip(clips[i], video_duration, final_clips)
            print(f"{colorama.Fore.GREEN}[+] Clip #{i} ajouté   ")
 

        final_video = final_clips + transition_clips
        video: VideoClip = CompositeVideoClip(final_video)

        
        # for i in range(0, len(all_clips_url), 2):
        #     for j in range(2):
        #         if i + j < len(all_clips_url):
        #             print(f"{colorama.Fore.YELLOW}[.]\tCompilation #{i+j} en cours", end='\r')

        #             clips = [self.loadClip(all_clips_url[i+k]) for k in range(j+1)]

        #             if isFirstClip: isFirstClip = False
        #             else: video_duration = __add_transition(video_duration, transition_clips)

        #             video_duration = __add_clip(clips[j], video_duration, final_clips)
                    
        #             print(f"{colorama.Fore.GREEN}[.]\tCompilation #{i+j} terminée")
        
        #     final_video = final_clips + transition_clips
        #     video: VideoClip = CompositeVideoClip(final_video)

        #     final_clips = [video]
        #     transition_clips = []

        print(f"{colorama.Fore.GREEN}[+]\tCOMPILATION TERMINÉE\t ")
        return video

    
if __name__ == "__main__":
    """
    A tester pour valider
    """
    # from googleapiclient.http import MediaInMemoryUpload
    # from ..Upload import upload
    
    URL1 = "clip_test.mp4"
    
    editor = VideoEditor()
    clip1 = editor.loadClip(URL1)
    video = editor.compileClips([clip1, clip1])
    editor.exportVideo("test", video)
    
    # with open(video, 'rb') as f:
    #     media = MediaInMemoryUpload(f, chunksize=-1, resumable=False)
            
    # frames = array2string(array(video.iter_frames()))
    # byte_like_object = bytes(frames.encode())
    # media = MediaInMemoryUpload(byte_like_object, chunksize=-1, resumable=False)
    # MediaUpload()
    
    # ytb = upload.Uploader()
    # ytb.login()
    # ytb.upload(media)
    # print("end...")

    # 0, 211, 0
    # 0.40 sec --> Début
    # 0.55 sec --> Fin
    
