#!/bin/bash
set -e

# 1. Detect PostgreSQL Version
VERSION=$(ls /etc/postgresql | head -n 1)
if [ -z "$VERSION" ]; then
    echo "Error: PostgreSQL not installed. Please run: sudo apt install postgresql"
    exit 1
fi
echo "Detected PostgreSQL version: $VERSION"

echo "Stopping PostgreSQL..."
sudo systemctl stop postgresql

echo "Dropping old cluster..."
sudo pg_dropcluster --stop $VERSION main || true

echo "Cleaning data directory..."
sudo rm -rf /var/lib/postgresql/$VERSION/main

echo "Creating fresh cluster..."
sudo pg_createcluster $VERSION main --start

echo "Starting PostgreSQL..."
sudo systemctl start postgresql

echo "Creating project database..."
sudo -u postgres createdb honeyword_db || echo "Database already exists"

echo "Setting database password..."
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

echo "Importing schema..."
psql -U postgres -d honeyword_db -f /home/gh0st/Documents/FUTB_project1/schema.sql

echo "--------------------------------------------------"
echo "SUCCESS! Your database is now fixed and ready."
echo "You can now start your server with: uvicorn main:app --reload"
echo "--------------------------------------------------"
