# Contributing Guide

## Folder Rules

- Put all learning content under `learning-paths/`
- Use this grouping:
  - `learning-paths/python/`
  - `learning-paths/ml/`
  - `learning-paths/web/`
- Prefer lowercase folder names with hyphens for new additions.

## Naming Rules

- New files should use clear names, for example:
  - `variables-basics.py`
  - `chapter-01-exercises.py`
  - `regression-basics.ipynb`
- Avoid generic names like `new file.py`.

## Notebook Hygiene

- Keep cells concise and well-commented.
- If possible, clear extremely large outputs before committing.
- Store datasets in the same track folder or document source links.

## Commit Style

Use short, focused commits:

- `docs: rewrite README with folder structure`
- `chore: move course content into learning-paths`
- `feat: add model accuracy evaluation notebook cell`

## Pull Requests

- Explain what changed and why.
- Mention impacted track folder(s).
- Add screenshots only when UI/web files are changed.
