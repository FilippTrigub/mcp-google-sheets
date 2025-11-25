/**
 * Resource implementations for Google Sheets MCP Server
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ErrorCode,
  McpError
} from '@modelcontextprotocol/sdk/types.js';
import { getServices } from './index.js';

/**
 * Register all resources with the MCP server
 */
export function registerResources(server: Server) {
  // List available resources
  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
      resources: [
        {
          uri: 'spreadsheet://info',
          name: 'Spreadsheet Info',
          description: 'Get basic information about a Google Spreadsheet',
          mimeType: 'application/json'
        }
      ]
    };
  });

  // Handle resource reads
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const { uri } = request.params;

    try {
      // Parse URI: spreadsheet://{spreadsheet_id}/info
      const match = uri.match(/^spreadsheet:\/\/([^\/]+)\/info$/);
      if (!match) {
        throw new McpError(
          ErrorCode.InvalidRequest,
          `Invalid resource URI: ${uri}. Expected format: spreadsheet://{spreadsheet_id}/info`
        );
      }

      const spreadsheetId = match[1];
      return await getSpreadsheetInfo(spreadsheetId, uri);
    } catch (error) {
      if (error instanceof McpError) {
        throw error;
      }
      throw new McpError(
        ErrorCode.InternalError,
        `Error reading resource: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  });
}

async function getSpreadsheetInfo(spreadsheetId: string, uri: string) {
  const { sheetsService } = getServices();

  const result = await sheetsService.spreadsheets.get({
    spreadsheetId
  });

  const info = {
    title: result.data.properties?.title || 'Unknown',
    sheets: result.data.sheets?.map((sheet: any) => ({
      title: sheet.properties?.title,
      sheetId: sheet.properties?.sheetId,
      gridProperties: sheet.properties?.gridProperties
    })) || []
  };

  return {
    contents: [
      {
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(info, null, 2)
      }
    ]
  };
}
