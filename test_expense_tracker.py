
import json
import expense_tracker


def test_wrong_json_structure_creates_backup(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    original_data = {"amount": 100, "category": "Food"}
    test_file.write_text(json.dumps(original_data), encoding="utf-8")

    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []

    backup_path = test_file.with_suffix(".json.bak")
    assert backup_path.exists()

    with backup_path.open("r", encoding="utf-8") as f:
        backup_data = json.load(f)

    assert backup_data == original_data


def test_invalid_json_creates_backup(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    original_data = "{invalid json}"
    test_file.write_text(original_data, encoding="utf-8")

    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []

    backup_path = test_file.with_suffix(".json.bak")
    assert backup_path.exists()

    backup_data = backup_path.read_text(encoding="utf-8")
    assert backup_data == original_data


def test_valid_json_list_loads_successfully(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    original_data = [
        {"amount": 100, "category": "Food"},
        {"amount": 200, "category": "Travel"}
    ]

    test_file.write_text(json.dumps(original_data), encoding="utf-8")

    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == original_data

    backup_path = test_file.with_suffix(".json.bak")
    assert not backup_path.exists()


def test_missing_file_initializes_empty_list(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []
    assert not test_file.exists()
