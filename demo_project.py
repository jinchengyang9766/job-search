"""Fictional demonstration only. No personal data is read or saved."""

from pydantic import ValidationError

from project import Project


demo_project = Project(
    name="Fictional Demo: Reading Tracker",
    project_type="personal",
    description="A fictional app for tracking books, used only for this demonstration.",
)

print("FICTIONAL DEMO ONLY - no data is saved.")
print(demo_project)
print("Project type value:", demo_project.project_type.value)
print("Organization when omitted:", demo_project.organization)

course_project = Project(
    name="Fictional Demo: Course Reading Tracker",
    project_type="course",
    organization="Fictional Demo University",
    description="A fictional course project used only to demonstrate affiliation.",
)
print("\nFictional project with an organization:")
print(course_project)

print("\nTrying a fictional company project without an organization:")
try:
    Project(
        name="Fictional Demo: Company Project",
        project_type="company",
        description="Fictional input used only to demonstrate a missing affiliation.",
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional course project with a blank organization:")
try:
    Project(
        name="Fictional Demo: Blank Affiliation",
        project_type="course",
        organization="   ",
        description="Fictional input used only to demonstrate a blank affiliation.",
    )
except ValidationError as error:
    print(error)

print("\nTrying fictional invalid input:")
try:
    Project(name="", project_type="personal", description="   ")
except ValidationError as error:
    print(error)

print("\nTrying a fictional unsupported project type:")
try:
    Project(
        name="Fictional Demo: Invalid Type",
        project_type="unknown",
        description="Fictional input used only to demonstrate type validation.",
    )
except ValidationError as error:
    print(error)
