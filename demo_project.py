"""Fictional demonstration only. No personal data is read or saved."""

from pydantic import ValidationError

from project import Project


demo_project = Project(
    name="Fictional Demo: Reading Tracker",
    project_type="personal",
    start_date="2026-01",
    is_ongoing=True,
    description="A fictional app for tracking books, used only for this demonstration.",
    contributions=["Built a fictional book-entry form.", "Added a fictional reading list."],
    tech_stack=["Python", "Pydantic"],
)

print("FICTIONAL DEMO ONLY - no data is saved.")
print(demo_project)
print("Project type value:", demo_project.project_type.value)
print("Organization when omitted:", demo_project.organization)

course_project = Project(
    name="Fictional Demo: Course Reading Tracker",
    project_type="course",
    organization="Fictional Demo University",
    start_date="2025-09",
    end_date="2025-12",
    is_ongoing=False,
    description="A fictional course project used only to demonstrate affiliation.",
    contributions=["Built a fictional reading tracker for the course example."],
    tech_stack=["Python"],
)
print("\nFictional project with an organization:")
print(course_project)

print("\nTrying a fictional company project without an organization:")
try:
    Project(
        name="Fictional Demo: Company Project",
        project_type="company",
        start_date="2026-01",
        is_ongoing=True,
        description="Fictional input used only to demonstrate a missing affiliation.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional course project with a blank organization:")
try:
    Project(
        name="Fictional Demo: Blank Affiliation",
        project_type="course",
        organization="   ",
        start_date="2026-01",
        is_ongoing=True,
        description="Fictional input used only to demonstrate a blank affiliation.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying fictional invalid input:")
try:
    Project(
        name="",
        project_type="personal",
        start_date="2026-01",
        is_ongoing=True,
        description="   ",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional unsupported project type:")
try:
    Project(
        name="Fictional Demo: Invalid Type",
        project_type="unknown",
        start_date="2026-01",
        is_ongoing=True,
        description="Fictional input used only to demonstrate type validation.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional project with an empty contributions list:")
try:
    Project(
        name="Fictional Demo: Empty Contributions",
        project_type="personal",
        start_date="2026-01",
        is_ongoing=True,
        description="Fictional input used only to demonstrate an empty list.",
        contributions=[],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional project with a blank technology item:")
try:
    Project(
        name="Fictional Demo: Blank Technology",
        project_type="personal",
        start_date="2026-01",
        is_ongoing=True,
        description="Fictional input used only to demonstrate an invalid list item.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python", "   "],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional project with an invalid date format:")
try:
    Project(
        name="Fictional Demo: Date Format",
        project_type="personal",
        start_date="2026-1",
        is_ongoing=True,
        description="Fictional input used only to demonstrate month formatting.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional project with a nonexistent month:")
try:
    Project(
        name="Fictional Demo: Invalid Month",
        project_type="personal",
        start_date="2026-13",
        is_ongoing=True,
        description="Fictional input used only to demonstrate month validity.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional project that ends before it starts:")
try:
    Project(
        name="Fictional Demo: Reversed Dates",
        project_type="personal",
        start_date="2026-06",
        end_date="2026-03",
        is_ongoing=False,
        description="Fictional input used only to demonstrate date ordering.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional ongoing project with an end date:")
try:
    Project(
        name="Fictional Demo: Ongoing With End Date",
        project_type="personal",
        start_date="2026-01",
        end_date="2026-03",
        is_ongoing=True,
        description="Fictional input used only to demonstrate ongoing-state consistency.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)

print("\nTrying a fictional ended project without an end date:")
try:
    Project(
        name="Fictional Demo: Ended Without End Date",
        project_type="personal",
        start_date="2026-01",
        is_ongoing=False,
        description="Fictional input used only to demonstrate a required end date.",
        contributions=["Implemented a fictional feature."],
        tech_stack=["Python"],
    )
except ValidationError as error:
    print(error)
