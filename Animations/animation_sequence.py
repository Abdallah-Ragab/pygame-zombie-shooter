from copy import deepcopy as copy


class AnimationSequence:
    queue = []

    def __init__(self, name, animations=[]):
        self.name = name
        self.animations = animations
        self.queue = copy(self.animations)

    def append(self, animation):
        self.queue.append(animation)

    def skip(self, count=1):
        old = self.queue.copy()
        for _ in range(count):
            self.end_animation()
        print("skipped: ", [a.name for a in old], " -> ", [a.name for a in self.queue])

    @property
    def END_FLAG(self):
        return self.PRE_END_FLAG and self.queue[0].END_FLAG

    @property
    def PRE_END_FLAG(self):
        return len(self.queue) == 1

    @property
    def active_animation(self):
        if self.queue:
            return self.queue[0]

    def end_animation(self):
        self.active_animation.reset()
        self.queue.pop(0)
        self.active_animation.reset()
    def generator(self):
        if self.active_animation.END_FLAG:
            self.active_animation.reset()
            if not self.active_animation.loop:
                self.end_animation()
        yield from self.active_animation.generator()

    def reset(self):
        self.queue = copy(self.animations)
