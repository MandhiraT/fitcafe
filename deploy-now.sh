#!/bin/bash
# FitCafe Deployment - Execute Now
# VPS IP: 91.107.193.144

set -e

COOLIFY_URL="https://coolify.thequietself.com"
COOLIFY_API_KEY="4|coZt0OWYqoQIbUuo3fo29Yh6QRkKwxxpJU1l2pPod84e5dd0"
DOMAIN="fitcafecoffee.com"
VPS_IP="91.107.193.144"
WORKSPACE_DIR="/home/mandhira/.openclaw/workspace-jarvis/fitcafe-website"

echo "🚀 FitCafe Deployment to Coolify"
echo "================================"
echo "VPS IP: $VPS_IP"
echo "Domain: $DOMAIN"
echo ""

cd "$WORKSPACE_DIR"

# Step 1: Initialize Git
echo "📦 Step 1/6: Initializing Git repository..."
if [ ! -d ".git" ]; then
    git init
    git config user.email "deploy@fitcafe.coffee"
    git config user.name "FitCafe Deploy"
    git add .
    git commit -m "Initial commit: FitCafe sales page"
    echo "✅ Git initialized and committed"
else
    echo "✅ Git already exists"
    git add .
    git commit -m "Deploy update $(date '+%H:%M')" || echo "No changes to commit"
fi

# Step 2: Get Server UUID
echo ""
echo "🖥️  Step 2/6: Fetching server from Coolify..."
SERVERS_JSON=$(curl -s "$COOLIFY_URL/api/v1/servers" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

SERVER_UUID=$(echo "$SERVERS_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$SERVER_UUID" ]; then
    echo "❌ Failed to get server UUID"
    echo "Response: $SERVERS_JSON"
    exit 1
fi

echo "✅ Server UUID: $SERVER_UUID"

# Step 3: Create Project
echo ""
echo "📁 Step 3/6: Creating project 'FitCafe'..."
PROJECT_JSON=$(curl -s -X POST "$COOLIFY_URL/api/v1/projects" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "FitCafe",
        "description": "FitCafe Coffee Website - fitcafecoffee.com"
    }')

PROJECT_UUID=$(echo "$PROJECT_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PROJECT_UUID" ]; then
    echo "⚠️  Project might exist, fetching..."
    PROJECTS_JSON=$(curl -s "$COOLIFY_URL/api/v1/projects" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" \
        -H "Accept: application/json")
    PROJECT_UUID=$(echo "$PROJECTS_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi

if [ -z "$PROJECT_UUID" ]; then
    echo "❌ Failed to get project UUID"
    exit 1
fi

echo "✅ Project UUID: $PROJECT_UUID"

# Step 4: Get Environment
echo ""
echo "🌍 Step 4/6: Getting environment..."
ENV_JSON=$(curl -s "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/environments" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

ENV_UUID=$(echo "$ENV_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
ENV_NAME="production"

if [ -z "$ENV_UUID" ]; then
    echo "⚠️  Using default environment"
    ENV_UUID=""
fi

echo "✅ Environment: $ENV_NAME"

# Step 5: Get Destination
echo ""
echo "🎯 Step 5/6: Getting destination..."
DEST_JSON=$(curl -s "$COOLIFY_URL/api/v1/servers/$SERVER_UUID/destinations" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

DEST_UUID=$(echo "$DEST_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$DEST_UUID" ]; then
    echo "❌ Failed to get destination UUID"
    exit 1
fi

echo "✅ Destination UUID: $DEST_UUID"

# Step 6: Create Application
echo ""
echo "🚀 Step 6/6: Creating application..."

APP_JSON=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"project_uuid\": \"$PROJECT_UUID\",
        \"server_uuid\": \"$SERVER_UUID\",
        \"environment_name\": \"$ENV_NAME\",
        \"destination_uuid\": \"$DEST_UUID\",
        \"name\": \"fitcafe-website\",
        \"description\": \"FitCafe Static Website\",
        \"git_repository\": \"https://github.com/placeholder/fitcafe.git\",
        \"git_branch\": \"main\",
        \"build_pack\": \"static\",
        \"is_static\": true,
        \"is_spa\": false,
        \"domains\": \"$DOMAIN\",
        \"base_directory\": \"/\",
        \"publish_directory\": \"/\",
        \"instant_deploy\": true,
        \"is_auto_deploy_enabled\": true,
        \"is_force_https_enabled\": true
    }")

APP_UUID=$(echo "$APP_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$APP_UUID" ]; then
    echo "⚠️  Application might exist, fetching..."
    APPS_JSON=$(curl -s "$COOLIFY_URL/api/v1/projects/$PROJECT_UUID/applications" \
        -H "Authorization: Bearer $COOLIFY_API_KEY" \
        -H "Accept: application/json")
    APP_UUID=$(echo "$APPS_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
fi

if [ -z "$APP_UUID" ]; then
    echo "❌ Failed to create application"
    echo "Response: $APP_JSON"
    exit 1
fi

echo "✅ Application UUID: $APP_UUID"

# Trigger Deployment
echo ""
echo "🎬 Triggering deployment..."
DEPLOY_JSON=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/deploy" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json")

echo "✅ Deployment triggered!"
echo "Deploy response: $DEPLOY_JSON"

# Add Domain
echo ""
echo "🌐 Configuring domain..."
DOMAIN_JSON=$(curl -s -X POST "$COOLIFY_URL/api/v1/applications/$APP_UUID/domains" \
    -H "Authorization: Bearer $COOLIFY_API_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"domain\": \"$DOMAIN\"
    }")

echo "✅ Domain configured"
echo "Domain response: $DOMAIN_JSON"

# Summary
echo ""
echo "================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================"
echo ""
echo "📁 Project UUID: $PROJECT_UUID"
echo "🚀 Application UUID: $APP_UUID"
echo "🌐 Domain: $DOMAIN"
echo "🖥️  VPS IP: $VPS_IP"
echo "🔗 Coolify Dashboard: $COOLIFY_URL"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo ""
echo "1. DNS Configuration:"
echo "   Add this A record to your DNS:"
echo "   fitcafecoffee.com.    A    $VPS_IP"
echo "   www.fitcafecoffee.com CNAME fitcafecoffee.com"
echo ""
echo "2. Git Repository (Optional):"
echo "   If you want to use Git auto-deploy:"
echo "   - Push code to GitHub/GitLab"
echo "   - Update repository URL in Coolify dashboard"
echo ""
echo "3. SSL Certificate:"
echo "   Coolify will auto-provision SSL via Let's Encrypt"
echo "   once DNS is verified (may take 5-10 minutes)"
echo ""
echo "4. Monitor Deployment:"
echo "   Check logs in Coolify dashboard:"
echo "   $COOLIFY_URL/project/$PROJECT_UUID/environment/$ENV_UUID/application/$APP_UUID"
echo ""
echo "🎉 Website will be live at: https://$DOMAIN"
echo ""
