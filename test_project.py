"""Acceptance checks using fictional records only; no files or database are read or saved."""

import unittest

from pydantic import ValidationError

from project import Project


def fictional_project_data():
    return {
        "name": "  Fictional Demo: Reading Tracker  ",
        "project_type": "personal",
        "start_date": "2026-01",
        "is_ongoing": True,
        "description": "A fictional project used only for acceptance checks.",
        "contributions": ["  Built a fictional form.  ", "Added a fictional list."],
        "tech_stack": ["Python", "  Pydantic  "],
    }


class ProjectAcceptanceTests(unittest.TestCase):
    def assert_invalid(self, data, location):
        with self.assertRaises(ValidationError) as caught:
            Project(**data)
        locations = [detail["loc"] for detail in caught.exception.errors()]
        self.assertIn(location, locations)

    def test_valid_record_preserves_facts(self):
        data = fictional_project_data()
        record = Project(**data)
        self.assertEqual(record.project_type.value, data["project_type"])
        for field in data:
            if field != "project_type":
                self.assertEqual(getattr(record, field), data[field])
        self.assertIsNone(record.organization)
        self.assertIsNone(record.end_date)

    def test_required_fields_cannot_be_omitted(self):
        for field in fictional_project_data():
            with self.subTest(field=field):
                data = fictional_project_data()
                del data[field]
                self.assert_invalid(data, (field,))

    def test_required_text_cannot_be_blank(self):
        for field in ("name", "description"):
            for value in ("", " \t\n"):
                with self.subTest(field=field, value=value):
                    data = fictional_project_data()
                    data[field] = value
                    self.assert_invalid(data, (field,))

    def test_categories_are_limited_to_the_agreed_values(self):
        for category in ("personal", "course", "company", "competition", "other"):
            with self.subTest(category=category):
                data = fictional_project_data()
                data.update(project_type=category, organization="Fictional Institution")
                self.assertEqual(Project(**data).project_type.value, category)
        data = fictional_project_data()
        data["project_type"] = "unknown"
        self.assert_invalid(data, ("project_type",))

    def test_organization_depends_on_project_type(self):
        for value in (None, "", " \t\n"):
            with self.subTest(category="personal", organization=value):
                data = fictional_project_data()
                data["organization"] = value
                self.assertEqual(Project(**data).organization, value)
        for category in ("course", "company", "competition", "other"):
            for value in (None, "", " \t\n"):
                with self.subTest(category=category, organization=value):
                    data = fictional_project_data()
                    data.update(project_type=category, organization=value)
                    self.assert_invalid(data, ())
        data = fictional_project_data()
        data["organization"] = 123
        self.assert_invalid(data, ("organization",))

    def test_lists_and_each_item_must_be_valid(self):
        cases = (
            ([], None),
            ([""], 0),
            (["Fictional text", " \t\n"], 1),
            (["Fictional text", 123], 1),
            ("Fictional text", None),
            (None, None),
        )
        for field in ("contributions", "tech_stack"):
            for value, bad_index in cases:
                with self.subTest(field=field, value=value):
                    data = fictional_project_data()
                    data[field] = value
                    location = (field,) if bad_index is None else (field, bad_index)
                    self.assert_invalid(data, location)

    def test_months_preserve_precision_and_reject_invalid_values(self):
        for month in ("0001-01", "2024-02", "9999-12"):
            with self.subTest(valid_month=month):
                data = fictional_project_data()
                data.update(start_date=month, end_date=month, is_ongoing=False)
                record = Project(**data)
                self.assertEqual(record.start_date, month)
                self.assertEqual(record.end_date, month)
        invalid_months = (
            "", "2026-1", "2026/01", "2026-01-01", "2026-01\n",
            " 2026-01", "0000-01", "2026-00", "2026-13", 202601,
        )
        for field in ("start_date", "end_date"):
            for value in invalid_months:
                with self.subTest(field=field, value=value):
                    data = fictional_project_data()
                    data.update(is_ongoing=False, end_date="2026-12")
                    data[field] = value
                    self.assert_invalid(data, (field,))
        data = fictional_project_data()
        data["start_date"] = None
        self.assert_invalid(data, ("start_date",))

    def test_ongoing_flag_requires_an_actual_boolean(self):
        for value in ("true", "false", 1, 0, None):
            with self.subTest(value=value):
                data = fictional_project_data()
                data["is_ongoing"] = value
                self.assert_invalid(data, ("is_ongoing",))

    def test_dates_and_ongoing_status_must_be_consistent(self):
        valid_cases = (
            {},
            {"end_date": None},
            {"is_ongoing": False, "end_date": "2026-01"},
            {"is_ongoing": False, "end_date": "2026-03"},
            {"is_ongoing": False, "start_date": "2025-12", "end_date": "2026-01"},
        )
        for changes in valid_cases:
            with self.subTest(valid_dates=changes):
                data = fictional_project_data()
                data.update(changes)
                record = Project(**data)
                self.assertEqual(record.start_date, data["start_date"])
                self.assertEqual(record.end_date, data.get("end_date"))
        invalid_cases = (
            {"end_date": "2026-03"},
            {"is_ongoing": False},
            {"is_ongoing": False, "end_date": None},
            {"is_ongoing": False, "start_date": "2026-06", "end_date": "2026-03"},
            {"is_ongoing": False, "end_date": "2025-12"},
        )
        for changes in invalid_cases:
            with self.subTest(invalid_dates=changes):
                data = fictional_project_data()
                data.update(changes)
                self.assert_invalid(data, ())


if __name__ == "__main__":
    unittest.main()
