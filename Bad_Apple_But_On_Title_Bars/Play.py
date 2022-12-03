import pygame, cv2, os, time
from pygame._sdl2 import *
pygame.init()

width, height = screen_size = (1275, 0)

path = __file__[:-len(os.path.basename(__file__))]
video_path = path + r"Data\Bad_Apple.mp4"
audio_path = path + r"Data\Bad_Apple.mp3"
icon = pygame.image.load(path + r"Data\Icon.png")
#Some os need to change \ to / in the file path

black = "\u2588\u2003"
white = "   \u2003\u200a"
video_width = 48
video_height = 36
distance_between_screens = 28
screen_title_width = 30
#You may need to change something as it depends on your os

try:
    pygame.mixer.music.load(audio_path)

    have_audio = True
except:
    have_audio = False

video = cv2.VideoCapture(video_path)

if not video.isOpened():
    exit("Cannot open video!")

screen_list = []
win_pos_x = (pygame.display.Info().current_w - width) / 2

for screen in range(video_height):
    win_pos = (win_pos_x, (screen * distance_between_screens) + screen_title_width)
    screen = Window("", screen_size, win_pos)
    screen.set_icon(icon)
    screen_list.append(screen)
#You may need to change as it depends on height and width of your screen(it needs about 1275 width and 1011 height)

os.environ["SDL_VIDEO_WINDOW_POS"] = "80, 100"
#Change this to set the preview video position

main_screen = pygame.display.set_mode((video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
pygame.display.set_caption("")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
Fps = video.get(cv2.CAP_PROP_FPS)

if __name__ == "__main__":
    if have_audio:
        pygame.mixer.music.play()

    while True:
        """
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                exit("Windows closed!")
        #You can stop the video normally at anytime if you add this, but you will experience more lag
        #If you disable this there will be less lag, but you will also experience some title rendering errors
        """

        sucess, frame = video.read()
            
        if sucess:
            sub_frame = cv2.resize(frame, (video_width, video_height), interpolation = cv2.INTER_CUBIC)

            for window in range(video_height):
                text = "".join([black if sub_frame[window, width, 0] <= 127 else white for width in range(video_width)])
                screen_list[window].title = text
            
            surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
            main_screen.blit(surface, (0, 0))
            pygame.display.update()
        else:
            if have_audio:
                if not pygame.mixer.music.get_busy():

                    pygame.quit()
                    exit("Video ended!")
            else:
                pygame.quit()
                exit("Video ended!")

        if have_audio:
            video_pos = video.get(cv2.CAP_PROP_POS_MSEC)

            if video_pos > pygame.mixer.music.get_pos():
                try:
                    time.sleep((video_pos - pygame.mixer.music.get_pos()) / 1000)
                except:
                    pass
            else:
                continue
        
        #print("FPS:", round(clock.get_fps())) #For those who need FPS
        
        clock.tick(Fps)
