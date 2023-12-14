
from copy import deepcopy
from .animation import Animation
from .sequence_animation import SequenceAnimation

class AnimationManager:
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
            if (
                transition.from_animation == from_animation
                and transition.to_animation == to_animation
            ):
                return transition, False
            if (
                transition.reversible
                and transition.from_animation == to_animation
                and transition.to_animation == from_animation
            ):
                return transition, True
        return None, False

    def get_transition_animation(
        self, from_animation, to_animation, transition, reverse=False
    ):
        transition_animation_name = f"transition_{from_animation}_{to_animation}"
        transition_animation = self.get_animation(transition_animation_name)
        if transition_animation:
            return transition_animation
        if reverse:
            print(f"Reversing animation {transition.intermediate_animation}")
            intermediate_animation = deepcopy(
                self.animations[transition.intermediate_animation]
            )
            print(dir(intermediate_animation))
            intermediate_animation.reverse_animation()
        else:
            intermediate_animation = self.animations[transition.intermediate_animation]
        transition_animation = SequenceAnimation(
            name=transition_animation_name,
            animations=[
                intermediate_animation,
                self.animations[to_animation],
            ],
            repeat_all=False,
        )
        return transition_animation

    def switch_animation(self, name, ignore_transition=False, force=False):
        if not name in self.animations:
            raise KeyError(f"Animation {name} not found")

        from_animation = (
            self.active_animation.active_animation.name
            if isinstance(self.active_animation, SequenceAnimation)
            else self.active_animation.name
        )
        to_animation = name

        print("from: ", from_animation, "to: ", to_animation)

        if not ignore_transition:
            transition, reverse = self.get_transition(from_animation, to_animation)
            print("transition: ", transition)
            if transition:
                animation = self.get_transition_animation(
                    from_animation, to_animation, transition, reverse=reverse
                )
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
