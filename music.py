import random
import pygame


class Player:
    music_queue = []
    background_effects_loop = []
    fadein_time = 500
    fadeout_time = 500
    background_effects_channel_count = 2
    background_music_channel_count = 2
    background_effects_loop_running_channels = background_effects_channel_count
    background_music_queue_running_channels = background_music_channel_count

    def __init__(
        self,
        background_music: dict = {},
        sound_effects: dict = {},
        background_effects: dict = {},
    ):
        # pygame.mixer.init()

        self.background_music = background_music
        self.sound_effects = sound_effects
        self.background_effects = background_effects

        pygame.mixer.set_reserved(
            self.background_music_channel_count + self.background_effects_channel_count
        )

        self.background_music_channels = [
            pygame.mixer.Channel(x) for x in range(self.background_music_channel_count)
        ]
        self.background_effects_channels = [
            pygame.mixer.Channel(x)
            for x in range(self.background_effects_channel_count)
        ]

        for channel in (
            self.background_music_channels + self.background_effects_channels
        ):
            channel.fadeout(self.fadeout_time)

    def add_background_music(self, background_music: dict):
        self.background_music.update(background_music)

    def add_sound_effects(self, sound_effects: dict):
        self.sound_effects.update(sound_effects)

    def add_background_effects(self, background_effects: dict):
        self.background_effects.update(background_effects)

    def play_background_music(
        self, music_name: str | list, loop: bool = True, volume: float = 1.0
    ):
        parallel_music = [music_name] if isinstance(music_name, str) else music_name
        for music in parallel_music:
            self._play_background_music(music, loop, volume)

    def enqueue_background_music(
        self, music_name: str | list, loop: bool = False, volume: float = 1.0
    ):
        parallel_music = [music_name] if isinstance(music_name, str) else music_name
        parallel_music = parallel_music[self.background_music_channel_count :]
        for music in parallel_music:
            self._enqueue_background_music(music, loop, volume)

    def loop_background_effect(self, effects: list | str, channel_count=None):
        if channel_count is not None:
            self.background_effects_loop_running_channels = channel_count
        else:
            self.background_effects_loop_running_channels = self.background_effects_channel_count

        self.clear_background_effects_loop()
        effects = [effects] if isinstance(effects, str) else effects
        for effect_name in effects:
            if effect_name not in self.background_effects:
                raise ValueError(f"{effect_name} not found in background effects")
            self.background_effects_loop.append(effect_name)

    def clear_background_effects_loop(self):
        self.background_effects_loop = []

    def play_sound_effect(self, sound_effect_name: str, volume: float = 1.0):
        if sound_effect_name not in self.sound_effects:
            raise ValueError(f"{sound_effect_name} not found in sound effects")
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound_effects[sound_effect_name])

    def stop_all(self):
        pygame.mixer.stop()
    def pause_all(self):
        pygame.mixer.pause()
    def unpause_all(self):
        pygame.mixer.unpause()

    def flush(self):
        # self.stop_all()
        # pygame.mixer.set_reserved(0)
        pygame.mixer.quit()


    def stop_background_music(self):
        for channel in self.background_music_channels:
            channel.stop()

    def play_background_effect(self, background_effect_name: str, volume: float = 1.0):
        if background_effect_name not in self.background_effects:
            raise ValueError(
                f"{background_effect_name} not found in background effects"
            )

        pygame.mixer.find_channel().play(
            self.background_effects[background_effect_name]
        )

    def pause_background_music(self):
        for channel in self.background_music_channels:
            channel.pause()

    def unpause_background_music(self):
        for channel in self.background_music_channels:
            channel.unpause()

    def _play_background_music(self, music_name: str, loop: bool, volume: float):
        if music_name not in self.background_music:
            raise ValueError(f"{music_name} not found in background music")
        # print("playing background music")
        for channel in self.background_music_channels:
            if not channel.get_busy():
                channel.play(
                    self.background_music[music_name],
                    loops=0,
                    fade_ms=self.fadein_time,
                )
                # print("Found free channel")
                return
        # print("No free channel found")
        self.background_music_channels[0].play(
            self.background_music[music_name], loops=-1 if loop else 0, fade_ms=self.fadein_time
        )

    def _enqueue_background_music(self, music_name: str, loop: bool, volume: float):
        if music_name not in self.background_music:
            raise ValueError(f"{music_name} not found in background music")

        self.music_queue.append((self.background_music[music_name], loop))

    def background_music_is_playing(self):
        return any([channel.get_busy() for channel in self.background_music_channels])

    def update(self):
        self.run_music_queue()
        self.run_effects_loop()

    def run_effects_loop(self, ):
        available_channels = [
            channel
            for channel in self.background_music_channels
            if not channel.get_busy()
        ][:self.background_effects_loop_running_channels]
        for channel in available_channels:
            if self.background_effects_loop:
                effect = random.choice(self.background_effects_loop)
                channel.play(self.background_effects[effect])

    def run_music_queue(self):
        available_channels = [
            channel
            for channel in self.background_music_channels
            if not channel.get_busy()
        ][:self.background_music_queue_running_channels]
        for channel in available_channels:
            if self.music_queue:
                music = self.background_music[self.music_queue.pop(0)]
                channel.play(music, fade_ms=self.fadein_time)
