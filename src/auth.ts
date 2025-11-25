/**
 * Authentication module for Google Sheets MCP Server
 * Supports multiple authentication methods:
 * 1. Service Account (via file or base64 config)
 * 2. OAuth2 Standard (with client ID/secret)
 * 3. OAuth2 Legacy (with credentials file)
 * 4. Application Default Credentials (ADC)
 */

import { google } from 'googleapis';
import { OAuth2Client, GoogleAuth } from 'google-auth-library';
import { readFile, writeFile } from 'fs/promises';
import { existsSync } from 'fs';

const SCOPES = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive.file'
];

const OAUTH2_AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth';
const OAUTH2_TOKEN_URL = 'https://oauth2.googleapis.com/token';

/**
 * Authenticate with Google APIs using various methods
 * Priority order:
 * 1. CREDENTIALS_CONFIG (base64 encoded service account)
 * 2. SERVICE_ACCOUNT_PATH (service account file)
 * 3. GOOGLE_SHEETS_CLIENT_ID + GOOGLE_SHEETS_CLIENT_SECRET (OAuth2 standard)
 * 4. CREDENTIALS_PATH (OAuth2 legacy with credentials file)
 * 5. Application Default Credentials (ADC)
 */
export async function authenticateGoogle(): Promise<any> {
  // Method 1: Base64 encoded credentials config
  const credentialsConfig = process.env.CREDENTIALS_CONFIG;
  if (credentialsConfig) {
    try {
      const decoded = Buffer.from(credentialsConfig, 'base64').toString('utf-8');
      const credentials = JSON.parse(decoded);
      
      const auth = new google.auth.GoogleAuth({
        credentials,
        scopes: SCOPES
      });
      
      console.error('Using base64 encoded credentials configuration');
      return auth;
    } catch (error) {
      console.error('Error using CREDENTIALS_CONFIG:', error);
    }
  }

  // Method 2: Service Account file path
  const serviceAccountPath = process.env.SERVICE_ACCOUNT_PATH;
  if (serviceAccountPath && existsSync(serviceAccountPath)) {
    try {
      const auth = new google.auth.GoogleAuth({
        keyFile: serviceAccountPath,
        scopes: SCOPES
      });
      
      console.error('Using service account authentication');
      const folderIdMsg = process.env.DRIVE_FOLDER_ID 
        ? `Working with Google Drive folder ID: ${process.env.DRIVE_FOLDER_ID}`
        : 'No DRIVE_FOLDER_ID specified';
      console.error(folderIdMsg);
      
      return auth;
    } catch (error) {
      console.error('Error using service account authentication:', error);
    }
  }

  // Method 3: OAuth2 with Direct Token (from environment variables)
  const accessToken = process.env.GOOGLE_SHEETS_ACCESS_TOKEN;
  const refreshToken = process.env.GOOGLE_SHEETS_REFRESH_TOKEN;
  const clientId = process.env.GOOGLE_SHEETS_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_SHEETS_CLIENT_SECRET;
  const expiryDate = process.env.GOOGLE_SHEETS_TOKEN_EXPIRY;

  if (accessToken && clientId && clientSecret) {
    console.error('Trying OAuth2 with direct token from environment variables');
    try {
      const oauth2Client = new OAuth2Client({
        clientId,
        clientSecret,
        redirectUri: 'http://localhost'
      });

      // Set credentials directly from environment variables
      const credentials: any = {
        access_token: accessToken,
        token_type: 'Bearer',
        scope: SCOPES.join(' ')
      };

      if (refreshToken) {
        credentials.refresh_token = refreshToken;
      }

      if (expiryDate) {
        credentials.expiry_date = new Date(expiryDate).getTime();
      }

      oauth2Client.setCredentials(credentials);

      // Check if token is expired and refresh if we have a refresh token
      if (expiryDate && refreshToken) {
        const expiry = new Date(expiryDate).getTime();
        if (expiry < Date.now()) {
          console.error('Token expired, refreshing...');
          const { credentials: newCredentials } = await oauth2Client.refreshAccessToken();
          oauth2Client.setCredentials(newCredentials);
          
          // Log new token info for updating in DB
          console.error('New access token obtained. Update your database with:');
          console.error(JSON.stringify({
            accessToken: newCredentials.access_token,
            expiresAt: new Date(newCredentials.expiry_date || 0).toISOString(),
            refreshToken: newCredentials.refresh_token || refreshToken
          }, null, 2));
        }
      }

      console.error('Successfully authenticated using OAuth2 with direct token');
      return oauth2Client;
    } catch (error) {
      console.error('Error with OAuth2 direct token:', error);
    }
  }

  // Method 4: OAuth2 Standard Flow with Token File (fallback for backward compatibility)
  const tokenPath = process.env.TOKEN_PATH || 'token.json';

  if (clientId && clientSecret && existsSync(tokenPath)) {
    console.error('Trying OAuth2 standard flow with token file');
    try {
      const oauth2Client = new OAuth2Client({
        clientId,
        clientSecret,
        redirectUri: 'http://localhost'
      });

      const tokenData = await readFile(tokenPath, 'utf-8');
      const tokens = JSON.parse(tokenData);
      oauth2Client.setCredentials(tokens);

      // Refresh if expired (check expiry_date)
      const tokenExpiryDate = tokens.expiry_date;
      if (tokenExpiryDate && tokenExpiryDate < Date.now()) {
        console.error('Refreshing expired OAuth2 token');
        const { credentials } = await oauth2Client.refreshAccessToken();
        oauth2Client.setCredentials(credentials);
        await writeFile(tokenPath, JSON.stringify(credentials));
      }

      console.error('Successfully authenticated using OAuth2 standard flow');
      return oauth2Client;
    } catch (error) {
      console.error('Error with OAuth2 standard flow:', error);
    }
  }

  // Method 5: OAuth2 Legacy Flow (credentials file)
  const credentialsPath = process.env.CREDENTIALS_PATH || 'credentials.json';
  if (existsSync(credentialsPath)) {
    console.error('Trying OAuth authentication flow with credentials file');
    try {
      const credentialsData = await readFile(credentialsPath, 'utf-8');
      const credentials = JSON.parse(credentialsData);
      
      const { client_id, client_secret, redirect_uris } = 
        credentials.installed || credentials.web;

      const oauth2Client = new OAuth2Client({
        clientId: client_id,
        clientSecret: client_secret,
        redirectUri: redirect_uris[0]
      });

      // Check for existing token
      if (existsSync(tokenPath)) {
        const tokenData = await readFile(tokenPath, 'utf-8');
        const tokens = JSON.parse(tokenData);
        oauth2Client.setCredentials(tokens);

        // Refresh if expired (check expiry_date)
        const expiryDate = tokens.expiry_date;
        if (expiryDate && expiryDate < Date.now()) {
          const { credentials: newCredentials } = await oauth2Client.refreshAccessToken();
          oauth2Client.setCredentials(newCredentials);
          await writeFile(tokenPath, JSON.stringify(newCredentials));
        }

        console.error('Successfully authenticated using OAuth flow');
        return oauth2Client;
      } else {
        throw new Error(
          'OAuth2 token not found. Interactive authentication is required. ' +
          'Please run the server interactively first to authenticate via browser.'
        );
      }
    } catch (error) {
      console.error('Error with OAuth flow:', error);
    }
  }

  // Method 6: Application Default Credentials
  try {
    console.error('Attempting to use Application Default Credentials (ADC)');
    console.error('ADC will check: GOOGLE_APPLICATION_CREDENTIALS, gcloud auth, and metadata service');
    
    const auth = await google.auth.getClient({
      scopes: SCOPES
    });
    
    console.error('Successfully authenticated using ADC');
    return auth;
  } catch (error) {
    console.error('Error using Application Default Credentials:', error);
  }

  throw new Error('All authentication methods failed. Please configure credentials.');
}
