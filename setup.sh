#!/bin/bash

# Sri Lanka Tourism Chatbot Setup Script
echo "🎯 Setting up Sri Lanka Tourism Chatbot..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x start.sh
chmod +x seed.sh
chmod +x setup.sh

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data/mongodb
mkdir -p data/redis
mkdir -p rasa

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "   Please update the .env file with your API keys and configuration."
fi

# Pull required Docker images
echo "🐳 Pulling Docker images..."
docker-compose pull

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Update the .env file with your API keys (optional for basic functionality)"
echo "2. Start the services: ./start.sh"
echo "3. Seed the database: ./seed.sh"
echo "4. Access the API documentation: http://localhost:8000/docs"
echo ""
echo "📚 For more information, see README.md"