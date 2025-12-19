#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';

/**
 * Get Cloudflare account ID
 * Usage: ./get-account-id.ts
 */
async function main() {
  try {
    console.log('📋 Fetching Cloudflare account ID...\n');

    const accounts = await cloudflare.listAccounts();

    if (!accounts.result || accounts.result.length === 0) {
      console.log('No accounts found.');
      process.exit(1);
    }

    console.log(`Found ${accounts.result.length} account(s):\n`);

    accounts.result.forEach((account: any) => {
      console.log(`Account: ${account.name}`);
      console.log(`ID: ${account.id}`);
      console.log(`Type: ${account.type || 'N/A'}`);
      console.log('');
      console.log('Add this to your .env file:');
      console.log(`CLOUDFLARE_ACCOUNT_ID=${account.id}`);
      console.log('');
    });

  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();