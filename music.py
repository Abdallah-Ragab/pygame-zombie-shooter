import pygame


class Player():
    queue = []
    fadein_time = 500
    fadeout_time = 500
    max_background_channels = 2

    def __init__(self, background_music: dict, sound_effects: dict):
        self.background_music = background_music
        self.sound_effects = sound_effects

        pygame.mixer.set_reserved(self.max_background_channels)
        self.background_channels = [pygame.mixer.Channel(x) for x in range(self.max_background_channels)]

        for channel in self.background_channels:
            channel.fadeout(self.fadeout_time)


    def add_background_music(self, background_music: dict):
        self.background_music.update(background_music)

    def add_sound_effects(self, sound_effects: dict):
        self.sound_effects.update(sound_effects)


    def play_background_music(self, music_name: str | list, loop: bool = True, volume: float = 1.0):
        parallel_music = [music_name] if isinstance(music_name, str) else music_name
        parallel_music = parallel_music[self.max_background_channels:]
        for music in parallel_music:

            self._play_background_music(music, loop, volume)

    def _play_background_music(self, music_name: str, loop: bool, volume: float):

        if music_name not in self.background_music:
            raise ValueError(f"{music_name} not found in background music")

        self.queue.append((self.background_music[music_name], loop))

        if not self.background_channels[0].get_busy():
            self._play_next()

    def enqueue_background_music(self, music_name: str | list, loop: bool = True, volume: float = 1.0):
        parallel_music = [music_name] if isinstance(music_name, str) else music_name
        parallel_music = parallel_music[self.max_background_channels:]
        for music in parallel_music:
            self._enqueue_background_music(music, loop, volume)

    def _enqueue_background_music(self, music_name: str, loop: bool, volume: float):
        if music_name not in self.background_music:
            raise ValueError(f"{music_name} not found in background music")

        self.queue.append((self.background_music[music_name], loop))

    def _play_next(self):
        music, loop = self.queue.pop(0)
        self.background_channels[0].play(music, loop=loop, fade_ms=self.fadein_time)

    def background_music_is_playing(self):
        return any([channel.get_busy() for channel in self.background_channels])

    def pause_background_music(self):
        for channel in self.background_channels:
            channel.pause()

    def unpause_background_music(self):
        for channel in self.background_channels:
            channel.unpause()

    def update(self):
        if not self.background_music_is_playing() and self.queue:
            self._play_next()

    def play_sound_effect(self, sound_effect_name: str, volume: float = 1.0):
        if sound_effect_name not in self.sound_effects:
            raise ValueError(f"{sound_effect_name} not found in sound effects")

        pygame.mixer.find_channel().play(self.sound_effects[sound_effect_name])

    def stop_all_sounds(self):
        pygame.mixer.stop()

    def stop_background_music(self):
        for channel in self.background_channels:
            channel.stop()
