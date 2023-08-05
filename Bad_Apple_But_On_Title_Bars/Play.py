import pygame, cv2, time, os, sys
from pygame._sdl2 import Window
pygame.display.init()

path = os.path.dirname(sys.argv[0])
video_path = os.path.join(path, "Data", "Bad_Apple.mp4")
audio_path = os.path.join(path, "Data", "Bad_Apple.mp3")

black = "\u2588\u2003"
white = "   \u2003\u200a"
video_width = 48
video_height = 36

icon = pygame.Surface((32, 32), pygame.SRCALPHA)
clock = pygame.time.Clock()
width, height = screen_size = (1275, 0)
default_fps = 60

distance_between_screens = 28
#You can change this value as you like

screen_position = (100, 100)
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % screen_position
#Change this to set the preview video position

if __name__ == "__main__":
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise RuntimeError("Failed to open the video.")

    video_fps = video.get(cv2.CAP_PROP_FPS)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)

        have_audio = True
    except pygame.error:
        have_audio = False

    screens = []
    win_pos_x = (pygame.display.Info().current_w - width) // 2
    for screen in range(video_height):
        screen = Window("", screen_size, (win_pos_x, screen * distance_between_screens))
        screen.set_icon(icon)
        screens.append(screen)

    main_screen = pygame.display.set_mode((int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    pygame.display.set_caption("")
    pygame.display.set_icon(icon)


    if have_audio:
        pygame.mixer.music.play()
    else:
        start = time.monotonic_ns()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.display.quit()
                if have_audio:
                    pygame.mixer.quit()
                exit()

        current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
        number_of_frames_difference = (pygame.mixer.music.get_pos() / 1000 if have_audio else (time.monotonic_ns() - start) / 1000000000) * video_fps - current_frame
        if number_of_frames_difference >= 0:
            if number_of_frames_difference >= 2:
                video.set(cv2.CAP_PROP_POS_FRAMES, int(current_frame + number_of_frames_difference))

            success, frame = video.read()
            if success:
                title_frame = cv2.resize(frame, (video_width, video_height), interpolation = cv2.INTER_CUBIC)
                for window in range(video_height):
                    screens[window].title = "".join([black if title_frame[window, width, 0] <= 127 else white for width in range(video_width)])

                main_screen.blit(pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR").convert(), (0, 0))
                pygame.display.update()
            else:
                pygame.display.quit()
                if have_audio:
                    pygame.mixer.quit()
                exit()

        clock.tick(default_fps)

        #print(f"FPS: {round(clock.get_fps())} / {default_fps}")
        #For those who need to get the FPS
