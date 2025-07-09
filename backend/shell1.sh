#!/bin/bash

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version

# Navigate to the project directory
cd /mnt/persist/workspace

# Install project dependencies
npm install

# Build the project to check for any build errors
npm run build

# Check if there are any TypeScript or ESLint errors
npm run lint