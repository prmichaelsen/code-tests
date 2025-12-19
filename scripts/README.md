# Cloudflare API Scripts

Executable TypeScript scripts for interacting with Cloudflare APIs using ts-node.

## Setup

### 1. Install Dependencies

```bash
cd scripts
npm install
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your Cloudflare credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
CLOUDFLARE_API_KEY=your_api_key_here
CLOUDFLARE_EMAIL=your_email_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here  # Optional
CLOUDFLARE_ZONE_ID=your_zone_id_here        # Optional
```

### 3. Get Your Cloudflare API Key

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Go to **My Profile** → **API Tokens**
3. Under **API Keys**, click **View** next to "Global API Key"
4. Enter your password to reveal the key
5. Copy the key to your `.env` file

## Available Scripts

All scripts are executable TypeScript files that can be run directly with ts-node.

### Verify Credentials

```bash
./verify-credentials.ts
```

Verifies your Cloudflare API credentials and shows account information.

### List Zones (Domains)

```bash
./list-zones.ts
```

Lists all domains (zones) in your Cloudflare account with their status and name servers.

### List Pages Projects

```bash
./list-cloudflare-pages.ts
```

Lists all Cloudflare Pages projects with their URLs and deployment information.

## Creating New Scripts

To create a new executable script:

1. Create a new `.ts` file in the `scripts/` directory
2. Add the shebang at the top: `#!/usr/bin/env ts-node`
3. Import the client: `import { cloudflare } from './src/cloudflare-client';`
4. Write your script logic
5. Make it executable: `chmod +x your-script.ts`
6. Run it: `./your-script.ts`

### Example Script Template

```typescript
#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';

/**
 * Description of what this script does
 * Usage: ./my-script.ts
 */
async function main() {
  try {
    console.log('🚀 Starting...\n');

    // Your code here
    const result = await cloudflare.listZones();
    console.log(result);

  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
```

## Project Structure

```
scripts/
├── src/
│   ├── config.ts              # Environment configuration
│   ├── cloudflare-client.ts   # Cloudflare API client
│   └── index.ts               # Shared utilities (optional)
├── verify-credentials.ts      # Executable: Verify API credentials
├── list-zones.ts              # Executable: List domains
├── list-cloudflare-pages.ts  # Executable: List Pages projects
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
└── README.md                  # This file
```

## Cloudflare API Client

The `CloudflareClient` class (`src/cloudflare-client.ts`) provides methods for:

### Authentication
- `verifyCredentials()` - Verify API credentials

### Accounts
- `listAccounts()` - List all accounts
- `getAccount()` - Get account details

### Zones (Domains)
- `listZones()` - List all zones
- `getZone(zoneId)` - Get zone details

### Cloudflare Pages
- `listPagesProjects()` - List all Pages projects
- `getPagesProject(projectName)` - Get project details
- `listPagesDeployments(projectName)` - List deployments
- `createPagesDeployment(projectName, data)` - Create new deployment

### Generic HTTP Methods
- `get(endpoint, config?)` - GET request
- `post(endpoint, data?, config?)` - POST request
- `put(endpoint, data?, config?)` - PUT request
- `patch(endpoint, data?, config?)` - PATCH request
- `delete(endpoint, config?)` - DELETE request

## Troubleshooting

### "Missing required environment variables"

Make sure you've created a `.env` file with your Cloudflare credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

### "Invalid credentials"

1. Verify your API key is correct
2. Verify your email matches the Cloudflare account
3. Check if the API key has the necessary permissions

### "CLOUDFLARE_ACCOUNT_ID is required"

Some operations (like Pages) require an Account ID. Add it to your `.env` file:

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
```

### "Permission denied" when running scripts

Make sure the scripts are executable:

```bash
chmod +x *.ts
```

## Security Notes

- ⚠️ **Never commit `.env` file to version control**
- ⚠️ **Keep your API keys secure**
- ⚠️ **Use API Tokens instead of Global API Key when possible**
- ⚠️ **Restrict API Token permissions to minimum required**

## Resources

- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Cloudflare Pages API](https://developers.cloudflare.com/api/operations/pages-project-get-projects)
- [API Tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)

## License

MIT