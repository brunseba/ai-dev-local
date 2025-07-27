#!/usr/bin/env node
/**
 * Flowise Silent Setup Initialization Script
 * AI Dev Local - Automated Flowise Configuration
 */

const fs = require('fs');
const path = require('path');

// Configuration paths
const CONFIG_PATH = '/root/.flowise/config/flowise.json';
const DATA_DIR = '/root/.flowise';
const LOG_DIR = '/root/.flowise/logs';
const STORAGE_DIR = '/root/.flowise/storage';

/**
 * Ensure required directories exist
 */
function ensureDirectories() {
    const dirs = [DATA_DIR, LOG_DIR, STORAGE_DIR];
    dirs.forEach(dir => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
            console.log(`Created directory: ${dir}`);
        }
    });
}

/**
 * Load configuration from JSON file
 */
function loadConfig() {
    try {
        if (fs.existsSync(CONFIG_PATH)) {
            const configData = fs.readFileSync(CONFIG_PATH, 'utf8');
            return JSON.parse(configData);
        }
        console.warn('Configuration file not found, using defaults');
        return null;
    } catch (error) {
        console.error('Error loading configuration:', error.message);
        return null;
    }
}

/**
 * Set up default credentials if they don't exist
 */
function setupDefaultCredentials(config) {
    if (!config || !config.defaults || !config.defaults.credentials) {
        return;
    }

    console.log('Setting up default credentials...');
    
    // Here you would typically interact with Flowise's credential system
    // This is a placeholder for the actual implementation
    config.defaults.credentials.forEach(cred => {
        console.log(`- Configuring ${cred.name}`);
        // Implementation would depend on Flowise's internal API
    });
}

/**
 * Initialize database connection settings
 */
function initializeDatabase(config) {
    if (!config || !config.database) {
        return;
    }

    const dbConfig = config.database;
    console.log('Initializing database configuration...');
    console.log(`- Type: ${dbConfig.type}`);
    console.log(`- Host: ${dbConfig.host}:${dbConfig.port}`);
    console.log(`- Database: ${dbConfig.database}`);
    
    // Set environment variables for Flowise
    process.env.DATABASE_TYPE = dbConfig.type;
    process.env.DATABASE_HOST = dbConfig.host;
    process.env.DATABASE_PORT = dbConfig.port.toString();
    process.env.DATABASE_USER = dbConfig.username;
    process.env.DATABASE_PASSWORD = dbConfig.password;
    process.env.DATABASE_NAME = dbConfig.database;
    process.env.OVERRIDE_DATABASE = dbConfig.override.toString();
}

/**
 * Set up authentication configuration
 */
function setupAuthentication(config) {
    if (!config || !config.authentication) {
        return;
    }

    const auth = config.authentication;
    console.log('Setting up authentication...');
    
    if (auth.enabled) {
        process.env.FLOWISE_USERNAME = auth.username;
        process.env.FLOWISE_PASSWORD = auth.password;
        process.env.JWT_AUTH_TOKEN_SECRET = auth.jwtSecret;
        process.env.JWT_REFRESH_TOKEN_SECRET = auth.jwtRefreshSecret;
        process.env.JWT_TOKEN_EXPIRY_IN_MINUTES = auth.tokenExpiryMinutes.toString();
        process.env.JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES = auth.refreshTokenExpiryMinutes.toString();
        
        console.log(`- Username: ${auth.username}`);
        console.log('- Password: [CONFIGURED]');
        console.log('- JWT tokens configured');
    }
}

/**
 * Configure server settings
 */
function configureServer(config) {
    if (!config || !config.server) {
        return;
    }

    const server = config.server;
    console.log('Configuring server settings...');
    
    process.env.PORT = server.port.toString();
    process.env.CORS_ORIGINS = server.corsOrigins;
    process.env.IFRAME_ORIGINS = server.iframeOrigins;
    process.env.NUMBER_OF_PROXIES = server.numberOfProxies.toString();
    
    console.log(`- Port: ${server.port}`);
    console.log(`- CORS Origins: ${server.corsOrigins}`);
}

/**
 * Main initialization function
 */
function initialize() {
    console.log('=== Flowise Silent Setup Initialization ===');
    console.log('AI Dev Local - Automated Configuration');
    console.log('');

    // Ensure directories exist
    ensureDirectories();

    // Load configuration
    const config = loadConfig();
    if (!config) {
        console.log('No configuration found, using environment defaults');
        return;
    }

    // Initialize components
    initializeDatabase(config);
    setupAuthentication(config);
    configureServer(config);
    setupDefaultCredentials(config);

    console.log('');
    console.log('=== Initialization Complete ===');
    console.log('Flowise is ready for silent startup');
    console.log('');
}

// Run initialization if this script is executed directly
if (require.main === module) {
    initialize();
}

module.exports = { initialize };
