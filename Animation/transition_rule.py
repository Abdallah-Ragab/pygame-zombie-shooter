class TransitionRule:
    def __init__(
        self, from_animation, to_animation, intermediate_animation, reversible=False
    ):
        self.from_animation = from_animation
        self.to_animation = to_animation
        self.intermediate_animation = intermediate_animation
        self.reversible = reversible

    def __repr__(self):
        return f"<TransitionRule: {self.from_animation} {'<' if self.reversible else ''}-> {self.intermediate_animation} {'<' if self.reversible else ''}-> {self.to_animation}>"

