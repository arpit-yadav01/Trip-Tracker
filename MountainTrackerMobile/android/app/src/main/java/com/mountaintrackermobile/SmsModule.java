package com.mountaintracker;
   // use your real package name

import android.telephony.SmsManager;
import com.facebook.react.bridge.*;

public class SmsModule extends ReactContextBaseJavaModule {

    SmsModule(ReactApplicationContext context) {
        super(context);
    }

    @Override
    public String getName() {
        return "SmsModule";
    }

    @ReactMethod
    public void sendSMS(String phoneNumber, String message, Promise promise) {
        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phoneNumber, null, message, null, null);
            promise.resolve("SMS Sent");
        } catch (Exception e) {
            promise.reject("SMS_ERROR", e);
        }
    }
}
