from pygame import mixer
from os import listdir
from os.path import join as path_join
from SFX import Sound
from Ambiente import DEFAULT_GLOBAL_VOLUME, DEFAULT_MUSIC_VOLUME, PATH

class MusicModule:

    def __init__(self, volume: float = 1) -> None:
        mixer.init()
        
        self._sounds = [
            Sound(
                path_join(PATH, "assets", "music", "sounds", filename),
                global_volume=DEFAULT_GLOBAL_VOLUME
            )
            for filename in filter(
                lambda x: x.endswith(".wav"),
                listdir(path_join(PATH, "assets", "music", "sounds"))
            )
        ]
        
        self._sounds.sort(key=lambda sound: sound.name)
        self._bg_volume = volume

    @property
    def sounds(self) -> list:
        return self._sounds

    @sounds.setter
    def sounds(self, value: list) -> None:
        if not isinstance(value, list):
            raise TypeError("Expected a list of Sound objects.")
        self._sounds = value

    @property
    def bg_volume(self) -> float:
        return self._bg_volume

    @bg_volume.setter
    def bg_volume(self, value: float) -> None:
        if not (0 <= value <= 1):
            raise ValueError("Volume must be between 0 and 1.")
        self._bg_volume = value

    def change_sound_config(self, index: int, duration: int = None, fade: int = None,
                            global_volume: float = None) -> None:
        mixer.music.set_volume(self._bg_volume * global_volume)

        if index in range(len(self._sounds)):
            self._sounds[index].change_config(duration, fade, global_volume)
        else:
            raise IndexError("Index out of range for sounds.")

    def set_global_volume(self, global_volume: float) -> None:
        mixer.music.set_volume(self._bg_volume * global_volume)
        for sound in self._sounds:
            sound.change_config(global_volume=global_volume)

    def __getitem__(self, index: int) -> Sound:
        if index in range(len(self._sounds)):
            return self._sounds[index]
        raise IndexError("Index out of range for sounds.")

    @staticmethod
    def play_music(background: str, volume: float = DEFAULT_MUSIC_VOLUME) -> None:
        mixer.music.load(path_join(PATH, "assets", "music", background))
        mixer.music.set_volume(volume)
        mixer.music.play(-1)

    @staticmethod
    def stop_music() -> None:
        mixer.music.unload()
