from .animation import Animation

class SequenceAnimation:
    active_animation = None
    animation_index = 0
    FINISHED_FLAG = False

    def __init__(self, name, animations, repeat_all=False):
        self.name = name
        self.animations = animations
        self.repeat = repeat_all

    def __repr__(self):
        return f"<SequenceAnimation: {' - '.join(self.animations)}>"

    def validate(self):
        if not isinstance(self.animations, list):
            raise TypeError(
                f"SequenceAnimation must be a list, not {type(self.animations)}"
            )

        if len(self.animations) < 2:
            raise ValueError("SequenceAnimation must contain at least 2 animations")

        for animation in self.animations:
            if not isinstance(animation, Animation):
                raise TypeError(
                    f"SequenceAnimation can only contain Animation objects, not {type(animation)}"
                )

    def get_frame(self):
        self.active_animation = self.animations[self.animation_index]
        is_last_animation = self.animation_index == len(self.animations) - 1

        self.FINISHED_FLAG = False

        frame = self.active_animation.get_frame()

        if self.active_animation.FINISHED_FLAG:
            if is_last_animation:
                self.FINISHED_FLAG = True
                if self.repeat:
                    self.animation_index = 0
                else:
                    pass
            else:
                self.animation_index += 1

        return frame

    def reset(self):
        self.animation_index = 0
        self.FINISHED_FLAG = False
        for animation in self.animations:
            animation.reset()

    def hard_reset(self):
        self.reset()
        for animation in self.animations:
            animation.hard_reset()