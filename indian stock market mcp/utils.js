// utils.js
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

// Get the directory name of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Loads configuration from mcpconfig.json file
 * @returns {Object} The parsed configuration object
 */
export function loadConfig() {
  try {
    const config = JSON.parse(
      fs.readFileSync(path.join(__dirname, "mcpconfig.json"), "utf8")
    );
    return config;
  } catch (error) {
    console.warn(
      "Could not read mcpconfig.json, using defaults:",
      error.message
    );
    return {
      server_name: "anthropic-mcp-server",
      host: "0.0.0.0",
      port: 8000,
      server_version: "1.0.0",
      tool_names: [],
      mode: "sse", // Default mode
      refresh_time_minutes: 1440, // 24 hours by default
      envs: [],
    };
  }
}
