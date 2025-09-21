// MongoDB initialization script
db = db.getSiblingDB('sri_lanka_tourism_chatbot');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "username", "full_name", "hashed_password"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        },
        username: {
          bsonType: "string",
          minLength: 3,
          maxLength: 50
        },
        full_name: {
          bsonType: "string",
          minLength: 2,
          maxLength: 100
        }
      }
    }
  }
});

db.createCollection('tourist_attractions');
db.createCollection('restaurants');
db.createCollection('accommodations');
db.createCollection('transportation');
db.createCollection('emergency_services');
db.createCollection('cultural_events');
db.createCollection('chat_sessions');
db.createCollection('messages');
db.createCollection('languages');
db.createCollection('feedback');
db.createCollection('reviews');
db.createCollection('analytics');

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "role": 1 });
db.users.createIndex({ "status": 1 });

db.tourist_attractions.createIndex({ "name": 1 });
db.tourist_attractions.createIndex({ "district": 1 });
db.tourist_attractions.createIndex({ "province": 1 });
db.tourist_attractions.createIndex({ "attraction_type": 1 });
db.tourist_attractions.createIndex({ "is_active": 1 });
db.tourist_attractions.createIndex({ "is_featured": 1 });
db.tourist_attractions.createIndex({ "location": "2dsphere" });

db.restaurants.createIndex({ "name": 1 });
db.restaurants.createIndex({ "district": 1 });
db.restaurants.createIndex({ "cuisine_types": 1 });
db.restaurants.createIndex({ "is_active": 1 });
db.restaurants.createIndex({ "location": "2dsphere" });

db.accommodations.createIndex({ "name": 1 });
db.accommodations.createIndex({ "accommodation_type": 1 });
db.accommodations.createIndex({ "district": 1 });
db.accommodations.createIndex({ "is_active": 1 });
db.accommodations.createIndex({ "location": "2dsphere" });

db.chat_sessions.createIndex({ "session_id": 1 }, { unique: true });
db.chat_sessions.createIndex({ "user_id": 1 });
db.chat_sessions.createIndex({ "is_active": 1 });
db.chat_sessions.createIndex({ "started_at": 1 });

db.messages.createIndex({ "message_id": 1 }, { unique: true });
db.messages.createIndex({ "session_id": 1 });
db.messages.createIndex({ "timestamp": 1 });
db.messages.createIndex({ "role": 1 });
db.messages.createIndex({ "intent": 1 });

db.languages.createIndex({ "code": 1 }, { unique: true });
db.languages.createIndex({ "is_active": 1 });

db.feedback.createIndex({ "feedback_id": 1 }, { unique: true });
db.feedback.createIndex({ "user_id": 1 });
db.feedback.createIndex({ "feedback_type": 1 });
db.feedback.createIndex({ "rating": 1 });
db.feedback.createIndex({ "created_at": 1 });

db.reviews.createIndex({ "review_id": 1 }, { unique: true });
db.reviews.createIndex({ "user_id": 1 });
db.reviews.createIndex({ "item_id": 1 });
db.reviews.createIndex({ "item_type": 1 });
db.reviews.createIndex({ "rating": 1 });
db.reviews.createIndex({ "is_approved": 1 });

db.analytics.createIndex({ "analytics_id": 1 }, { unique: true });
db.analytics.createIndex({ "date": 1 });
db.analytics.createIndex({ "hour": 1 });

print("Database initialization completed successfully!");