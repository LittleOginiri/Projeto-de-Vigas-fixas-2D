import sqlite3
import json
from pathlib import Path
from typing import List, Any

DB_PATH = Path("statics/data.db")

class SQLiteProjectDAO:
    def __init__(self) -> None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS project (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          payload_json TEXT NOT NULL
        )""")
        self.conn.commit()

    def save_project(self, project: Any) -> None:
        payload = json.dumps(project, ensure_ascii=False)
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO project (id, name, payload_json) VALUES (?, ?, ?)",
            (project["id"], project["name"], payload)
        )
        self.conn.commit()

    def load_project(self, project_id: str) -> Any:
        cur = self.conn.cursor()
        row = cur.execute(
            "SELECT payload_json FROM project WHERE id = ?", (project_id,)
        ).fetchone()
        return json.loads(row[0]) if row else None

    def list_projects(self) -> List[str]:
        cur = self.conn.cursor()
        return [r[0] for r in cur.execute("SELECT id FROM project ORDER BY name").fetchall()]

    def delete_project(self, project_id: str) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM project WHERE id = ?", (project_id,))
        self.conn.commit()