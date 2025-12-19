import { cloudflare } from './cloudflare-client';

/**
 * Main entry point for Cloudflare API scripts
 */
async function main() {
  try {
    console.log('🚀 Cloudflare API Client\n');

    // Verify credentials
    console.log('Verifying credentials...');
    const isValid = await cloudflare.verifyCredentials();
    
    if (!isValid) {
      console.error('\n❌ Invalid credentials. Please check your .env file.');
      process.exit(1);
    }

    console.log('\n✅ Ready to use Cloudflare API');
    console.log('\nAvailable operations:');
    console.log('  - List zones (domains)');
    console.log('  - List Pages projects');
    console.log('  - List deployments');
    console.log('  - Create deployments');
    console.log('  - And more...\n');

    // Example: List accounts
    console.log('Fetching accounts...');
    const accounts = await cloudflare.listAccounts();
    console.log(`Found ${accounts.result.length} account(s):`);
    accounts.result.forEach((account: any) => {
      console.log(`  - ${account.name} (${account.id})`);
    });

    // Example: List zones if available
    console.log('\nFetching zones...');
    const zones = await cloudflare.listZones();
    if (zones.result.length > 0) {
      console.log(`Found ${zones.result.length} zone(s):`);
      zones.result.forEach((zone: any) => {
        console.log(`  - ${zone.name} (${zone.id})`);
      });
    } else {
      console.log('No zones found.');
    }

  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

// Run main function
main();