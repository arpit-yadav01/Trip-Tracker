import SQLite from "react-native-sqlite-storage";

SQLite.enablePromise(true);

let db = null;

export async function initDB() {
  try {
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
  } catch (error) {
    console.log("DB init error:", error);
  }
}


export async function insertLocation(tripId, userId, lat, lng, timestamp) {
  if (!db) return;

  await db.executeSql(
    `INSERT INTO locations 
     (trip_id, user_id, lat, lng, timestamp, synced)
     VALUES (?, ?, ?, ?, ?, 0);`,
    [tripId, userId, lat, lng, timestamp]
  );
}

export async function getUnsyncedLocations(limit = 100) {
  if (!db) return [];

  const result = await db.executeSql(
    `SELECT * FROM locations 
     WHERE synced = 0 
     ORDER BY id ASC 
     LIMIT ?;`,
    [limit]
  );

  return result[0].rows.raw();
}

export async function markLocationsSynced(ids) {
  if (!db || ids.length === 0) return;

  const placeholders = ids.map(() => "?").join(",");

  await db.executeSql(
    `UPDATE locations SET synced = 1 WHERE id IN (${placeholders});`,
    ids
  );
}

export async function getLastLocation() {
  if (!db) return null;

  const result = await db.executeSql(
    `SELECT * FROM locations 
     ORDER BY id DESC 
     LIMIT 1;`
  );

  if (result[0].rows.length > 0) {
    return result[0].rows.item(0);
  }

  return null;
}


export async function insertLocation(tripId, userId, lat, lng, timestamp) {
  if (!db) return;

  await db.executeSql(
    `INSERT INTO locations 
     (trip_id, user_id, lat, lng, timestamp, synced)
     VALUES (?, ?, ?, ?, ?, 0);`,
    [tripId, userId, lat, lng, timestamp]
  );
}

export async function getUnsyncedLocations(limit = 100) {
  if (!db) return [];

  const result = await db.executeSql(
    `SELECT * FROM locations 
     WHERE synced = 0 
     ORDER BY id ASC 
     LIMIT ?;`,
    [limit]
  );

  return result[0].rows.raw();
}

export async function markLocationsSynced(ids) {
  if (!db || ids.length === 0) return;

  const placeholders = ids.map(() => "?").join(",");

  await db.executeSql(
    `UPDATE locations SET synced = 1 WHERE id IN (${placeholders});`,
    ids
  );
}

export async function getLastLocation() {
  if (!db) return null;

  const result = await db.executeSql(
    `SELECT * FROM locations 
     ORDER BY id DESC 
     LIMIT 1;`
  );

  if (result[0].rows.length > 0) {
    return result[0].rows.item(0);
  }

  return null;
}