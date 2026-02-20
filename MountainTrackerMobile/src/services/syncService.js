import NetInfo from "@react-native-community/netinfo";
import axios from "axios";
import { getUnsyncedLocations, markLocationsSynced } from "../storage/localDB";

let syncing = false;

export function startSyncEngine(apiBaseUrl) {
  setInterval(async () => {

    if (syncing) return;

    const state = await NetInfo.fetch();
    if (!state.isConnected) return;

    syncing = true;

    try {
      const locations = await getUnsyncedLocations(100);

      if (locations.length === 0) {
        syncing = false;
        return;
      }

      await axios.post(`${apiBaseUrl}/tracking/batch`, {
        locations
      });

      const ids = locations.map(l => l.id);
      await markLocationsSynced(ids);

      console.log("Batch synced:", ids.length);

    } catch (err) {
      console.log("Sync failed:", err.message);
    } finally {
      syncing = false;
    }

  }, 15000);
}