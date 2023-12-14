import os
import pygame


class TransitionRule():

    def __init__(self, from_animation, to_animation, transition_animation, reversible=False):
        self.from_animation = from_animation
        self.to_animation = to_animation
        self.transition_animation = transition_animation
        self.reversible = reversible

    def __repr__(self):
        return f"<TransitionRule: {self.from_animation} {'<' if self.reversible else ''}-> {self.transition_animation} {'<' if self.reversible else ''}-> {self.to_animation}>"


class AnimationSequence():
    active_animation = None
    animation_index = 0
    FINISHED_FLAG = False

    def __init__(self, name, animations, repeat_all):
        self.name = name
        self.animations = animations
        self.repeat = repeat_all
    def __repr__(self):
        return f"<AnimationSequence: {' - '.join(self.animations)}>"

    def validate(self):
        if not isinstance(self.animations, list):
            raise TypeError(f"AnimationSequence must be a list, not {type(self.animations)}")

        if len(self.animations) < 2:
            raise ValueError("AnimationSequence must contain at least 2 animations")

        for animation in self.animations:
            if not isinstance(animation, Animation):
                raise TypeError(f"AnimationSequence can only contain Animation objects, not {type(animation)}")

    def get_frame(self):
        self.active_animation = self.animations[self.animation_index]
        is_last_animation = self.animation_index == len(self.animations) - 1

        self.FINISHED_FLAG = False

        if self.active_animation.FINISHED_FLAG:
            if is_last_animation:
                self.FINISHED_FLAG = True
                if self.repeat:
                    self.animation_index = 0
                else: pass
            else:
                self.animation_index += 1

        return self.active_animation.get_frame()

    def reset(self):
        self.animation_index = 0
        self.FINISHED_FLAG = False
        for animation in self.animations:
            animation.reset()

    def hard_reset(self):
        self.reset()
        for animation in self.animations:
            animation.hard_reset()

class Animation():
    index = 0
    DEFAULT_SPEED = 1
    iterations = 0
    FINISHED_FLAG = False

    def __init__(self, name, path, speed=DEFAULT_SPEED, inverse=False, end=9999, start=0):
        self.name = name
        self.path = path
        self.speed = float(speed)
        self.inverse = inverse
        self.files = self.discover_files()
        self.end = min(int(end), len(self.files) - 1)
        self.start = int(start)
        self.frame_count = self.end - self.start + 1


    def __repr__(self):
        return f"<Animation: {self.name}>"

    def discover_files(self):
        files = os.listdir(self.path)
        files.sort()
        if self.inverse:
            files.reverse()
        return files

    def get_frame(self):
        self.index += self.speed
        self.index = int(self.index)
        index = self.index % self.frame_count

        if index >= self.end:
            self.iterations += 1
            self.FINISHED_FLAG = True
        else:
            self.FINISHED_FLAG = False

        return Frame(os.path.join(self.path, self.files[index]))

    def reset(self):
        self.index = self.start
        self.FINISHED_FLAG = False

    def hard_reset(self):
        self.reset()
        self.iterations = 0


class AnimationManager():

    def __init__(self, animations, default, transitions=[]):
        self.animations = animations
        self.transitions = transitions
        self.default = default
        self.active_animation = self.animations[self.default]

    def update(self):
        return self.active_animation.get_frame()

    def set_animation(self, name, force=False):
        if name not in self.animations:
            raise KeyError(f"Animation {name} not found")

        if self.active_animation.name == name and not force:
            return

        self.active_animation = self.animations[name]

    def add_animation(self, animation):
        self.animations[animation.name] = animation

    def get_animation(self, name):
        return self.animations.get(name, None)

    def get_transition(self, from_animation, to_animation):
        for transition in self.transitions:
            if transition.from_animation == from_animation and transition.to_animation == to_animation:
                return transition
            if transition.reversible and transition.from_animation == to_animation and transition.to_animation == from_animation:
                return transition
        return None

    def get_transition_animation(self, from_animation, to_animation, transition):
        transition_animation_name = f"transition_{from_animation}_{to_animation}"
        transition_animation = self.get_animation(transition_animation_name)
        if transition_animation:
            return transition_animation
        transition_animation = AnimationSequence(
            name=transition_animation_name,
            animations=[
                self.animations[transition.transition_animation],
                self.animations[to_animation],
            ],
            repeat_all=False,)
        return transition_animation

    def switch_animation(self, name, ignore_transition=False, force=False):
        if not name in self.animations:
            raise KeyError(f"Animation {name} not found")

        from_animation = self.active_animation.active_animation.name if isinstance(self.active_animation, AnimationSequence) else self.active_animation.name
        to_animation = name

        print("from: ", from_animation, "to: ", to_animation)

        if not ignore_transition:
            transition = self.get_transition(from_animation, to_animation)
            print("transition: ", transition)
            if transition:
                animation = self.get_transition_animation(from_animation, to_animation, transition)
                self.add_animation(animation)
                animation_name = animation.name
            else:
                animation_name = to_animation
        else:
            animation_name = to_animation

        print("animation_name: ", animation_name)

        self.set_animation(animation_name, force=force)
        self.reset_animation()

    def reset_animation(self):
        self.active_animation.reset()

    def hard_reset(self):
        self.active_animation.hard_reset()

    def __repr__(self):
        return f"<AnimationManager: {self.active_animation}>"

    def __str__(self):
        return f"<AnimationManager: {self.active_animation}>"

    def __getitem__(self, key):
        return self.animations[key]

    def __setitem__(self, key, value):
        self.animations[key] = value

    def __delitem__(self, key):
        del self.animations[key]



    current_animation = Animation("idle", "D:\\game assets\\zombie\\idle")




# class Animation:
#     DEFAULT_SPEED = 1

#     def __init__(self, name, dir, speed = DEFAULT_SPEED, end=None, start=None, inverse=False, loop=False):
#         self.name = name
#         self.dir = dir
#         self.speed = float(speed)
#         self.inverse = inverse
#         self.loop = loop

#         self.files = os.listdir(self.dir)
#         self.files.sort()
#         if self.inverse:
#             self.files.reverse()

#         self.end = int(end) if end else len(self.files) - 1
#         self.start = int(start) if start else 0
#         self.index = self.start

#     def generator(self):
#         while not self.END_FLAG:
#             self.index += self.speed
#             self.index = int(self.index)
#             print("start: ", self.start, "end: ", self.end, "index: ", self.index, "END: ", self.END_FLAG)
#             yield Frame(dir=self.dir, file=self.files[self.index], name=self.name)


#     @property
#     def END_FLAG(self):
#         return self.index >= self.end

#     @property
#     def PRE_END_FLAG(self):
#         return self.index >= self.end - 1

#     def reset(self):
#         self.index = self.start

#     def skip(self):
#         pass

class Frame:
    def __init__(self, path=None, dir=None, file=None, name=None):
        self._name = name
        if path:
            self.dir = os.path.dirname(path)
            self.file = os.path.basename(path)
        else:
            self.dir = dir
            self.file = file

        if not self.dir:
            raise ValueError("No directory specified")
        if not self.file:
            raise ValueError("No file specified")

        self.file_name = self.file.split(".")[0]


    @property
    def z_index(self):
        return str(self.index).zfill(4)

    @property
    def name(self):
        if self._name:
            return self._name

        if self.dir[-1] == "/" or self.dir[-1] == "\\":
            self.dir = self.dir[:-1]
        if "/" in self.dir:
            return self.dir.split("/")[-1]
        else:
            return self.dir.split("\\")[-1]

    @property
    def index(self):
        return int(self.file_name)

    @property
    def path(self):
        return os.path.join(self.dir, self.file)

    @property
    def image(self):
        return pygame.image.load(self.path)


    def __repr__(self):
        return f"{self.name}.{self.z_index}"
