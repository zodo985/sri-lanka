#!/bin/bash

# Sri Lanka Tourism Chatbot Database Seeding Script
echo "🌱 Seeding Sri Lanka Tourism Chatbot database..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if MongoDB is running
echo "🔍 Checking if MongoDB is running..."
if ! docker-compose ps mongodb | grep -q "Up"; then
    echo "❌ MongoDB is not running. Please start the services first with:"
    echo "  ./start.sh"
    exit 1
fi

# Run the seeding script
echo "🌱 Running database seeding..."
python3 seed_data.py

if [ $? -eq 0 ]; then
    echo "✅ Database seeding completed successfully!"
    echo ""
    echo "🎉 Your Sri Lanka Tourism Chatbot is now ready!"
    echo ""
    echo "🌐 API Documentation: http://localhost:8000/docs"
    echo "🔧 ReDoc Documentation: http://localhost:8000/redoc"
    echo "❤️  Health Check: http://localhost:8000/health"
    echo ""
    echo "📊 Sample data has been added:"
    echo "  - 5 Tourist Attractions (Sigiriya, Temple of the Tooth, Yala, Galle Fort, Nuwara Eliya)"
    echo "  - 3 Restaurants (Ministry of Crab, Upali's, Empire Cafe)"
    echo "  - 2 Accommodations (Galle Face Hotel, Jetwing Lighthouse)"
    echo "  - 4 Emergency Services (Police, Tourist Police, Hospital, Fire)"
    echo "  - 2 Cultural Events (Kandy Perahera, New Year)"
    echo "  - 7 Supported Languages (EN, SI, TA, DE, FR, ZH, JA)"
    echo ""
    echo "🚀 You can now start testing the API endpoints!"
else
    echo "❌ Database seeding failed. Please check the error messages above."
    exit 1
fi