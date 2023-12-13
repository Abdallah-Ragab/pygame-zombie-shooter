class AnimationSequence:
    queue = []

    def __init__(self, name, animations=[]):
        self.name = name
        self.animations = animations
        self.queue = animations.copy()

    def append(self, animation):
        self.queue.append(animation)

    def skip(self, to=None):
        old = self.queue.copy()
        if to:
            self.queue = self.queue[:to]
        else:
            self.queue.pop(0)
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

    def generator(self):
        if self.active_animation.END_FLAG:
            if self.active_animation.loop:
                self.active_animation.reset()
            else:
                self.queue.pop(0)
        yield from self.active_animation.generator()
        # if self.active_animation.PRE_END_FLAG and self.PRE_END_FLAG:
        #     pass

    def reset(self):
        self.queue = self.animations.copy()

