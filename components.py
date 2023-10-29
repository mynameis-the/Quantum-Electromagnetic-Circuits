from dataclasses import dataclass

# step 1: caveman brain defines circuit components


@dataclass
class Component:
    ...


@dataclass
class Capacitor(Component):
    capacitance: float

    def __post_init__(self):
        self.value = self.capacitance


@dataclass
class Inductor(Capacitor):  # inductor has capacitance (for some reason)
    inductance: float

    def __post_init__(self):
        self.value = self.inductance
