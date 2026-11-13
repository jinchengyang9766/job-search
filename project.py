from enum import Enum
from re import fullmatch
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


NonBlankText = Annotated[str, Field(min_length=1, pattern=r"\S")]


class ProjectType(str, Enum):
    PERSONAL = "personal"
    COURSE = "course"
    COMPANY = "company"
    COMPETITION = "competition"
    OTHER = "other"


class Project(BaseModel):
    name: str = Field(min_length=1, pattern=r"\S")
    project_type: ProjectType
    organization: str | None = None
    start_date: str
    end_date: str | None = None
    is_ongoing: bool = Field(strict=True)
    description: str = Field(min_length=1, pattern=r"\S")
    contributions: list[NonBlankText] = Field(min_length=1)
    tech_stack: list[NonBlankText] = Field(min_length=1)

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_year_month(cls, value):
        if value is None:
            return value
        if fullmatch(r"[0-9]{4}-[0-9]{2}", value) is None:
            raise ValueError("date must use YYYY-MM format")
        year, month = value.split("-")
        if not 1 <= int(year) <= 9999:
            raise ValueError("year must be between 0001 and 9999")
        if not 1 <= int(month) <= 12:
            raise ValueError("month must be between 01 and 12")
        return value

    @model_validator(mode="after")
    def require_organization(self):
        if self.project_type != ProjectType.PERSONAL:
            if self.organization is None or not self.organization.strip():
                raise ValueError("organization is required for non-personal projects")
        return self

    @model_validator(mode="after")
    def validate_project_dates(self):
        if self.is_ongoing:
            if self.end_date is not None:
                raise ValueError("end_date must be empty when is_ongoing is True")
        else:
            if self.end_date is None:
                raise ValueError("end_date is required when is_ongoing is False")
            if self.end_date < self.start_date:
                raise ValueError("end_date must not be earlier than start_date")
        return self
