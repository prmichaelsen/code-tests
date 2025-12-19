#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';
import { config } from './src/config';

/**
 * Check Cloudflare Pages deployment status and guide setup
 * Usage: ./deploy-pages.ts
 */
async function main() {
  try {
    console.log('🚀 Cloudflare Pages Deployment Helper\n');

    // Verify credentials
    console.log('1. Verifying credentials...');
    const isValid = await cloudflare.verifyCredentials();
    if (!isValid) {
      console.error('❌ Invalid credentials');
      process.exit(1);
    }

    if (!config.accountId) {
      console.error('\n❌ CLOUDFLARE_ACCOUNT_ID is required');
      console.log('Run: ./get-account-id.ts to get your account ID');
      process.exit(1);
    }

    // Check existing Pages projects
    console.log('\n2. Checking existing Pages projects...');
    const projects = await cloudflare.listPagesProjects();
    
    const projectName = 'map-search-app';
    const existingProject = projects.result?.find((p: any) => p.name === projectName);

    if (existingProject) {
      console.log(`\n✅ Project "${projectName}" exists!`);
      console.log(`   Production URL: ${existingProject.domains?.[0] || 'N/A'}`);
      console.log(`   Created: ${existingProject.created_on}`);
      
      // List recent deployments
      console.log('\n3. Checking recent deployments...');
      const deployments = await cloudflare.listPagesDeployments(projectName);
      
      if (deployments.result && deployments.result.length > 0) {
        console.log(`\n   Latest deployments:`);
        deployments.result.slice(0, 3).forEach((dep: any, i: number) => {
          console.log(`   ${i + 1}. ${dep.url}`);
          console.log(`      Status: ${dep.latest_stage?.status || 'N/A'}`);
          console.log(`      Created: ${dep.created_on}`);
        });
      }
      
      console.log('\n📝 To deploy updates:');
      console.log('   git add -A');
      console.log('   git commit -m "your message"');
      console.log('   git push origin main');
      
    } else {
      console.log(`\nℹ️  Project "${projectName}" not found`);
      console.log('\n📝 To create and deploy:');
      console.log('\n   Option 1: Via Cloudflare Dashboard (Recommended)');
      console.log('   1. Go to https://dash.cloudflare.com/');
      console.log('   2. Navigate to Workers & Pages → Create');
      console.log('   3. Select "Pages" → "Connect to Git"');
      console.log('   4. Connect your repository');
      console.log('   5. Configure build:');
      console.log('      - Framework: Vite');
      console.log('      - Build command: npm run build');
      console.log('      - Build output: dist');
      console.log('      - Root directory: front-end/map-search-app');
      console.log('   6. Add environment variable:');
      console.log('      VITE_GOOGLE_MAPS_API_KEY=AIzaSyDm0IM8x2P9vzh3VkcYtv14DHHkGmz7nvY');
      console.log('\n   Option 2: Direct Upload (requires wrangler)');
      console.log('   npm install -g wrangler');
      console.log('   cd front-end/map-search-app');
      console.log('   npm run build');
      console.log('   wrangler pages deploy dist --project-name=map-search-app');
    }

    console.log('\n✅ Deployment check complete!');

  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();