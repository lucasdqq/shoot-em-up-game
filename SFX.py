from pygame import mixer
from os.path import join as path_join

class Sound:
    def __init__(self, filename: str, duration: int = 0, fade: int = 0, volume: int = 1,
                 global_volume: float = 1) -> None:

        self._name = filename
        self._sound = mixer.Sound(path_join("assets", "music", filename))
        self._duration = duration
        self._fade = fade
        self._volume = volume
        self._global_volume = global_volume

        self._sound.set_volume(self._volume * self._global_volume)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self._sound = mixer.Sound(path_join("assets", "music", value))

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int):
        self._duration = value

    @property
    def fade(self) -> int:
        return self._fade

    @fade.setter
    def fade(self, value: int):
        self._fade = value

    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value: int):
        self._volume = value
        self._sound.set_volume(self._volume * self._global_volume)

    @property
    def global_volume(self) -> float:
        return self._global_volume

    @global_volume.setter
    def global_volume(self, value: float):
        self._global_volume = value
        self._sound.set_volume(self._volume * self._global_volume)

    def __call__(self, volume) -> None:
        self._sound.set_volume(volume * self._global_volume)
        self._sound.play(0, self._duration, self._fade)

    def change_config(self, duration: int = None, fade_ms: int = None, global_volume: float = None) -> None:
        if duration is not None:
            self._duration = duration
        if fade_ms is not None:
            self._fade = fade_ms
        if global_volume is not None:
            self._global_volume = global_volume
            self._sound.set_volume(self._volume * self._global_volume)
