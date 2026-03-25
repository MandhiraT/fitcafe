#!/bin/bash
# Simple FitCafe Deployment - Step by Step
# Run this script to deploy to Coolify

set -e

COOLIFY_URL="https://coolify.thequietself.com"
COOLIFY_API_KEY="4|coZt0OWYqoQIbUuo3fo29Yh6QRkKwxxpJU1l2pPod84e5dd0"
DOMAIN="fitcafecoffee.com"
WORKSPACE_DIR="/home/mandhira/.openclaw/workspace-jarvis/fitcafe-website"

echo "🚀 Starting FitCafe Deployment..."
cd "$WORKSPACE_DIR"

# Step 1: Git Init
echo "📦 Step 1/6: Initializing Git..."
if [ ! -d ".git" ]; then
    git init
    git config user.email "deploy@fitcafe.coffee"
    git config user.name "FitCafe Deploy"
    git add .
    git commit -m "Initial commit: FitCafe website"
    echo "✅ Git initialized"
else
    echo "✅ Git already exists"
    git add .
    git commit -m "Update $(date '+%H:%M')" || echo "No changes"
fi

# Step 2: Get Server
echo "🖥️  Step 2/6: Getting server..."
SERVER_UUID=$(curl -s "$COOLIFY_URL/api/v1/servers" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" | \
    grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "✅ Server: $SERVER_UUID"

# Step 3: Create Project
echo "📁 Step 3/6: Creating project..."
PROJECT_DATA=$(curl -s -X POST "$COOLIFY_URL/api/v1/projects" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{"name":"FitCafe","description":"FitCafe Coffee Website"}')
PROJECT_UUID=$(echo "$PROJECT_DATA" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PROJECT_UUID" ]; then
    PROJECT_UUID=$(curl -s "$COOLIFY_URL/api/v1/projects" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" | \
        grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi
echo "✅ Project: $PROJECT_UUID"

# Step 4: Get Environment & Destination
echo "🌍 Step 4/6: Getting environment and destination..."
ENV_UUID=$(curl -s "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/environments" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" | \
    grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
DEST_UUID=$(curl -s "$COOLIFY_URL/api/v1/servers/$SERVER_UUID/destinations" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" | \
    grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "✅ Environment: $ENV_UUID, Destination: $DEST_UUID"

# Step 5: Create Application
echo "🚀 Step 5/6: Creating application..."
APP_DATA=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"project_uuid\": \"$PROJECT_UUID\",
        \"server_uuid\": \"$SERVER_UUID\",
        \"environment_name\": \"production\",
        \"destination_uuid\": \"$DEST_UUID\",
        \"name\": \"fitcafe-website\",
        \"description\": \"FitCafe Static Website\",
        \"git_repository\": \"https://github.com/placeholder/fitcafe.git\",
        \"git_branch\": \"main\",
        \"build_pack\": \"static\",
        \"is_static\": true,
        \"domains\": \"$DOMAIN\",
        \"base_directory\": \"/\",
        \"publish_directory\": \"/\",
        \"instant_deploy\": false
    }")
APP_UUID=$(echo "$APP_DATA" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$APP_UUID" ]; then
    APP_UUID=$(curl -s "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/applications" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" | \
        grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi
echo "✅ Application: $APP_UUID"

# Step 6: Deploy
echo "🎬 Step 6/6: Deploying..."
curl -s -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/deploy" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json"
echo "✅ Deployment triggered!"

echo ""
echo "================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================"
echo "Project UUID: $PROJECT_UUID"
echo "App UUID: $APP_UUID"
echo "Domain: $DOMAIN"
echo "Coolify: $COOLIFY_URL"
echo ""
echo "⚠️  Next: Update git repo URL in Coolify dashboard or push to remote"
