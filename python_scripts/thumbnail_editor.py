#!/usr/bin/env python3
# See also: https://legacy.imagemagick.org/Usage/fonts/#soft_shadow
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json


class ThumbnailMaker:
    
    def __init__(self, project_path):
        self.project_path = project_path
        
        self.background_image = Image.open(self.project_path +'assets/tools/images/thumbnail/background.png').convert('RGB')
        
        self.agent_numbers = [
            'astra', 'breach', 'brimstone',
            'chamber', 'cypher', 'fade',
            'jett', 'kayo', 'killjoy',
            'neon', 'omen', 'phoenix',
            'raze', 'reyna', 'sage',
            'skye', 'sova', 'viper',
            'yoru'
        ]
        
        self.text_content = "# "
        self.text_font = ImageFont.truetype(self.project_path + 'assets/tools/fonts/Blockletter.otf', 238)
        self.text_x = 1261
        self.text_y = 820

        self.agent_image = None
        self.agent_x = 0
        self.agent_y = 0
        
        self.border_image = Image.open(self.project_path +'assets/tools/images/thumbnail/border.png')
        self.border_image.convert('RGBA')
        
        self.initialize_statistics()
        self.update_statistics()
        
        
    def load_statistics(self):
        """Load the statistics from the statistics file (statistics.json)

        Returns:
            json_file: A dictionnary with the statistics as values.
        """
        # Load statistics
        with open(self.project_path + 'assets/tools/other/statistics.json', 'r') as file_object:
            json_file = json.load(file_object)
            
        return json_file
    
    
    def initialize_statistics(self):
        
        json_file = self.load_statistics()
        valorant_statistics = json_file['valorant']

        video_count = str(valorant_statistics['video_count'])

        agent_number = valorant_statistics['agent_number']
        agent_name = self.agent_numbers[agent_number]
        
        self.text_content += video_count
        self.agent_image = Image.open(self.project_path + f'assets/tools/images/thumbnail/valorant_agents/{agent_name}.png').convert('RGBA')


    def update_statistics(self):
        # Load statistics
        json_file = self.load_statistics()
        valorant_statistics = json_file['valorant']
        
        video_count = valorant_statistics['video_count']
        agent_number = valorant_statistics['agent_number']
        max_agent_number = valorant_statistics['max_agent_number']
        
        video_count += 1
        agent_number += 1
        
        if agent_number >= max_agent_number:
            agent_number = 0
        
        valorant_statistics['video_count'] = video_count
        valorant_statistics['agent_number'] = agent_number
        
        json_file['valorant'] = valorant_statistics
        
        with open(self.project_path + 'assets/tools/other/statistics.json', 'w') as file_object:
            json.dump(json_file, file_object, indent=4)
            

    def create_thumbnail(self):
        
        # Create piece of canvas to draw text on and blur
        blurred = Image.new('RGBA', self.background_image.size)

        draw = ImageDraw.Draw(blurred)
        draw.text(
            xy=(self.text_x, self.text_y),
            text=self.text_content,
            fill='black',
            font=self.text_font,
            anchor='mm'
        )

        blurred = blurred.filter(ImageFilter.BoxBlur(10))

        # Paste soft text onto background
        for i in range(2):
            self.background_image.paste(blurred,blurred)

        # Draw on sharp text
        draw = ImageDraw.Draw(self.background_image)
        draw.text(
            xy=(self.text_x, self.text_y), 
            text=self.text_content,
            fill='white',
            font=self.text_font,
            anchor='mm'
        )
        
        self.background_image.paste(self.agent_image, (self.agent_x, self.agent_y), self.agent_image)
        self.background_image.paste(self.border_image, mask=self.border_image)
    

    def export_thumbnail(self):
        self.background_image.save(self.project_path + 'assets/output/thumbnail.png')
    
    
    def create_and_export_thumbnail(self):
        self.create_thumbnail()
        self.export_thumbnail()

        
if __name__ == '__main__':
    minia = ThumbnailMaker()
    minia.create_and_export_thumbnail()