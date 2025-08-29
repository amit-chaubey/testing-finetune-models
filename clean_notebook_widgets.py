import sys
import json
from pathlib import Path


def remove_invalid_widget_state(nb: dict) -> dict:
    # Remove top-level widgets metadata if missing required keys
    metadata = nb.get("metadata", {})
    widgets = metadata.get("widgets")
    if isinstance(widgets, dict):
        state = widgets.get("state") if isinstance(widgets, dict) else None
        if state is None:
            metadata.pop("widgets", None)
            nb["metadata"] = metadata

    # Also check each cell's metadata for widgets
    for cell in nb.get("cells", []):
        cell_md = cell.get("metadata", {})
        w = cell_md.get("widgets")
        if isinstance(w, dict):
            st = w.get("state") if isinstance(w, dict) else None
            if st is None:
                cell_md.pop("widgets", None)
                cell["metadata"] = cell_md
    return nb


def main(path_str: str) -> None:
    path = Path(path_str)
    data = json.loads(path.read_text(encoding="utf-8"))
    cleaned = remove_invalid_widget_state(data)
    backup_path = path.with_suffix(path.suffix + ".bak")
    backup_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Cleaned: {path}\nBackup written to: {backup_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_notebook_widgets.py <notebook.ipynb>")
        sys.exit(1)
    main(sys.argv[1])


