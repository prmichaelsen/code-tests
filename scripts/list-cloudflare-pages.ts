#!/usr/bin/env ts-node

import { cloudflare } from './src/cloudflare-client';

/**
 * List all Cloudflare Pages projects
 * Usage: ./list-cloudflare-pages.ts
 */
async function main() {
  try {
    console.log('📄 Listing Cloudflare Pages projects...\n');

    const projects = await cloudflare.listPagesProjects();

    if (!projects.result || projects.result.length === 0) {
      console.log('No Pages projects found.');
      return;
    }

    console.log(`Found ${projects.result.length} project(s):\n`);

    projects.result.forEach((project: any) => {
      console.log(`📦 ${project.name}`);
      console.log(`   Created: ${project.created_on}`);
      console.log(`   Production URL: ${project.domains?.[0] || 'N/A'}`);
      console.log(`   Source: ${project.source?.type || 'N/A'}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();