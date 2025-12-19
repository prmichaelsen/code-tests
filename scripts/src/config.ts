import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

interface CloudflareConfig {
  apiKey: string;
  email: string;
  accountId?: string;
  zoneId?: string;
}

const getConfig = (): CloudflareConfig => {
  const apiKey = process.env.CLOUDFLARE_API_KEY;
  const email = process.env.CLOUDFLARE_EMAIL;

  if (!apiKey || !email) {
    throw new Error(
      'Missing required environment variables: CLOUDFLARE_API_KEY and CLOUDFLARE_EMAIL must be set in .env file'
    );
  }

  return {
    apiKey,
    email,
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID,
    zoneId: process.env.CLOUDFLARE_ZONE_ID,
  };
};

export const config = getConfig();