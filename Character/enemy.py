from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule
from .character import Character


class Enemy(Character):
        animation = AnimationController(
            animations=[
                Animation('idle', "D:\\game assets\\zombie\\idle", speed=1.5),
                Animation("walk", "D:\\game assets\\zombie\\walk", speed=1.5),
                Animation("idle_to_walk", "D:\\game assets\\zombie\\idle to walk", speed=1.5),
                SequenceAnimation(
                    name="scream_run",
                    animations=[
                        Animation("scream", "D:\\game assets\\zombie\\scream"),
                        Animation("run", "D:\\game assets\\zombie\\run")
                    ]
                ),
                Animation("attack", "D:\\game assets\\zombie\\attack", speed=1.5),
            ],
            default="idle",
            transitions=[
                TransitionRule("idle", "walk", "idle_to_walk", True),
            ]
        )

        def update(self):
            return super().update()