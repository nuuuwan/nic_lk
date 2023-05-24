from dataclasses import dataclass


@dataclass
class Gender:
    gender: str


Gender.MALE = Gender("MALE")
Gender.FEMALE = Gender("FEMALE")
