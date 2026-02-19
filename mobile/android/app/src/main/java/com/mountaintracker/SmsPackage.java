package com.triptracker;

import com.facebook.react.*;
import java.util.*;

public class SmsPackage implements ReactPackage {

    @Override
    public List<NativeModule> createNativeModules(
        ReactApplicationContext reactContext
    ) {
        return Arrays.<NativeModule>asList(
            new SmsModule(reactContext)
        );
    }

    @Override
    public List<ViewManager> createViewManagers(
        ReactApplicationContext reactContext
    ) {
        return Collections.emptyList();
    }
}
