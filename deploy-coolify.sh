#!/bin/bash
# FitCafe Website Deployment Script for Coolify
# This script initializes git and prepares for Coolify deployment

set -e

# Configuration
COOLIFY_URL="https://coolify.thequietself.com"
COOLIFY_API_KEY="4|coZt0OWYqoQIbUuo3fo29Yh6QRkKwxxpJU1l2pPod84e5dd0"
DOMAIN="fitcafecoffee.com"
PROJECT_NAME="FitCafe"
APP_NAME="fitcafe-website"
WORKSPACE_DIR="/home/mandhira/.openclaw/workspace-jarvis/fitcafe-website"

echo "🚀 FitCafe Deployment to Coolify"
echo "================================"

# Step 1: Initialize Git Repository
echo ""
echo "📦 Step 1: Initializing Git repository..."
cd "$WORKSPACE_DIR"

if [ ! -d ".git" ]; then
    git init
    git config user.email "deploy@fitcafe.coffee"
    git config user.name "FitCafe Deploy"
    git add .
    git commit -m "Initial commit: FitCafe sales page"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
    git add .
    git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
fi

# Step 2: Get Server UUID from Coolify
echo ""
echo "🖥️  Step 2: Fetching server information..."
SERVERS_RESPONSE=$(curl -s -X GET "$COOLIFY_URL/api/v1/servers" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json")

echo "Servers response: $SERVERS_RESPONSE"

# Extract the first server UUID (assuming we want the default Hetzner server)
SERVER_UUID=$(echo "$SERVERS_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$SERVER_UUID" ]; then
    echo "❌ Failed to get server UUID"
    exit 1
fi

echo "✅ Server UUID: $SERVER_UUID"

# Step 3: Create Project in Coolify
echo ""
echo "📁 Step 3: Creating project..."
PROJECT_RESPONSE=$(curl -s -X POST "$COOLIFY_URL/api/v1/projects" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"$PROJECT_NAME\",
        \"description\": \"FitCafe Coffee Website\"
    }")

echo "Project response: $PROJECT_RESPONSE"

# Extract project UUID
PROJECT_UUID=$(echo "$PROJECT_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PROJECT_UUID" ]; then
    echo "⚠️  Project might already exist, trying to find it..."
    # Try to get existing projects
    PROJECTS_RESPONSE=$(curl -s -X GET "$COOLIFY_URL/api/v1/projects" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" \
        -H "Accept: application/json")
    echo "Projects: $PROJECTS_RESPONSE"
    PROJECT_UUID=$(echo "$PROJECTS_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi

if [ -z "$PROJECT_UUID" ]; then
    echo "❌ Failed to get project UUID"
    exit 1
fi

echo "✅ Project UUID: $PROJECT_UUID"

# Step 4: Get Environment
echo ""
echo "🌍 Step 4: Getting environment..."
# Get environments for this project
ENVIRONMENTS_RESPONSE=$(curl -s -X GET "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/environments" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

echo "Environments: $ENVIRONMENTS_RESPONSE"

# Extract first environment UUID
ENV_UUID=$(echo "$ENVIRONMENTS_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
ENV_NAME="production"

if [ -z "$ENV_UUID" ]; then
    echo "⚠️  Using default environment name"
    ENV_UUID=""
fi

echo "✅ Environment: $ENV_NAME (UUID: $ENV_UUID)"

# Step 5: Get Destination (Docker)
echo ""
echo "🎯 Step 5: Getting destination..."
DESTINATIONS_RESPONSE=$(curl -s -X GET "$COOLIFY_URL/api/v1/servers/$SERVER_UUID/destinations" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

echo "Destinations: $DESTINATIONS_RESPONSE"

# Extract first destination UUID
DEST_UUID=$(echo "$DESTINATIONS_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$DEST_UUID" ]; then
    echo "❌ Failed to get destination UUID"
    exit 1
fi

echo "✅ Destination UUID: $DEST_UUID"

# Step 6: Create Application
echo ""
echo "🚀 Step 6: Creating application..."

# Prepare the git URL (we'll use a local path for now, but Coolify needs a git URL)
# For local deployment, we might need to push to a git provider first
# For now, let's create the app with a placeholder git URL
GIT_REPO="https://github.com/placeholder/fitcafe.git"
GIT_BRANCH="main"

APP_RESPONSE=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"project_uuid\": \"$PROJECT_UUID\",
        \"server_uuid\": \"$SERVER_UUID\",
        \"environment_name\": \"$ENV_NAME\",
        \"destination_uuid\": \"$DEST_UUID\",
        \"name\": \"$APP_NAME\",
        \"description\": \"FitCafe Static Website\",
        \"git_repository\": \"$GIT_REPO\",
        \"git_branch\": \"$GIT_BRANCH\",
        \"build_pack\": \"static\",
        \"is_static\": true,
        \"domains\": \"$DOMAIN\",
        \"base_directory\": \"/\",
        \"publish_directory\": \"/\",
        \"instant_deploy\": false
    }")

echo "Application response: $APP_RESPONSE"

# Extract app UUID
APP_UUID=$(echo "$APP_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$APP_UUID" ]; then
    echo "⚠️  Application might already exist or error occurred"
    echo "Response: $APP_RESPONSE"
    # Try to find existing app
    APPS_RESPONSE=$(curl -s -X GET "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/applications" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" \
        -H "Accept: application/json")
    echo "Existing apps: $APPS_RESPONSE"
    APP_UUID=$(echo "$APPS_RESPONSE" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi

if [ -z "$APP_UUID" ]; then
    echo "❌ Failed to create/get application"
    exit 1
fi

echo "✅ Application UUID: $APP_UUID"

# Step 7: Update Application with Local Git (if needed)
echo ""
echo "🔗 Step 7: Configuring git deployment..."

# For local git, we need to add Coolify as a remote
# Get the git deploy URL from Coolify
GIT_DEPLOY_URL=$(echo "$APP_RESPONSE" | grep -o '"git_repository":"[^"]*"' | cut -d'"' -f4)

if [ -n "$GIT_DEPLOY_URL" ] && [[ "$GIT_DEPLOY_URL" == *"coolify"* ]]; then
    echo "Setting up git remote..."
    git remote remove coolify 2>/dev/null || true
    git remote add coolify "$GIT_DEPLOY_URL"
    echo "✅ Git remote configured"
else
    echo "⚠️  Manual git setup may be required"
fi

# Step 8: Deploy
echo ""
echo "🎬 Step 8: Triggering deployment..."
DEPLOY_RESPONSE=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/deploy" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

echo "Deploy response: $DEPLOY_RESPONSE"

# Step 9: Configure Domain
echo ""
echo "🌐 Step 9: Configuring domain..."
DOMAIN_RESPONSE=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/domains" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"domain\": \"$DOMAIN\"
    }")

echo "Domain response: $DOMAIN_RESPONSE"

# Summary
echo ""
echo "================================"
echo "✅ Deployment Complete!"
echo "================================"
echo "📁 Project: $PROJECT_NAME ($PROJECT_UUID)"
echo "🚀 Application: $APP_NAME ($APP_UUID)"
echo "🌐 Domain: $DOMAIN"
echo "🔗 Coolify URL: $COOLIFY_URL"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. If using local git, push to Coolify:"
echo "   git push coolify main"
echo ""
echo "2. Or update the git repository URL in Coolify dashboard"
echo ""
echo "3. Ensure DNS for $DOMAIN points to your Hetzner server"
echo ""
echo "4. Monitor deployment in Coolify dashboard: $COOLIFY_URL"
echo ""
