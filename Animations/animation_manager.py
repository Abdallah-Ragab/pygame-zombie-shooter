
class AnimationManager:
    def __init__(self, animations: dict, default_animation=None):
        self.animations = animations
        self.default_animation = default_animation
        self.play_animation(default_animation)

    def play_animation(self, name):
        self.active_animation = self.animations[name]

    def frame(self):
        if self.active_animation.END_FLAG:
            self.active_animation = self.animations[self.default_animation]
            self.active_animation.reset()
        yield from self.active_animation.generator()


