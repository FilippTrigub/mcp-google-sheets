#!/usr/bin/env node

/**
 * Google Spreadsheet MCP Server
 * A Model Context Protocol (MCP) server for interacting with Google Sheets
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ErrorCode,
  McpError
} from '@modelcontextprotocol/sdk/types.js';
import { google, sheets_v4, drive_v3 } from 'googleapis';
import { authenticateGoogle } from './auth.js';
import { registerTools } from './tools.js';
import { registerResources } from './resources.js';

// Global services
let sheetsService: sheets_v4.Sheets;
let driveService: drive_v3.Drive;
let folderIdContext: string | undefined;

/**
 * Initialize Google API services
 */
async function initializeServices() {
  try {
    const auth = await authenticateGoogle();
    
    sheetsService = google.sheets({ version: 'v4', auth: auth as any });
    driveService = google.drive({ version: 'v3', auth: auth as any });
    folderIdContext = process.env.DRIVE_FOLDER_ID;
    
    console.error('Google Sheets services initialized successfully');
  } catch (error) {
    console.error('Failed to initialize services:', error);
    throw error;
  }
}

/**
 * Get the initialized services
 */
export function getServices() {
  if (!sheetsService || !driveService) {
    throw new Error('Services not initialized');
  }
  return { sheetsService, driveService, folderIdContext };
}

/**
 * Main server function
 */
async function main() {
  console.error('Starting Google Sheets MCP Server...');

  // Initialize services
  await initializeServices();

  // Create MCP server
  const server = new Server(
    {
      name: 'google-sheets-server',
      version: '1.0.0'
    },
    {
      capabilities: {
        tools: {},
        resources: {}
      }
    }
  );

  // Register all tools and resources
  registerTools(server);
  registerResources(server);

  // Connect to stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('Google Sheets MCP Server running on stdio');
}

// Handle process termination
process.on('SIGINT', () => {
  console.error('Shutting down server...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.error('Shutting down server...');
  process.exit(0);
});

// Run the server
main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
