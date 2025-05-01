"""
add polls tables
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            name VARCHAR(256) NOT NULL
        )
        """,
        "DROP TABLE IF EXISTS polls",
    ),
    step(
        """
        CREATE TABLE IF NOT EXISTS poll_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls (id) ON DELETE CASCADE
        )
        """,
        "DROP TABLE IF EXISTS poll_variants",
    ),
]
