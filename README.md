# Expense Tracker

A simple command-line expense tracker built in Python. It lets you add expenses,
view them, and see totals grouped by category. Expenses are saved to a local
JSON file so your data is still there the next time you run the program.

## Requirements

- Python 3 (no extra installs needed — this project only uses Python's
  built-in `datetime` and `json` modules)

## Menu Options

1. **Add Expense** — enter a category and amount; the date is recorded automatically.
2. **View Expenses** — see all recorded expenses with amount, category, and date.
3. **Totals by Category** — see the total amount spent per category.
4. **Exit** — saves all expenses to `expenses.json` and closes the program.

## Notes

- Amounts are stored as positive numbers regardless of input (negative values are converted using `abs()`).
- Categories are case-insensitive (e.g. "Food" and "food" are treated the same).