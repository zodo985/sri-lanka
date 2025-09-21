# Sri Lanka Tourism Multilingual Chatbot

A comprehensive AI-powered multilingual chatbot for Sri Lanka Tourism that supports Sinhala, Tamil, English, German, French, Chinese, and Japanese languages.

## 🌟 Features

### Core Features
- **Multilingual Support**: Sinhala, Tamil, English, German, French, Chinese, Japanese
- **AI-Powered Chatbot**: Natural language processing and conversation management
- **Tourism Information**: Comprehensive database of attractions, restaurants, accommodations
- **Real-time Translation**: Automatic language detection and translation
- **Voice Support**: Speech-to-text and text-to-speech capabilities
- **Image Recognition**: Landmark identification from photos
- **Personalized Recommendations**: AI-powered suggestions based on user preferences

### Tourism Services
- **Tourist Attractions**: Historical sites, natural wonders, cultural landmarks
- **Restaurants**: Local cuisine, international dining, food recommendations
- **Accommodations**: Hotels, resorts, guesthouses, hostels
- **Transportation**: Buses, trains, taxis, tuk-tuks, rental cars
- **Emergency Services**: Police, hospitals, tourist police, embassies
- **Cultural Events**: Festivals, ceremonies, celebrations

### Advanced Features
- **Itinerary Planning**: Automated trip planning and optimization
- **Weather Integration**: Real-time weather information
- **Currency Conversion**: Live exchange rates
- **Cultural Etiquette**: Local customs and traditions guide
- **Emergency Assistance**: Quick access to emergency contacts
- **Social Features**: User reviews, ratings, and recommendations

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for flexible data storage
- **Beanie**: MongoDB ODM for Python
- **Redis**: Caching and session management
- **Rasa**: Open-source conversational AI framework
- **Docker**: Containerization for easy deployment

### API Endpoints
- **Authentication**: User registration, login, JWT tokens
- **Chat**: Real-time conversation management
- **Tourism**: Attractions, restaurants, accommodations
- **Recommendations**: AI-powered personalized suggestions
- **Feedback**: User reviews and ratings
- **Admin**: Management and analytics

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sri-lanka-tourism-chatbot
```

### 2. Start the Services
```bash
# Make scripts executable
chmod +x start.sh seed.sh

# Start all services
./start.sh
```

### 3. Seed the Database
```bash
# Add initial data
./seed.sh
```

### 4. Access the Application
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Chat Endpoints
- `POST /api/v1/chat/sessions` - Create chat session
- `GET /api/v1/chat/sessions/{session_id}` - Get chat session
- `POST /api/v1/chat/sessions/{session_id}/messages` - Send message
- `POST /api/v1/chat/sessions/{session_id}/voice` - Process voice message
- `GET /api/v1/chat/sessions/{session_id}/messages` - Get messages
- `PUT /api/v1/chat/sessions/{session_id}/end` - End chat session

### Tourism Endpoints
- `GET /api/v1/tourism/attractions` - Get tourist attractions
- `GET /api/v1/tourism/attractions/{id}` - Get specific attraction
- `GET /api/v1/tourism/restaurants` - Get restaurants
- `GET /api/v1/tourism/accommodations` - Get accommodations
- `GET /api/v1/tourism/transportation` - Get transportation options
- `GET /api/v1/tourism/emergency-services` - Get emergency services
- `GET /api/v1/tourism/cultural-events` - Get cultural events
- `GET /api/v1/tourism/featured` - Get featured content

### Recommendation Endpoints
- `GET /api/v1/recommendations/attractions` - Get attraction recommendations
- `GET /api/v1/recommendations/restaurants` - Get restaurant recommendations
- `GET /api/v1/recommendations/accommodations` - Get accommodation recommendations
- `GET /api/v1/recommendations/personalized` - Get personalized recommendations

### Feedback Endpoints
- `POST /api/v1/feedback/submit` - Submit feedback
- `GET /api/v1/feedback/my-feedback` - Get user feedback
- `POST /api/v1/feedback/review` - Submit review
- `GET /api/v1/feedback/reviews/{item_id}` - Get item reviews
- `POST /api/v1/feedback/review/{review_id}/vote` - Vote on review

## 🗄️ Database Schema

### Core Collections
- **users**: User accounts and profiles
- **user_preferences**: User settings and preferences
- **chat_sessions**: Chat conversation sessions
- **messages**: Individual chat messages
- **voice_messages**: Voice message processing

### Tourism Collections
- **tourist_attractions**: Tourist destinations and landmarks
- **restaurants**: Dining establishments
- **accommodations**: Hotels and lodging
- **transportation**: Transport options
- **emergency_services**: Emergency contacts
- **cultural_events**: Festivals and events

### Content Collections
- **languages**: Supported languages
- **translations**: Translation cache
- **image_recognitions**: Image analysis results
- **content_templates**: Response templates
- **faqs**: Frequently asked questions

### Analytics Collections
- **feedback**: User feedback and ratings
- **reviews**: Detailed reviews
- **analytics**: Usage statistics
- **user_behavior**: User interaction tracking
- **system_metrics**: Performance metrics

## 🔧 Configuration

### Environment Variables
```bash
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sri_lanka_tourism_chatbot

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
CURRENCY_LAYER_API_KEY=your_currency_layer_api_key

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### API Testing
Use the interactive API documentation at http://localhost:8000/docs to test endpoints.

## 📊 Monitoring

### Health Checks
- **Application**: http://localhost:8000/health
- **Database**: Check MongoDB connection
- **Cache**: Check Redis connection

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs mongodb
docker-compose logs redis
```

## 🚀 Deployment

### Production Deployment
1. Update environment variables for production
2. Use production-grade MongoDB and Redis instances
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure monitoring and logging

### Docker Deployment
```bash
# Build production image
docker build -t sri-lanka-tourism-chatbot .

# Run with production settings
docker run -d -p 8000:8000 \
  -e MONGODB_URL=your_production_mongodb_url \
  -e REDIS_URL=your_production_redis_url \
  sri-lanka-tourism-chatbot
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the logs for error details

## 🔮 Future Enhancements

- **Mobile App**: Flutter mobile application
- **Advanced AI**: GPT integration for better conversations
- **Real-time Features**: WebSocket support for live chat
- **Analytics Dashboard**: Comprehensive analytics and reporting
- **Multi-tenant Support**: Support for multiple tourism boards
- **Offline Mode**: Local data storage for offline access
- **AR Integration**: Augmented reality features
- **Social Integration**: Social media sharing and login

---

**Built with ❤️ for Sri Lanka Tourism**