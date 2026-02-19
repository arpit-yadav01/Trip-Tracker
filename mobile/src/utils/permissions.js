import { PermissionsAndroid, Platform } from "react-native";

export async function requestSMSPermission() {
  if (Platform.OS !== "android") return false;

  try {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.SEND_SMS,
      {
        title: "SMS Permission Required",
        message:
          "SMS is used only for emergency safety alerts when internet is unavailable.",
        buttonNeutral: "Ask Me Later",
        buttonNegative: "Cancel",
        buttonPositive: "Allow",
      }
    );

    return granted === PermissionsAndroid.RESULTS.GRANTED;
  } catch (err) {
    console.warn(err);
    return false;
  }
}
