# MCP Google Sheets - Project Context

## Recent Changes

### Complete Rewrite to Node.js/TypeScript
The entire server implementation has been rewritten from Python to Node.js/TypeScript:
- **Language**: Migrated from Python 3.10+ to Node.js 18+ with TypeScript 5.7
- **SDK**: Now uses `@modelcontextprotocol/sdk` (official Node.js MCP SDK)
- **Package Manager**: Changed from `uv` to `npm`
- **Build System**: TypeScript compiler (`tsc`) with ES2022 modules
- **Architecture**: Modular design with separate files for auth, tools, and resources
- **Compatibility**: All authentication methods and tools preserved from Python version

### OAuth 2.0 Standard Flow (Authentication Method)
OAuth2 authentication supports environment variables instead of a credentials file:
- **New Variables**: `GOOGLE_SHEETS_CLIENT_ID` and `GOOGLE_SHEETS_CLIENT_SECRET`
- **Priority**: Checked after Service Account but before legacy OAuth2 file-based flow
- **Benefits**: Better suited for containerized environments, CI/CD pipelines, and configuration management
- **Behavior**: Constructs OAuth2 client config dynamically, still uses `TOKEN_PATH` for token persistence
- **Backward Compatible**: Legacy OAuth2 flow with `CREDENTIALS_PATH` still supported

### API Scope
The Drive API scope is set to file-level access:
- **Scope**: `https://www.googleapis.com/auth/drive.file` (only files created/opened by the app)

## Project Overview

**mcp-google-sheets** is a Python-based Model Context Protocol (MCP) server that acts as a bridge between MCP-compatible clients (like Claude Desktop) and the Google Sheets API. It enables AI assistants to interact with Google Spreadsheets through a comprehensive set of tools for automation and data manipulation.

### Key Technologies
- **Language**: Node.js 18+ with TypeScript 5.7
- **Framework**: `@modelcontextprotocol/sdk` (official MCP SDK for Node.js)
- **APIs**: Google Sheets API v4, Google Drive API v3
- **Package Manager**: `npm`
- **Authentication**: Service Accounts, OAuth 2.0 (Standard & Legacy), Application Default Credentials (ADC)
- **Distribution**: npm package (`mcp-google-sheets`)

### Architecture
The server implements the Model Context Protocol (MCP) specification, exposing:
- **Tools**: 20+ operations for spreadsheet manipulation (CRUD, batch operations, sharing, formatting)
- **Resources**: Spreadsheet metadata access via URI scheme (`spreadsheet://{id}/info`)
- **Transports**: Supports both `stdio` (default) and `sse` (Server-Sent Events) transports

### API Scopes
The server requests the following Google API scopes:
- `https://www.googleapis.com/auth/spreadsheets` - Full access to Google Sheets
- `https://www.googleapis.com/auth/drive.file` - Access to files created or opened by the app (more restrictive than full Drive access)

## Building and Running

### Prerequisites
1. **Install Node.js** (version 18 or higher):
   ```bash
   # Check version
   node --version
   
   # Install via package manager or download from https://nodejs.org/
   ```

2. **Google Cloud Setup** (Required):
   - Create a GCP project
   - Enable Google Sheets API and Google Drive API
   - Configure credentials (Service Account recommended)
   - See README.md for detailed authentication setup

### Running the Server

#### Quick Start (Using npx - Recommended for Users)
```bash
# Set environment variables first
export SERVICE_ACCOUNT_PATH="/path/to/service-account-key.json"
export DRIVE_FOLDER_ID="your_drive_folder_id"

# Run latest version from npm
npx mcp-google-sheets@latest
```

#### Development Mode (From Source)
```bash
# Clone and navigate to the project
cd /home/filipp/blackbox/mcp-google-sheets

# Install dependencies
npm install

# Set environment variables
export SERVICE_ACCOUNT_PATH="/path/to/service-account-key.json"
export DRIVE_FOLDER_ID="your_drive_folder_id"

# Run the server
npm start

# Or run directly
node dist/index.js
```

#### Docker Deployment
```bash
# Build the image
docker build -t mcp-google-sheets .

# Run with SSE transport (port 8000)
docker run --rm -p 8000:8000 \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e CREDENTIALS_CONFIG=<base64_encoded_credentials> \
  -e DRIVE_FOLDER_ID=<folder_id> \
  mcp-google-sheets
```

### Building the Package
```bash
# Install dependencies
npm install

# Build TypeScript to JavaScript
npm run build

# Output: dist/*.js, dist/*.d.ts, and source maps
```

### Testing
Currently, no automated test suite is present in the repository. Testing is done manually through:
1. Running the server with a test client
2. Executing tool calls via Claude Desktop or other MCP clients
3. Verifying operations in Google Sheets

## Development Conventions

### Code Style
- **Language**: TypeScript with strict mode enabled
- **Module System**: ES2022 modules (`import`/`export`)
- **Type Safety**: Full TypeScript type annotations
- **Async/Await**: All async operations use async/await pattern
- **Error Handling**: Try-catch blocks with McpError for protocol errors
- **Logging**: Uses `console.error()` for logging (stdout reserved for MCP protocol)

### Module-Level Constants
```typescript
const SCOPES = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive.file'
];

const OAUTH2_AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth';
const OAUTH2_TOKEN_URL = 'https://oauth2.googleapis.com/token';

// Environment variables accessed via process.env
const credentialsConfig = process.env.CREDENTIALS_CONFIG;
const tokenPath = process.env.TOKEN_PATH || 'token.json';
const credentialsPath = process.env.CREDENTIALS_PATH || 'credentials.json';
const serviceAccountPath = process.env.SERVICE_ACCOUNT_PATH;
const driveFolderId = process.env.DRIVE_FOLDER_ID;
const clientId = process.env.GOOGLE_SHEETS_CLIENT_ID;
const clientSecret = process.env.GOOGLE_SHEETS_CLIENT_SECRET;
```

### Project Structure
```
mcp-google-sheets/
├── src/
│   ├── index.ts             # Main entry point and server initialization
│   ├── auth.ts              # Authentication module (all auth methods)
│   ├── tools.ts             # Tool implementations
│   └── resources.ts         # Resource implementations
├── dist/                    # Compiled JavaScript output
├── package.json             # Project metadata and dependencies
├── package-lock.json        # Locked dependencies
├── tsconfig.json            # TypeScript configuration
├── Dockerfile               # Multi-stage Docker build
└── README.md                # Comprehensive documentation
```

### Key Design Patterns

#### 1. Server Initialization
The server uses a straightforward initialization pattern:
```typescript
async function initializeServices() {
  const auth = await authenticateGoogle();
  
  sheetsService = google.sheets({ version: 'v4', auth });
  driveService = google.drive({ version: 'v3', auth });
  folderIdContext = process.env.DRIVE_FOLDER_ID;
}

// Called before server starts
await initializeServices();

// Services accessed via getServices() function
export function getServices() {
  return { sheetsService, driveService, folderIdContext };
}
```

The initialization function handles all authentication methods and builds the Google Sheets and Drive services that are then available to all tools.

#### 2. Authentication Priority
The server checks credentials in this order:
1. `CREDENTIALS_CONFIG` (Base64-encoded JSON) - Service Account credentials
2. `SERVICE_ACCOUNT_PATH` (Service Account file path)
3. `GOOGLE_SHEETS_CLIENT_ID` + `GOOGLE_SHEETS_CLIENT_SECRET` (OAuth 2.0 Standard flow) - **NEW**
4. `CREDENTIALS_PATH` + `TOKEN_PATH` (OAuth 2.0 Legacy flow with credentials file)
5. Application Default Credentials (ADC) - automatic fallback

**OAuth 2.0 Standard Flow (New Method):**
- Uses environment variables for client credentials instead of a JSON file
- More suitable for containerized environments and CI/CD pipelines
- Constructs OAuth2 client config dynamically from `GOOGLE_SHEETS_CLIENT_ID` and `GOOGLE_SHEETS_CLIENT_SECRET`
- Still uses `TOKEN_PATH` to persist refresh tokens between sessions
- Triggers interactive browser login on first use or when token expires
- Automatically refreshes expired tokens using the refresh token

**OAuth 2.0 Legacy Flow:**
- Uses `CREDENTIALS_PATH` pointing to a downloaded credentials.json file
- Maintained for backward compatibility with existing setups
- Same token refresh behavior as the standard flow

#### 3. Tool Definitions
Tools are registered using request handlers:
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get_sheet_data',
        description: 'Get data from a specific sheet',
        inputSchema: { /* JSON Schema */ }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case 'get_sheet_data':
      return await getSheetDataHandler(args);
    // ... other tools
  }
});
```

#### 4. Resource URIs
Resources are registered with URI pattern matching:
```typescript
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  
  // Parse URI: spreadsheet://{spreadsheet_id}/info
  const match = uri.match(/^spreadsheet:\/\/([^\/]+)\/info$/);
  const spreadsheetId = match[1];
  
  return await getSpreadsheetInfo(spreadsheetId, uri);
});
```

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SERVICE_ACCOUNT_PATH` | Path to Service Account JSON key | `service_account.json` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google's standard ADC variable | - |
| `DRIVE_FOLDER_ID` | Default Google Drive folder for operations | Empty string |
| `GOOGLE_SHEETS_CLIENT_ID` | OAuth2 Client ID (Standard flow) | - |
| `GOOGLE_SHEETS_CLIENT_SECRET` | OAuth2 Client Secret (Standard flow) | - |
| `CREDENTIALS_PATH` | Path to OAuth 2.0 credentials file (Legacy) | `credentials.json` |
| `TOKEN_PATH` | Path to store OAuth token | `token.json` |
| `CREDENTIALS_CONFIG` | Base64-encoded credentials (for containers) | - |
| `HOST` / `FASTMCP_HOST` | Server host for SSE transport | `0.0.0.0` |
| `PORT` / `FASTMCP_PORT` | Server port for SSE transport | `8000` |

### Available Tools (20+)

**Spreadsheet Operations:**
- `list_spreadsheets` - List spreadsheets in folder
- `create_spreadsheet` - Create new spreadsheet
- `get_spreadsheet_info` - Get metadata (resource)

**Sheet Operations:**
- `list_sheets` - List all sheets in spreadsheet
- `create_sheet` - Add new sheet tab
- `copy_sheet` - Copy sheet between spreadsheets
- `rename_sheet` - Rename existing sheet

**Data Operations:**
- `get_sheet_data` - Read data from range
- `get_sheet_formulas` - Read formulas from range
- `update_cells` - Write data to range
- `batch_update_cells` - Update multiple ranges
- `add_rows` - Insert rows
- `add_columns` - Insert columns

**Batch Operations:**
- `get_multiple_sheet_data` - Fetch from multiple ranges
- `get_multiple_spreadsheet_summary` - Get summaries of multiple spreadsheets

**Sharing:**
- `share_spreadsheet` - Share with users/emails with roles

**Drive Operations:**
- `list_folders` - List folders in Drive

### Authentication Implementation Details

#### OAuth 2.0 Standard Flow
The OAuth2 standard flow implementation:
1. **Environment Variables**: Uses `GOOGLE_SHEETS_CLIENT_ID` and `GOOGLE_SHEETS_CLIENT_SECRET`
2. **OAuth2Client**: Creates OAuth2Client with credentials:
   ```typescript
   const oauth2Client = new OAuth2Client({
     clientId,
     clientSecret,
     redirectUri: 'http://localhost'
   });
   ```
3. **Token Management**: 
   - Checks for existing token at `TOKEN_PATH` (default: `token.json`)
   - Refreshes expired tokens automatically by checking `expiry_date`
   - Triggers interactive browser flow if no valid token exists
   - Saves token to `TOKEN_PATH` for future use
4. **Token Refresh**: Checks `tokens.expiry_date < Date.now()` to determine if refresh is needed

#### OAuth 2.0 Legacy Flow
The legacy flow reads credentials from a JSON file and creates OAuth2Client with the file's client_id and client_secret.

#### Service Account Flow
Service accounts use `google.auth.GoogleAuth` with either:
- `keyFile`: Path to service account JSON file
- `credentials`: Parsed JSON object (for base64-encoded credentials)

### Dependencies
Core dependencies (from `package.json`):
- `@modelcontextprotocol/sdk` ^1.0.4 - Official MCP SDK for Node.js
- `googleapis` ^144.0.0 - Google APIs Node.js client
- `zod` ^3.25.1 - Schema validation (peer dependency for MCP SDK)

Dev dependencies:
- `typescript` ^5.7.2 - TypeScript compiler
- `@types/node` ^22.10.2 - Node.js type definitions

### CI/CD
- **GitHub Actions**: `.github/workflows/release.yml`
- **Trigger**: On GitHub release publication
- **Process**:
  1. Install dependencies with `npm install`
  2. Build TypeScript with `npm run build`
  3. Upload artifacts
  4. Publish to npm registry

### Versioning
- Version managed in `package.json`
- Follows semantic versioning (semver)
- Updated manually or via release tools

## Common Development Tasks

### Adding a New Tool
1. Add tool definition to `ListToolsRequestSchema` handler in `src/tools.ts`
2. Add case to switch statement in `CallToolRequestSchema` handler
3. Implement handler function with TypeScript types
4. Access services via `getServices()` from `src/index.ts`
5. Return MCP-compliant response with `content` array
6. Rebuild with `npm run build`
7. Update README.md with tool documentation

### Testing Changes Locally

#### Testing with Service Account
```bash
# Build first
npm run build

# Run server in one terminal
export SERVICE_ACCOUNT_PATH="/path/to/service-account-key.json"
export DRIVE_FOLDER_ID="your_folder_id"
node dist/index.js
```

#### Testing with OAuth2 Standard Flow
```bash
# Build first
npm run build

# Run server with OAuth2 credentials
export GOOGLE_SHEETS_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_SHEETS_CLIENT_SECRET="your-client-secret"
export TOKEN_PATH="/path/to/token.json"
node dist/index.js
# Browser will open for authentication on first run
```

#### Testing with OAuth2 Legacy Flow
```bash
# Build first
npm run build

# Run server with credentials file
export CREDENTIALS_PATH="/path/to/credentials.json"
export TOKEN_PATH="/path/to/token.json"
node dist/index.js
```

#### Configure Claude Desktop for Local Testing
Edit `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "google-sheets-local": {
      "command": "node",
      "args": ["/home/filipp/blackbox/mcp-google-sheets/dist/index.js"],
      "env": {
        "GOOGLE_SHEETS_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_SHEETS_CLIENT_SECRET": "your-client-secret",
        "TOKEN_PATH": "/path/to/token.json"
      }
    }
  }
}
```

### Debugging

#### Authentication Debugging
The server prints which authentication method it's using on startup:
- `"Using service account authentication"` - Service Account via `SERVICE_ACCOUNT_PATH`
- `"Trying OAuth2 standard flow with client credentials"` - OAuth2 with `GOOGLE_SHEETS_CLIENT_ID`/`SECRET`
- `"Trying OAuth authentication flow with credentials file"` - OAuth2 Legacy with `CREDENTIALS_PATH`
- `"Attempting to use Application Default Credentials (ADC)"` - ADC fallback
- `"Successfully authenticated using OAuth2 standard flow"` - OAuth2 standard flow succeeded
- `"Refreshing expired OAuth2 token"` - Token refresh in progress

#### Common Issues
- **Environment variables**: Verify all required variables are set correctly
- **Google Cloud APIs**: Ensure Google Sheets API and Google Drive API are enabled
- **Service Accounts**: Ensure folder is shared with service account email (from `client_email` in JSON)
- **OAuth2 Scopes**: Ensure OAuth consent screen includes required scopes:
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/drive.file`
- **Token Path**: Ensure `TOKEN_PATH` directory exists and is writable
- **Browser Access**: OAuth2 flows require browser access for initial authentication

#### Advanced Debugging
- Use `--transport sse` for HTTP-based debugging (easier to inspect with curl/Postman)
- Check token.json contents to verify refresh token is present
- Delete token.json to force re-authentication if token is corrupted

## License
MIT License - Copyright (c) 2025 Xing Wu

## Repository
- **GitHub**: https://github.com/xing5/mcp-google-sheets
- **PyPI**: https://pypi.org/project/mcp-google-sheets/
- **Author**: Xing Wu (xingwu.cs@gmail.com)
