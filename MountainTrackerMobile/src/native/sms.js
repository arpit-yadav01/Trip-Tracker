import { NativeModules } from "react-native";

const { SmsModule } = NativeModules;

export async function sendEmergencySMS(phone, message) {
  try {
    const result = await SmsModule.sendSMS(phone, message);
    console.log("SMS Sent:", result);
  } catch (error) {
    console.log("SMS Error:", error);
  }
}