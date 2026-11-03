
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

    backup_files = list(test_file.parent.glob(f"{test_file.stem}_*.json.bak"))
    assert len(backup_files) >= 1

    backup_path = backup_files[0]

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

    backup_files = list(test_file.parent.glob(f"{test_file.stem}_*.json.bak"))
    assert len(backup_files) >= 1

    backup_path = backup_files[0]
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

    backup_files = list(test_file.parent.glob(f"{test_file.stem}_*.json.bak"))
    assert len(backup_files) == 0


def test_missing_file_initializes_empty_list(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []
    assert not test_file.exists()

def test_multiple_backups_are_preserved(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"
    
    monkeypatch.setattr(expense_tracker, "FILE_PATH", test_file)

    original_data = "{invalid json}"
    test_file.write_text(original_data, encoding="utf-8")

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []
    
    backup_files = list(test_file.parent.glob(f"{test_file.stem}_*.json.bak"))
    assert len(backup_files) >= 1

    backup_path = backup_files[0]
    backup_data = backup_path.read_text(encoding="utf-8")

    assert backup_data == original_data

    original_data = "{It is not a valid json}"
    test_file.write_text(original_data, encoding="utf-8")

    tracker = expense_tracker.ExpenseTracker()
    tracker.load_expenses()

    assert tracker.expenses == []
    
    backup_files = list(test_file.parent.glob(f"{test_file.stem}_*.json.bak"))

    assert len(backup_files) == 2
    
    backup_contents = {
        backup.read_text(encoding="utf-8")
        for backup in backup_files
    }
    
    assert backup_contents == {
        "{invalid json}",
        "{It is not a valid json}"
    }

