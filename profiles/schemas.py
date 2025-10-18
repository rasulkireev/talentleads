from pydantic import BaseModel, Field, field_validator

from profiles.choices import CapacityChoices, LevelChoices
from talentleads.utils import get_talentleads_logger

logger = get_talentleads_logger(__name__)


class ProfileSchema(BaseModel):
    location: str = Field(..., description="can't be empty")
    city: str = Field(..., description="figure out from location, can't be empty")
    country: str = Field(..., description="figure out from location, can't be empty")
    state: str = Field(
        ...,
        description="if country is USA please guess the state, otherwise empty string. keep the short format, like MA, NY, etc.",
    )
    is_remote: bool = Field(..., description="boolean")
    willing_to_relocate: str = Field(..., description="choose from: Yes, No, Maybe. can't be empty")
    technologies_used: list[str] = Field(..., description="Techonologies used by the profile")
    resume_link: str = Field(..., description="valid url or empty")
    email: str = Field(..., description="valid email or empty")
    personal_website: str = Field(..., description="valid url or empty")
    description: str = Field(
        ...,
        description="Overview of what the profile is capable of doing if hired + any details mentioned in the original comment",
    )
    name: str = Field(..., description="Name of the profile")
    title: str = Field(
        ...,
        description="(Short (6 words max) title based on one of the technologies_used and description, can't be empty",
    )
    level: str = Field(
        ..., description=f"One of the following options: {', '.join([choice[0] for choice in LevelChoices.choices])}"
    )
    years_of_experience: int = Field(..., description="years of experience")
    capacity: str = Field(
        ...,
        description=f"Time Commitment of the profile. One of the following options: {', '.join([choice[0] for choice in CapacityChoices.choices])}",
    )

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, v):
        valid_types = [choice[0] for choice in CapacityChoices.choices]

        if v not in valid_types:
            v_lower = v.lower()
            for valid_type in valid_types:
                if v_lower in valid_type.lower():
                    return valid_type

            logger.warning("[Profile Schema] Capacity is not a valid option", provided_capacity=v)
            if len(v) > 50:
                return v
            else:
                return CapacityChoices.FULL_TIME_EMPLOYEE
        return v

    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        valid_types = [choice[0] for choice in LevelChoices.choices]

        if v not in valid_types:
            v_lower = v.lower()
            for valid_type in valid_types:
                if v_lower in valid_type.lower():
                    return valid_type

            logger.warning("[Profile Schema] Level is not a valid option", provided_level=v)
            if len(v) > 50:
                return v
            else:
                return LevelChoices.MID_LEVEL
        return v
