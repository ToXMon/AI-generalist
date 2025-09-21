# Deployment Configuration

This directory contains all deployment-related configuration files for the AI Generalist application.

## Files

- `akash-deploy.yaml` - Main Akash Network deployment configuration
- `akash-deploy-console.yaml` - Akash Console deployment configuration with enhanced features
- `providers.yaml` - Akash Network provider configuration
- `docker-compose.yml` - Local development Docker Compose configuration (located in root)
- `docker-compose.prod.yml` - Production Docker Compose configuration (located in root)

## Environment Variables Required

Before deploying, ensure the following environment variables are set:

- `VENICE_API_KEY` - API key for Venice.ai service
- `EMAIL_USER` - Email address for notifications
- `EMAIL_PASS` - Email password or app-specific password
- `EMAIL_TO` - Recipient email address for notifications

## Security Notes

- Never commit actual credentials to version control
- Use environment variables or secure secret management
- Review deployment files before pushing to ensure no sensitive data is included