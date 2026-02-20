import SQLite from "react-native-sqlite-storage";

SQLite.enablePromise(true);

let db;

export async function initDB() {
  db = await SQLite.openDatabase({
    name: "tracker.db",
    location: "default"
  });

  await db.executeSql(`
    CREATE TABLE IF NOT EXISTS locations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      trip_id TEXT,
      user_id TEXT,
      lat REAL,
      lng REAL,
      timestamp INTEGER,
      synced INTEGER DEFAULT 0
    );
  `);

  await db.executeSql(`
    CREATE INDEX IF NOT EXISTS idx_synced
    ON locations (synced);
  `);

  console.log("Local DB ready");
}