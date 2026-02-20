import NetInfo from "@react-native-community/netinfo";
import { sendEmergencySMS } from "../native/sms";
import { getLastLocation } from "../storage/localDB";

let offlineStart = null;
let smsSent = false;

export function startOfflineMonitor(
  thresholdMinutes,
  emergencyPhone
) {
  setInterval(async () => {
    const state = await NetInfo.fetch();

    if (!state.isConnected) {
      if (!offlineStart) {
        offlineStart = Date.now();
      }

      const offlineMinutes =
        (Date.now() - offlineStart) / 60000;

      if (offlineMinutes > thresholdMinutes && !smsSent) {

        const location = await getLastLocation();

        if (!location) {
          console.log("No GPS stored locally yet.");
          return;
        }

        const message = `
🚨 SAFETY ALERT

User Offline
Last Location:
https://maps.google.com/?q=${location.lat},${location.lng}
`;

        await sendEmergencySMS(emergencyPhone, message);
        smsSent = true;
      }
    } else {
      offlineStart = null;
      smsSent = false;
    }
  }, 60000);
}