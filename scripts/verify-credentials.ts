#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';

/**
 * Verify Cloudflare API credentials
 * Usage: ./verify-credentials.ts
 */
async function main() {
  try {
    console.log('🔐 Verifying Cloudflare credentials...\n');

    const isValid = await cloudflare.verifyCredentials();

    if (isValid) {
      console.log('\n✅ Credentials are valid and working!');
      
      // Get additional account info
      const accounts = await cloudflare.listAccounts();
      console.log(`\n📊 You have access to ${accounts.result.length} account(s)`);
    } else {
      console.log('\n❌ Credentials are invalid');
      console.log('Please check your .env file:');
      console.log('  - CLOUDFLARE_API_KEY');
      console.log('  - CLOUDFLARE_EMAIL');
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();