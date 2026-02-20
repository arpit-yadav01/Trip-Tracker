import React, { useEffect } from "react";
import { StatusBar, StyleSheet, useColorScheme, View } from "react-native";
import {
  SafeAreaProvider,
  useSafeAreaInsets,
} from "react-native-safe-area-context";

import { initDB } from "./src/storage/localDB";
import { startSyncEngine } from "./src/services/syncService";

function App() {
  const isDarkMode = useColorScheme() === "dark";

  useEffect(() => {
    initDB();
    startSyncEngine("http://YOUR_BACKEND_IP:8000");
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

  return (
    <View style={styles.container}>
      {/* Your real app UI will go here */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;