
<div align="center">
  <b>mcp-google-sheets</b>

  <p align="center">
    <i>Your AI Assistant's Gateway to Google Sheets! </i>📊
  </p>

[![npm version](https://img.shields.io/npm/v/mcp-google-sheets)](https://www.npmjs.com/package/mcp-google-sheets)
[![License](https://img.shields.io/github/license/xing5/mcp-google-sheets)](LICENSE)
</div>

---

## 🤔 What is this?

`mcp-google-sheets` is a **Node.js/TypeScript** MCP server that acts as a bridge between any MCP-compatible client (like Claude Desktop) and the Google Sheets API. It allows you to interact with your Google Spreadsheets using a defined set of tools, enabling powerful automation and data manipulation workflows driven by AI.

## 🚀 Quick Start with OAuth 2.0

The easiest way to get started is using **OAuth 2.0 with environment variables** - no credential files needed!

### 1. Prerequisites

- **Node.js 18+** installed ([download here](https://nodejs.org/))
- A Google Cloud Platform account

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**

4. **Create OAuth 2.0 Credentials:**
   - Navigate to **APIs & Services** → **Credentials**
   - Click **+ CREATE CREDENTIALS** → **OAuth client ID**
   - Choose **Desktop app** as the application type
   - Name it (e.g., "MCP Google Sheets")
   - Click **CREATE**
   - **Copy the Client ID and Client Secret** (you'll need these!)

5. **Configure OAuth Consent Screen:**
   - Go to **APIs & Services** → **OAuth consent screen**
   - Select **External** (unless you have a Google Workspace)
   - Fill in the required information
   - Add the following scopes:
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.file`
   - Add your email as a test user

### 3. Install and Run

```bash
# Install globally
npm install -g mcp-google-sheets

# Or run directly with npx (no installation needed)
npx mcp-google-sheets
```

### 4. Set Environment Variables

Set your OAuth credentials as environment variables:

**Linux/macOS:**
```bash
export GOOGLE_SHEETS_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_SHEETS_CLIENT_SECRET="your-client-secret"
export TOKEN_PATH="$HOME/.mcp-google-sheets-token.json"
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_SHEETS_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
$env:GOOGLE_SHEETS_CLIENT_SECRET = "your-client-secret"
$env:TOKEN_PATH = "$env:USERPROFILE\.mcp-google-sheets-token.json"
```

**Windows (CMD):**
```cmd
set GOOGLE_SHEETS_CLIENT_ID=your-client-id.apps.googleusercontent.com
set GOOGLE_SHEETS_CLIENT_SECRET=your-client-secret
set TOKEN_PATH=%USERPROFILE%\.mcp-google-sheets-token.json
```

### 5. First Run (Interactive Authentication)

On the first run, a browser window will open for you to authenticate:

```bash
npx mcp-google-sheets
```

1. A browser will open automatically
2. Sign in with your Google account
3. Grant the requested permissions
4. The token will be saved to `TOKEN_PATH` for future use

After the first authentication, the server will use the saved token automatically!

---

## 🔌 Usage with Claude Desktop

Add this configuration to your Claude Desktop config file:

**Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["mcp-google-sheets"],
      "env": {
        "GOOGLE_SHEETS_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_SHEETS_CLIENT_SECRET": "your-client-secret",
        "TOKEN_PATH": "/full/path/to/token.json"
      }
    }
  }
}
```

**macOS Note:** If you get a `spawn npx ENOENT` error, use the full path:
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "/usr/local/bin/npx",
      "args": ["mcp-google-sheets"],
      "env": {
        "GOOGLE_SHEETS_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_SHEETS_CLIENT_SECRET": "your-client-secret",
        "TOKEN_PATH": "/Users/yourusername/.mcp-google-sheets-token.json"
      }
    }
  }
}
```

---

## 🔑 Alternative Authentication Methods

### Method A: OAuth 2.0 with Direct Token Injection (For Gemini CLI / Database-backed) 🚀

**Pros:**
- No token files needed
- Perfect for database-backed OAuth flows
- Automatic token refresh
- Ideal for Gemini CLI integration

**Setup:**

Set these environment variables with tokens from your database:

```bash
export GOOGLE_SHEETS_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_SHEETS_CLIENT_SECRET="your-client-secret"
export GOOGLE_SHEETS_ACCESS_TOKEN="ya29.a0AfB_byD..."
export GOOGLE_SHEETS_REFRESH_TOKEN="1//0gH..."  # Optional but recommended
export GOOGLE_SHEETS_TOKEN_EXPIRY="2025-11-25T10:34:45.248Z"  # ISO 8601 format
```

The server will use these tokens directly without needing any files!

**For Gemini CLI users:** See [GEMINI_CLI_SETUP.md](GEMINI_CLI_SETUP.md) for detailed integration guide.

### Method B: OAuth 2.0 with Environment Variables (Interactive) ✅

**Pros:**
- No credential files to manage
- Easy to configure in CI/CD
- Secure token storage
- Works great for personal use

**Setup:** See [Quick Start](#-quick-start-with-oauth-20) above

### Method C: Service Account (For Server/Automation) 🤖

**Pros:**
- No interactive authentication needed
- Great for headless servers
- Can be used in Docker containers

**Setup:**

1. In Google Cloud Console → **IAM & Admin** → **Service Accounts**
2. Click **+ CREATE SERVICE ACCOUNT**
3. Name it and grant necessary roles
4. Click **Keys** → **Add Key** → **Create new key** → **JSON**
5. Download the JSON key file

**Environment Variables:**
```bash
export SERVICE_ACCOUNT_PATH="/path/to/service-account-key.json"
export DRIVE_FOLDER_ID="your-google-drive-folder-id"  # Optional
```

**Important:** Share your Google Drive folder with the service account email (found in the JSON file as `client_email`)

### Method D: OAuth 2.0 with Credentials File (Legacy) 📄

**Setup:**

1. Download OAuth credentials JSON from Google Cloud Console
2. Save as `credentials.json`

**Environment Variables:**
```bash
export CREDENTIALS_PATH="/path/to/credentials.json"
export TOKEN_PATH="/path/to/token.json"
```

### Method E: Application Default Credentials (ADC) 🌐

**For Google Cloud environments (GKE, Cloud Run, etc.)**

```bash
# Local development
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/drive.file

# Or set the standard Google variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

---

## 🛠️ Available Tools

The server provides these tools for Claude (or any MCP client):

### Spreadsheet Operations
- **`list_spreadsheets`** - List all accessible spreadsheets
- **`create_spreadsheet`** - Create a new spreadsheet
- **`get_sheet_data`** - Read data from a sheet
- **`update_cells`** - Update cell values
- **`batch_update_cells`** - Update multiple ranges at once

### Sheet Management
- **`list_sheets`** - List all sheets in a spreadsheet
- **`create_sheet`** - Add a new sheet tab
- **`share_spreadsheet`** - Share with users via email

### Resources
- **`spreadsheet://{id}/info`** - Get spreadsheet metadata

---

## 💬 Example Prompts for Claude

Once connected, try these prompts:

- "List all my spreadsheets"
- "Create a new spreadsheet called 'Q4 Budget 2024'"
- "Get the data from Sheet1 in my Budget spreadsheet"
- "Update cell A1 in Sheet1 to 'Total Revenue'"
- "Share my Budget spreadsheet with john@example.com as a viewer"
- "Create a new sheet called 'Summary' in my Budget spreadsheet"

---

## 🔧 Development

### Clone and Build

```bash
# Clone the repository
git clone https://github.com/xing5/mcp-google-sheets.git
cd mcp-google-sheets

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run locally
node dist/index.js
```

### Project Structure

```
mcp-google-sheets/
├── src/
│   ├── index.ts       # Main server entry point
│   ├── auth.ts        # Authentication logic
│   ├── tools.ts       # Tool implementations
│   └── resources.ts   # Resource handlers
├── dist/              # Compiled JavaScript
├── package.json
├── tsconfig.json
└── README.md
```

### Testing Locally with Claude Desktop

```json
{
  "mcpServers": {
    "google-sheets-dev": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-google-sheets/dist/index.js"],
      "env": {
        "GOOGLE_SHEETS_CLIENT_ID": "your-client-id",
        "GOOGLE_SHEETS_CLIENT_SECRET": "your-client-secret",
        "TOKEN_PATH": "/path/to/token.json"
      }
    }
  }
}
```

---

## 🐳 Docker Support

```bash
# Build
docker build -t mcp-google-sheets .

# Run with OAuth (requires pre-authenticated token)
docker run -p 8000:8000 \
  -e GOOGLE_SHEETS_CLIENT_ID="your-client-id" \
  -e GOOGLE_SHEETS_CLIENT_SECRET="your-secret" \
  -v /path/to/token.json:/app/token.json \
  -e TOKEN_PATH=/app/token.json \
  mcp-google-sheets

# Run with Service Account
docker run -p 8000:8000 \
  -e SERVICE_ACCOUNT_PATH=/app/service-account.json \
  -v /path/to/service-account.json:/app/service-account.json \
  mcp-google-sheets
```

---

## 🔒 Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Restrict OAuth scopes** to only what you need
4. **Use Service Accounts** for production/automation
5. **Regularly rotate** service account keys
6. **Store tokens securely** with appropriate file permissions

---

## 🐛 Troubleshooting

### "All authentication methods failed"

**Solution:** Ensure you've set the required environment variables:
```bash
# Check if variables are set
echo $GOOGLE_SHEETS_CLIENT_ID
echo $GOOGLE_SHEETS_CLIENT_SECRET
echo $TOKEN_PATH
```

### "OAuth token not found"

**Solution:** Run the server interactively first to authenticate:
```bash
npx mcp-google-sheets
```
A browser will open for authentication.

### "spawn npx ENOENT" (macOS)

**Solution:** Use the full path to npx in Claude Desktop config:
```bash
which npx  # Find the full path
```

### Token expired

**Solution:** The server automatically refreshes tokens. If issues persist, delete the token file and re-authenticate:
```bash
rm ~/.mcp-google-sheets-token.json
npx mcp-google-sheets  # Re-authenticate
```

---

## 📝 Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GOOGLE_SHEETS_CLIENT_ID` | For OAuth | OAuth 2.0 Client ID | - |
| `GOOGLE_SHEETS_CLIENT_SECRET` | For OAuth | OAuth 2.0 Client Secret | - |
| `GOOGLE_SHEETS_ACCESS_TOKEN` | For Direct Token | OAuth access token from DB | - |
| `GOOGLE_SHEETS_REFRESH_TOKEN` | For Direct Token | OAuth refresh token (optional) | - |
| `GOOGLE_SHEETS_TOKEN_EXPIRY` | For Direct Token | Token expiry (ISO 8601) | - |
| `TOKEN_PATH` | For File-based OAuth | Path to store OAuth token | `token.json` |
| `SERVICE_ACCOUNT_PATH` | For Service Account | Path to service account JSON | - |
| `DRIVE_FOLDER_ID` | Optional | Default Google Drive folder | - |
| `CREDENTIALS_PATH` | For Legacy OAuth | Path to credentials.json | `credentials.json` |
| `GOOGLE_APPLICATION_CREDENTIALS` | For ADC | Google's standard ADC variable | - |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Credits

- Built with [@modelcontextprotocol/sdk](https://github.com/modelcontextprotocol/typescript-sdk)
- Uses [googleapis](https://github.com/googleapis/google-api-nodejs-client)
- Inspired by [kazz187/mcp-google-spreadsheet](https://github.com/kazz187/mcp-google-spreadsheet)

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/xing5/mcp-google-sheets/issues)
- **Discussions:** [GitHub Discussions](https://github.com/xing5/mcp-google-sheets/discussions)

---

<div align="center">
  Made with ❤️ for the MCP community
</div>
