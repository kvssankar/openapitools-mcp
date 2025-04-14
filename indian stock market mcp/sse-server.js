// sse-server.js
import express from "express";
import cors from "cors";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { AnthropicAdapter } from "@reacter/openapitools";
import { loadConfig } from "./utils.js";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default async function startSseServer() {
  // Load configuration
  const mcpConfig = loadConfig();

  // Set default refresh time to 1 day (in minutes) if not specified
  const refreshTimeMinutes = mcpConfig.refresh_time_minutes || 24 * 60; // 1 day default

  const app = express();

  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  const toolsAdapter = new AnthropicAdapter(
    mcpConfig.api_key || path.join(__dirname, "openapitools"),
    {
      verbose: false, // Needs to be false to work with claude desktop (stdio), turn it on for sse
    }
  );

  toolsAdapter.setEnvironmentVariables(mcpConfig.envs);

  const toolHandler = await toolsAdapter.createAnthropicToolHandler();

  // Cache for tools
  let toolsCache = {
    tools: [],
    lastFetchTime: 0,
  };

  // Function to fetch and update tools cache
  async function refreshToolsCache() {
    // Check if tool_names array exists and has items
    const toolNames =
      mcpConfig.tool_names && mcpConfig.tool_names.length > 0
        ? mcpConfig.tool_names
        : undefined;

    // Fetch tools
    const tools = await toolsAdapter.getAnthropicTools(toolNames);

    // Update cache
    toolsCache.tools = tools;
    toolsCache.lastFetchTime = Date.now();

    return tools;
  }

  // Check if cache needs refreshing
  function shouldRefreshCache() {
    const cacheAgeMs = Date.now() - toolsCache.lastFetchTime;
    const refreshThresholdMs = refreshTimeMinutes * 60 * 1000;
    return cacheAgeMs > refreshThresholdMs || toolsCache.tools.length === 0;
  }

  // Initial tools fetch
  await refreshToolsCache();

  const server = new Server(
    {
      name: mcpConfig.server_name || "example-server",
      version: mcpConfig.server_version || "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    // Check if cache needs refreshing
    if (shouldRefreshCache()) {
      await refreshToolsCache();
    }

    return {
      tools: toolsCache.tools,
    };
  });

  // Add endpoint for manual refresh
  server.setRequestHandler(
    {
      method: "POST",
      path: "/refresh-tools",
    },
    async () => {
      try {
        await refreshToolsCache();
        return {
          success: true,
          message: "Tools cache refreshed successfully",
          timestamp: new Date().toISOString(),
        };
      } catch (error) {
        return {
          success: false,
          message: `Error refreshing tools: ${error.message}`,
          timestamp: new Date().toISOString(),
        };
      }
    }
  );

  server.setRequestHandler(CallToolRequestSchema, async (request, extra) => {
    try {
      const result = await toolHandler({
        id: "223",
        name: request.params.name,
        input: request.params.arguments,
      });
      return {
        content: [
          {
            type: "text",
            text: result.output,
          },
        ],
      };
    } catch (e) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${e.message}`,
          },
        ],
        isError: true,
      };
    }
  });

  const transports = {};

  app.get("/sse", async (_, res) => {
    const transport = new SSEServerTransport("/messages", res);
    transports[transport.sessionId] = transport;
    res.on("close", () => {
      delete transports[transport.sessionId];
    });
    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    const sessionId = req.query.sessionId;
    const transport = transports[sessionId];
    if (transport) {
      await transport.handlePostMessage(req, res);
    } else {
      res.status(400).send("No transport found for sessionId");
    }
  });

  // Also add REST endpoint for manual refresh outside of MCP
  app.get("/api/refresh-tools", async (req, res) => {
    try {
      await refreshToolsCache();
      res.json({
        success: true,
        message: "Tools cache refreshed successfully",
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: `Error refreshing tools: ${error.message}`,
        timestamp: new Date().toISOString(),
      });
    }
  });

  const port = mcpConfig.port || 3001;
  return new Promise((resolve) => {
    app.listen(port, mcpConfig.host || "0.0.0.0", () => {
      resolve();
    });
  });
}
