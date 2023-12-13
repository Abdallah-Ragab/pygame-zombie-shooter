
class AnimationManager:
    def __init__(self, animations: dict, default_animation=None):
        self.animations = animations
        self.default_animation = default_animation
        self.active_animation = None
        self.play_animation(default_animation)

    def play_animation(self, name):
        print("playing animation: ", name)
        self.reset_animation()
        self.active_animation = self.animations[name]

    def frame(self):
        if self.active_animation.END_FLAG:
            self.reset_animation()
            self.active_animation = self.animations[self.default_animation]
            self.reset_animation()
        yield from self.active_animation.generator()

    def reset_animation(self):
        if self.active_animation:
            self.active_animation.reset()


