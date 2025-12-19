#!/usr/bin/env ts-node

import { execSync } from 'child_process';
import { config } from './src/config';

/**
 * Deploy to Cloudflare Pages using wrangler
 * Usage: ./deploy-with-wrangler.ts
 */
async function main() {
  try {
    console.log('🚀 Deploying to Cloudflare Pages with Wrangler\n');

    const projectName = 'map-search-app';
    const buildDir = '../front-end/map-search-app/dist';

    // Check if wrangler is installed
    console.log('1. Checking wrangler installation...');
    try {
      execSync('npx wrangler --version', { stdio: 'pipe' });
      console.log('✓ Wrangler is available');
    } catch (error) {
      console.log('ℹ️  Wrangler not found, will use npx');
    }

    // Check if build directory exists
    console.log('\n2. Checking build directory...');
    try {
      execSync(`ls ${buildDir}`, { stdio: 'pipe' });
      console.log(`✓ Build directory exists: ${buildDir}`);
    } catch (error) {
      console.error(`❌ Build directory not found: ${buildDir}`);
      console.log('\nPlease build the app first:');
      console.log('  cd front-end/map-search-app');
      console.log('  npm run build');
      process.exit(1);
    }

    // Set environment variables for wrangler
    process.env.CLOUDFLARE_API_TOKEN = config.apiKey;
    process.env.CLOUDFLARE_ACCOUNT_ID = config.accountId;

    console.log('\n3. Deploying to Cloudflare Pages...');
    console.log(`   Project: ${projectName}`);
    console.log(`   Directory: ${buildDir}`);
    console.log('');

    // Deploy with wrangler
    const deployCommand = `npx wrangler pages deploy ${buildDir} --project-name=${projectName}`;
    
    console.log(`Running: ${deployCommand}\n`);
    
    execSync(deployCommand, {
      stdio: 'inherit',
      env: {
        ...process.env,
        CLOUDFLARE_API_TOKEN: config.apiKey,
        CLOUDFLARE_ACCOUNT_ID: config.accountId,
      },
    });

    console.log('\n✅ Deployment complete!');

  } catch (error) {
    console.error('\n❌ Deployment failed:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();