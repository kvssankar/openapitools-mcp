// stdio-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { AnthropicAdapter } from "@reacter/openapitools";
import { loadConfig } from "./utils.js";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default async function startStdioServer() {
  // Load configuration
  const mcpConfig = loadConfig();

  // Set default refresh time to 1 day (in minutes) if not specified
  const refreshTimeMinutes = mcpConfig.refresh_time_minutes || 24 * 60; // 1 day default

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

    const mcpTools = [];
    for (let tool of tools) {
      mcpTools.push({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.input_schema,
      });
    }

    // Update cache
    toolsCache.tools = mcpTools;
    toolsCache.lastFetchTime = Date.now();

    return mcpTools;
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

  const transport = new StdioServerTransport();
  await server.connect(transport);
}
