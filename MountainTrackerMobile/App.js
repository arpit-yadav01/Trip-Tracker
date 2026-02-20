import React, { useEffect } from "react";
import { StatusBar, StyleSheet, useColorScheme, View } from "react-native";
import {
  SafeAreaProvider,
  useSafeAreaInsets,
} from "react-native-safe-area-context";

import { initDB } from "./src/storage/localDB";
import { startSyncEngine } from "./src/services/syncService";
import { startOfflineMonitor } from "./src/services/offlineMonitor";

function App() {
  const isDarkMode = useColorScheme() === "dark";

  useEffect(() => {
    // Initialize Local SQLite DB
    initDB();

    // Start background sync engine
    startSyncEngine("http://192.168.1.6:8000");

    // Start offline monitor (5 minutes threshold)
    startOfflineMonitor(
      5,                // threshold minutes
      "+911234567890"   // replace with real emergency number
    );
  }, []);

  return (
    <SafeAreaProvider>
      <StatusBar barStyle={isDarkMode ? "light-content" : "dark-content"} />
      <AppContent />
    </SafeAreaProvider>
  );
}

function AppContent() {
  const safeAreaInsets = useSafeAreaInsets();

  return <View style={styles.container} />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;