import aiosqlite
from datetime import datetime
from pathlib import Path
from backend.config import settings


async def get_db():
    db_path = Path(settings.database_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(db_path)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys = ON")
    return db


async def init_db():
    db = await get_db()
    try:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
        """)
        await db.commit()
    finally:
        await db.close()


async def create_conversation(title: str = "新しいチャット") -> dict:
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,)
        )
        await db.commit()
        conversation_id = cursor.lastrowid
        cursor = await db.execute(
            "SELECT * FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        row = await cursor.fetchone()
        return dict(row)
    finally:
        await db.close()


async def get_conversations() -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM conversations ORDER BY updated_at DESC"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_conversation(conversation_id: int) -> dict | None:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        conversation = dict(row)

        cursor = await db.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,)
        )
        messages = await cursor.fetchall()
        conversation["messages"] = [dict(msg) for msg in messages]
        return conversation
    finally:
        await db.close()


async def delete_conversation(conversation_id: int) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def add_message(conversation_id: int, role: str, content: str) -> dict:
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, role, content)
        )
        message_id = cursor.lastrowid

        await db.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), conversation_id)
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT * FROM messages WHERE id = ?",
            (message_id,)
        )
        row = await cursor.fetchone()
        return dict(row)
    finally:
        await db.close()


async def update_conversation_title(conversation_id: int, title: str) -> bool:
    db = await get_db()
    try:
        cursor = await db.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, datetime.now().isoformat(), conversation_id)
        )
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def get_conversation_messages(conversation_id: int) -> list[dict]:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()
