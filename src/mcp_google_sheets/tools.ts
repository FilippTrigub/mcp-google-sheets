/**
 * Tool implementations for Google Sheets MCP Server
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError
} from '@modelcontextprotocol/sdk/types.js';
import { getServices } from './index.js';

/**
 * Register all tools with the MCP server
 */
export function registerTools(server: Server) {
  // List available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: 'list_spreadsheets',
          description: 'Lists spreadsheets in the configured Drive folder or accessible by the user',
          inputSchema: {
            type: 'object',
            properties: {
              folder_id: {
                type: 'string',
                description: 'Optional Google Drive folder ID to search in'
              }
            }
          }
        },
        {
          name: 'create_spreadsheet',
          description: 'Creates a new spreadsheet',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'The desired title for the spreadsheet'
              },
              folder_id: {
                type: 'string',
                description: 'Optional Google Drive folder ID where the spreadsheet should be created'
              }
            },
            required: ['title']
          }
        },
        {
          name: 'get_sheet_data',
          description: 'Get data from a specific sheet in a Google Spreadsheet',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet'
              },
              sheet: {
                type: 'string',
                description: 'The name of the sheet'
              },
              range: {
                type: 'string',
                description: 'Optional cell range in A1 notation (e.g., A1:C10)'
              },
              include_grid_data: {
                type: 'boolean',
                description: 'If true, includes cell formatting and metadata',
                default: false
              }
            },
            required: ['spreadsheet_id', 'sheet']
          }
        },
        {
          name: 'update_cells',
          description: 'Update cells in a Google Spreadsheet',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet'
              },
              sheet: {
                type: 'string',
                description: 'The name of the sheet'
              },
              range: {
                type: 'string',
                description: 'Cell range in A1 notation'
              },
              data: {
                type: 'array',
                description: '2D array of values to update',
                items: {
                  type: 'array'
                }
              }
            },
            required: ['spreadsheet_id', 'sheet', 'range', 'data']
          }
        },
        {
          name: 'list_sheets',
          description: 'List all sheets in a Google Spreadsheet',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet'
              }
            },
            required: ['spreadsheet_id']
          }
        },
        {
          name: 'create_sheet',
          description: 'Create a new sheet tab in an existing Google Spreadsheet',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet'
              },
              title: {
                type: 'string',
                description: 'The title for the new sheet'
              }
            },
            required: ['spreadsheet_id', 'title']
          }
        },
        {
          name: 'share_spreadsheet',
          description: 'Share a Google Spreadsheet with multiple users via email',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet to share'
              },
              recipients: {
                type: 'array',
                description: 'List of recipients with email_address and role',
                items: {
                  type: 'object',
                  properties: {
                    email_address: { type: 'string' },
                    role: { type: 'string', enum: ['reader', 'commenter', 'writer'] }
                  },
                  required: ['email_address', 'role']
                }
              },
              send_notification: {
                type: 'boolean',
                description: 'Whether to send notification emails',
                default: true
              }
            },
            required: ['spreadsheet_id', 'recipients']
          }
        },
        {
          name: 'batch_update_cells',
          description: 'Update multiple ranges in a Google Spreadsheet in one call',
          inputSchema: {
            type: 'object',
            properties: {
              spreadsheet_id: {
                type: 'string',
                description: 'The ID of the spreadsheet'
              },
              sheet: {
                type: 'string',
                description: 'The name of the sheet'
              },
              ranges: {
                type: 'object',
                description: 'Dictionary mapping range strings to 2D arrays of values'
              }
            },
            required: ['spreadsheet_id', 'sheet', 'ranges']
          }
        }
      ]
    };
  });

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      switch (name) {
        case 'list_spreadsheets':
          return await listSpreadsheetsHandler(args);
        case 'create_spreadsheet':
          return await createSpreadsheetHandler(args);
        case 'get_sheet_data':
          return await getSheetDataHandler(args);
        case 'update_cells':
          return await updateCellsHandler(args);
        case 'list_sheets':
          return await listSheetsHandler(args);
        case 'create_sheet':
          return await createSheetHandler(args);
        case 'share_spreadsheet':
          return await shareSpreadsheetHandler(args);
        case 'batch_update_cells':
          return await batchUpdateCellsHandler(args);
        default:
          throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
      }
    } catch (error) {
      if (error instanceof McpError) {
        throw error;
      }
      throw new McpError(
        ErrorCode.InternalError,
        `Error executing tool ${name}: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  });
}

// Tool handler implementations
async function listSpreadsheetsHandler(args: any) {
  const { driveService, folderIdContext } = getServices();
  const targetFolderId = args.folder_id || folderIdContext;

  let query = "mimeType='application/vnd.google-apps.spreadsheet'";
  
  if (targetFolderId) {
    query += ` and '${targetFolderId}' in parents`;
    console.error(`Searching for spreadsheets in folder: ${targetFolderId}`);
  } else {
    console.error("Searching for spreadsheets in 'My Drive'");
  }

  const result = await driveService.files.list({
    q: query,
    spaces: 'drive',
    includeItemsFromAllDrives: true,
    supportsAllDrives: true,
    fields: 'files(id, name)',
    orderBy: 'modifiedTime desc'
  });

  const spreadsheets = result.data.files || [];
  const output = spreadsheets.map((sheet: any) => ({
    id: sheet.id,
    title: sheet.name
  }));

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(output, null, 2)
      }
    ]
  };
}

async function createSpreadsheetHandler(args: any) {
  const { driveService, folderIdContext } = getServices();
  const { title, folder_id } = args;
  const targetFolderId = folder_id || folderIdContext;

  const fileBody: any = {
    name: title,
    mimeType: 'application/vnd.google-apps.spreadsheet'
  };

  if (targetFolderId) {
    fileBody.parents = [targetFolderId];
  }

  const result = await driveService.files.create({
    supportsAllDrives: true,
    requestBody: fileBody,
    fields: 'id, name, parents'
  });

  const spreadsheetId = result.data.id;
  const parents = result.data.parents;
  const folderInfo = targetFolderId ? ` in folder ${targetFolderId}` : ' in root';
  console.error(`Spreadsheet created with ID: ${spreadsheetId}${folderInfo}`);

  const output = {
    spreadsheetId,
    title: result.data.name || title,
    folder: parents ? parents[0] : 'root'
  };

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(output, null, 2)
      }
    ]
  };
}

async function getSheetDataHandler(args: any) {
  const { sheetsService } = getServices();
  const { spreadsheet_id, sheet, range, include_grid_data = false } = args;

  const fullRange = range ? `${sheet}!${range}` : sheet;

  if (include_grid_data) {
    const result = await sheetsService.spreadsheets.get({
      spreadsheetId: spreadsheet_id,
      ranges: [fullRange],
      includeGridData: true
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result.data, null, 2)
        }
      ]
    };
  } else {
    const result = await sheetsService.spreadsheets.values.get({
      spreadsheetId: spreadsheet_id,
      range: fullRange
    });

    const output = {
      spreadsheetId: spreadsheet_id,
      valueRanges: [
        {
          range: fullRange,
          values: result.data.values || []
        }
      ]
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(output, null, 2)
        }
      ]
    };
  }
}

async function updateCellsHandler(args: any) {
  const { sheetsService } = getServices();
  const { spreadsheet_id, sheet, range, data } = args;

  const fullRange = `${sheet}!${range}`;

  const result = await sheetsService.spreadsheets.values.update({
    spreadsheetId: spreadsheet_id,
    range: fullRange,
    valueInputOption: 'USER_ENTERED',
    requestBody: {
      values: data
    }
  });

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(result.data, null, 2)
      }
    ]
  };
}

async function listSheetsHandler(args: any) {
  const { sheetsService } = getServices();
  const { spreadsheet_id } = args;

  const result = await sheetsService.spreadsheets.get({
    spreadsheetId: spreadsheet_id
  });

  const sheetNames = result.data.sheets?.map((sheet: any) => sheet.properties?.title) || [];

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(sheetNames, null, 2)
      }
    ]
  };
}

async function createSheetHandler(args: any) {
  const { sheetsService } = getServices();
  const { spreadsheet_id, title } = args;

  const result = await sheetsService.spreadsheets.batchUpdate({
    spreadsheetId: spreadsheet_id,
    requestBody: {
      requests: [
        {
          addSheet: {
            properties: {
              title
            }
          }
        }
      ]
    }
  });

  const newSheetProps = result.data.replies?.[0]?.addSheet?.properties;

  const output = {
    sheetId: newSheetProps?.sheetId,
    title: newSheetProps?.title,
    index: newSheetProps?.index,
    spreadsheetId: spreadsheet_id
  };

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(output, null, 2)
      }
    ]
  };
}

async function shareSpreadsheetHandler(args: any) {
  const { driveService } = getServices();
  const { spreadsheet_id, recipients, send_notification = true } = args;

  const successes: any[] = [];
  const failures: any[] = [];

  for (const recipient of recipients) {
    const { email_address, role } = recipient;

    if (!email_address) {
      failures.push({
        email_address: null,
        error: 'Missing email_address in recipient entry'
      });
      continue;
    }

    if (!['reader', 'commenter', 'writer'].includes(role)) {
      failures.push({
        email_address,
        error: `Invalid role '${role}'. Must be 'reader', 'commenter', or 'writer'`
      });
      continue;
    }

    try {
      const result = await driveService.permissions.create({
        fileId: spreadsheet_id,
        sendNotificationEmail: send_notification,
        requestBody: {
          type: 'user',
          role,
          emailAddress: email_address
        },
        fields: 'id'
      });

      successes.push({
        email_address,
        role,
        permissionId: result.data.id
      });
    } catch (error: any) {
      failures.push({
        email_address,
        error: `Failed to share: ${error.message || String(error)}`
      });
    }
  }

  const output = { successes, failures };

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(output, null, 2)
      }
    ]
  };
}

async function batchUpdateCellsHandler(args: any) {
  const { sheetsService } = getServices();
  const { spreadsheet_id, sheet, ranges } = args;

  const data = Object.entries(ranges).map(([range, values]) => ({
    range: `${sheet}!${range}`,
    values
  }));

  const result = await sheetsService.spreadsheets.values.batchUpdate({
    spreadsheetId: spreadsheet_id,
    requestBody: {
      valueInputOption: 'USER_ENTERED',
      data
    }
  });

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(result.data, null, 2)
      }
    ]
  };
}
