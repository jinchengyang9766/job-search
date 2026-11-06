from enum import Enum

from pydantic import BaseModel, Field, model_validator


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
    description: str = Field(min_length=1, pattern=r"\S")

    @model_validator(mode="after")
    def require_organization(self):
        if self.project_type != ProjectType.PERSONAL:
            if self.organization is None or not self.organization.strip():
                raise ValueError("organization is required for non-personal projects")
        return self
