#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';

/**
 * List all Cloudflare zones (domains)
 * Usage: ./list-zones.ts
 */
async function main() {
  try {
    console.log('🌐 Listing Cloudflare zones...\n');

    const zones = await cloudflare.listZones();

    if (!zones.result || zones.result.length === 0) {
      console.log('No zones found.');
      return;
    }

    console.log(`Found ${zones.result.length} zone(s):\n`);

    zones.result.forEach((zone: any) => {
      console.log(`🌍 ${zone.name}`);
      console.log(`   ID: ${zone.id}`);
      console.log(`   Status: ${zone.status}`);
      console.log(`   Name Servers: ${zone.name_servers?.join(', ') || 'N/A'}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();