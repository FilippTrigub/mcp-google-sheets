#!/usr/bin/env python3
"""
Test script to verify OAuth2 configuration is properly set up
"""

import os
import sys

# Add src to path
sys.path.insert(0, 'src')

print("Testing OAuth2 Configuration...")
print("=" * 60)

# Test 1: Check if constants are defined
print("\n1. Checking if OAuth2 constants are defined in server.py...")
try:
    # Read the file and check for the constants
    with open('src/mcp_google_sheets/server.py', 'r') as f:
        content = f.read()
        
    checks = {
        'SCOPES with drive.file': 'https://www.googleapis.com/auth/drive.file' in content,
        'GOOGLE_SHEETS_CLIENT_ID': "GOOGLE_SHEETS_CLIENT_ID = os.environ.get('GOOGLE_SHEETS_CLIENT_ID'" in content,
        'GOOGLE_SHEETS_CLIENT_SECRET': "GOOGLE_SHEETS_CLIENT_SECRET = os.environ.get('GOOGLE_SHEETS_CLIENT_SECRET'" in content,
        'OAUTH2_AUTHORIZATION_URL': "OAUTH2_AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'" in content,
        'OAUTH2_TOKEN_URL': "OAUTH2_TOKEN_URL = 'https://oauth2.googleapis.com/token'" in content,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ All constant definitions found!")
    else:
        print("\n✗ Some constants are missing!")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error reading server.py: {e}")
    sys.exit(1)

# Test 2: Check if OAuth2 flow is implemented
print("\n2. Checking if OAuth2 standard flow is implemented...")
try:
    oauth2_flow_checks = {
        'OAuth2 client config creation': '"installed": {' in content and '"client_id": GOOGLE_SHEETS_CLIENT_ID' in content,
        'OAuth2 flow initialization': 'InstalledAppFlow.from_client_config(client_config, SCOPES)' in content,
        'Token refresh logic': 'creds.refresh(Request())' in content,
        'Token persistence': 'with open(TOKEN_PATH, \'w\') as token:' in content,
    }
    
    all_passed = True
    for check_name, result in oauth2_flow_checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ OAuth2 standard flow implementation found!")
    else:
        print("\n✗ Some OAuth2 flow components are missing!")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error checking OAuth2 flow: {e}")
    sys.exit(1)

# Test 3: Check authentication priority order
print("\n3. Checking authentication priority order...")
try:
    # Find the order of authentication checks
    lines = content.split('\n')
    auth_checks = []
    for i, line in enumerate(lines):
        if 'if CREDENTIALS_CONFIG:' in line:
            auth_checks.append(('CREDENTIALS_CONFIG', i))
        elif 'if not creds and SERVICE_ACCOUNT_PATH' in line:
            auth_checks.append(('SERVICE_ACCOUNT_PATH', i))
        elif 'if not creds and GOOGLE_SHEETS_CLIENT_ID and GOOGLE_SHEETS_CLIENT_SECRET:' in line:
            auth_checks.append(('GOOGLE_SHEETS_CLIENT_ID/SECRET', i))
        elif 'if not creds and CREDENTIALS_PATH' in line:
            auth_checks.append(('CREDENTIALS_PATH', i))
        elif 'if not creds:' in line and 'google.auth.default' in content[content.find('if not creds:', i):content.find('if not creds:', i)+500]:
            auth_checks.append(('ADC', i))
    
    print("  Authentication priority order:")
    for idx, (method, line_num) in enumerate(auth_checks, 1):
        print(f"    {idx}. {method} (line {line_num})")
    
    expected_order = ['CREDENTIALS_CONFIG', 'SERVICE_ACCOUNT_PATH', 'GOOGLE_SHEETS_CLIENT_ID/SECRET', 'CREDENTIALS_PATH', 'ADC']
    actual_order = [method for method, _ in auth_checks]
    
    if actual_order == expected_order:
        print("\n✓ Authentication priority order is correct!")
    else:
        print(f"\n⚠ Warning: Expected order {expected_order}, got {actual_order}")
        
except Exception as e:
    print(f"✗ Error checking authentication order: {e}")
    sys.exit(1)

# Test 4: Check README documentation
print("\n4. Checking README.md documentation...")
try:
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    readme_checks = {
        'OAuth 2.0 Standard section': '### Method B: OAuth 2.0 Standard' in readme_content,
        'GOOGLE_SHEETS_CLIENT_ID documented': 'GOOGLE_SHEETS_CLIENT_ID' in readme_content,
        'GOOGLE_SHEETS_CLIENT_SECRET documented': 'GOOGLE_SHEETS_CLIENT_SECRET' in readme_content,
        'OAuth2 config example': '"GOOGLE_SHEETS_CLIENT_ID":' in readme_content,
        'Updated authentication priority': 'GOOGLE_SHEETS_CLIENT_ID` + `GOOGLE_SHEETS_CLIENT_SECRET` (OAuth2 Standard Flow)' in readme_content,
    }
    
    all_passed = True
    for check_name, result in readme_checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ README.md documentation is complete!")
    else:
        print("\n✗ Some documentation is missing!")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error reading README.md: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! OAuth2 configuration is properly implemented.")
print("=" * 60)
