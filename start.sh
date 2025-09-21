#!/bin/bash

# Sri Lanka Tourism Chatbot Startup Script
echo "🚀 Starting Sri Lanka Tourism Chatbot..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data/mongodb
mkdir -p data/redis

# Set permissions
chmod +x start.sh
chmod +x seed.sh

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d mongodb redis

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to be ready..."
sleep 10

# Start backend
echo "🔧 Starting backend service..."
docker-compose up -d backend

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running successfully!"
    echo ""
    echo "🌐 API Documentation: http://localhost:8000/docs"
    echo "🔧 ReDoc Documentation: http://localhost:8000/redoc"
    echo "❤️  Health Check: http://localhost:8000/health"
    echo ""
    echo "📊 MongoDB: localhost:27017"
    echo "🔄 Redis: localhost:6379"
    echo ""
    echo "To seed the database with initial data, run:"
    echo "  ./seed.sh"
    echo ""
    echo "To stop all services, run:"
    echo "  docker-compose down"
else
    echo "❌ Some services failed to start. Check logs with:"
    echo "  docker-compose logs"
fi