// index.js
import { loadConfig } from "./utils.js";

async function main() {
  const config = loadConfig();

  // Determine which server to run based on the mode in config
  if (config.mode === "stdio") {
    const { default: startStdioServer } = await import("./stdio-server.js");
    await startStdioServer();
  } else {
    const { default: startSseServer } = await import("./sse-server.js");
    await startSseServer();
  }
}

main().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});
