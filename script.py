import moviepy.editor as mpe
import moviepy.video as mpv
from random import randint
from math import floor

colours = ['white', 'brown','grey', 'black', 
'red', 'maroon', 'lime', 'green', 
'yellow', 'gold', 'aqua', 'blue', 
'sky-blue', 'orange','pastel-pink','pink',
'magenta','purple','lavender'
]

class Generator:
    def __init__(self, filename, audioname, colournames):
        self.total_duration = 0
        self.clip_list = []
        self.clip = mpe.VideoFileClip(filename)
        self.audio = mpe.AudioFileClip(audioname)
        self.colournames = colournames
        self.overlay = mpe.VideoFileClip('assets/overlay.mov').subclip().resize(self.clip.size).set_opacity(0.40)

    def audi_test(self):
        f = self.clip.set_audio(self.audio)
        f.write_videofile('out.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    def create(self, desired_length, desired_trim):
        while self.total_duration < desired_length:
            self.add_clip()
        final = mpe.concatenate_videoclips(self.clip_list)

        self.audio = self.audio.set_duration(self.total_duration)
        final = final.set_audio(self.audio)
        final.write_videofile('output_file.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    def add_clip(self,trim):
        r = randint(0, floor(self.clip.duration-trim))
        #Pick random clip ^, Put colours in array, pick random colour below..
        colour_nums = [colours[a] for a in self.colournames]
        randcolour = colour_nums[randint(0,len(colour_nums))]
        subclip = self.clip.subclip(r, r+(r%trim))
        merged = mpe.CompositeVideoClip([subclip, self.overlay.subclip(2, 2+r%trim)])
        if r%2==0: #adds a fade_in transition if r is even.
            merged = mpv.fx.all.fadein(merged, 3)
        image = mpe.ImageClip('assets/'+randcolour+'.png').resize(self.clip.size).set_opacity(0.35).set_duration(trim)
        merged = mpe.CompositeVideoClip([merged, image])
        self.clip_list.append(merged)
        self.total_duration += r%trim

    
movie_name = input("Filename of Movie?")
music = input("Filename of music?")
desired_duration = int(input("Desired length of video in seconds? (full video)"))
desired_trim = int(input("Desired length of video segments in seconds? (trimmed portions)"))

desired_colours = []
choice = 1337
for n,a in enumerate(colours):
    print((n+1),a , end='  \t ')
    if((n+1)%5==0):
        print('')
#Just incase, for formatting
if((n+1)%5!=0):
        print('')   
while(choice!=0):
    print('Selected colours: ', desired_colours)
    choice = input('Pick a colour using it\'s number representive, enter 0 when finished, put x in front of number to delete it: ')
    #Check if deleting, otherwise we are just adding..
    if(choice[0].upper()=='X'):
        choice = int(choice[1:len(choice)])
        if(choice>0 and choice < len(colours)):
            try:
                desired_colours.remove(int(choice))
            except:
                print('Can\'t delete a value that doesn\'t exist in the list')
    else:
        choice = int(choice)
        if(choice>0 and choice < len(colours) and choice not in desired_colours):
            desired_colours.append(int(choice))
            

g = Generator(movie_name, music, desired_colours)
g.create(desired_duration,desired_trim)
