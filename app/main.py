from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
import os
import re

app = FastAPI(title="Restaurant Recommendation System",
             description="A mood-based restaurant recommendation system",
             version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to safely handle NaN values for string columns
def safe_str(value):
    if pd.isna(value) or value is None or value == '':
        return None
    return str(value)

# Load the models and data
try:
    # Check if model files exist
    if not os.path.exists('model/reason_data.pkl'):
        print("Reason data file not found. Running train_model.py...")
        import subprocess
        subprocess.run(['python', 'model/train_model.py'], check=True)
    
    with open('model/reason_data.pkl', 'rb') as f:
        reason_data = pickle.load(f)
    
    with open('model/example_moods.pkl', 'rb') as f:
        example_moods = pickle.load(f)
        
    vectorizer = joblib.load('model/vectorizer.joblib')
    restaurant_data = pd.read_pickle('model/restaurant_data.pkl')
    
    # Get reason vectors from the loaded data
    reason_vectors = reason_data['reason_vectors']
    reason_to_food_mapping = reason_data['reason_to_food_mapping']
    
    # Ensure numeric columns are properly handled
    restaurant_data['Dinner Ratings'] = pd.to_numeric(restaurant_data['Dinner Ratings'], errors='coerce').fillna(0)
    restaurant_data['Delivery Ratings'] = pd.to_numeric(restaurant_data['Delivery Ratings'], errors='coerce').fillna(0)
    restaurant_data['AverageCost'] = pd.to_numeric(restaurant_data['AverageCost'], errors='coerce').fillna(0)
    
    # Convert string columns properly
    restaurant_data['PopularDishes'] = restaurant_data['PopularDishes'].fillna('').astype(str)
    restaurant_data['PopularDishes'] = restaurant_data['PopularDishes'].replace('nan', '')
    restaurant_data['KnownFor'] = restaurant_data['KnownFor'].fillna('').astype(str)
    restaurant_data['KnownFor'] = restaurant_data['KnownFor'].replace('nan', '')
    
    # Convert boolean columns to proper booleans
    restaurant_data['IsHomeDelivery'] = restaurant_data['IsHomeDelivery'].astype(bool)
    restaurant_data['isTakeaway'] = restaurant_data['isTakeaway'].astype(bool)
    restaurant_data['isIndoorSeating'] = restaurant_data['isIndoorSeating'].astype(bool)
    
    # Flag to indicate models loaded successfully
    models_loaded = True
    
except Exception as e:
    print(f"Error loading models: {str(e)}")
    reason_data = {}
    example_moods = ["happy", "sad", "stressed", "hungry", "tired"]
    restaurant_data = pd.DataFrame()
    reason_vectors = None
    reason_to_food_mapping = {}
    models_loaded = False

class MoodRequest(BaseModel):
    mood: str
    location: Optional[str] = None
    price_range: Optional[str] = None

class Restaurant(BaseModel):
    name: str
    cuisines: str
    area: str
    address: str
    dinner_rating: float
    delivery_rating: float
    popular_dishes: Optional[str] = None
    known_for: Optional[str] = None
    average_cost: float
    home_delivery: bool
    takeaway: bool
    indoor_seating: bool

@app.get("/moods")
async def get_available_moods():
    return {"moods": example_moods}

@app.post("/recommend")
async def get_recommendations(request: MoodRequest):
    if not models_loaded:
        raise HTTPException(status_code=500, detail="Model data not loaded properly")
    
    # Vectorize the user's mood
    try:
        mood_vector = vectorizer.transform([request.mood])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process mood: {str(e)}")
    
    # Calculate similarity with all reason vectors
    similarities = cosine_similarity(mood_vector, reason_vectors)[0]
    
    # Get top 5 most similar reasons
    top_indices = similarities.argsort()[-5:][::-1]
    
    # Get recommended cuisines from the associated comfort foods
    recommended_cuisines = []
    for idx in top_indices:
        if int(idx) in reason_to_food_mapping:
            recommended_cuisines.extend(reason_to_food_mapping[int(idx)])
    
    # Remove duplicates
    recommended_cuisines = list(set(recommended_cuisines))
    
    if not recommended_cuisines:
        raise HTTPException(status_code=404, detail="No food matches found for your mood")
    
    # Escape special regex characters in food names
    escaped_cuisines = [re.escape(cuisine) for cuisine in recommended_cuisines]
    
    # Filter restaurants - use regex with word boundaries to avoid partial matches
    pattern = '|'.join(escaped_cuisines)
    mask = restaurant_data['Cuisines'].str.contains(pattern, case=False, na=False, regex=True)
    
    if request.location:
        mask &= restaurant_data['Area'].str.contains(request.location, case=False, na=False)
    
    if request.price_range:
        if request.price_range == "low":
            mask &= restaurant_data['AverageCost'] <= 500
        elif request.price_range == "medium":
            mask &= (restaurant_data['AverageCost'] > 500) & (restaurant_data['AverageCost'] <= 1500)
        else:
            mask &= restaurant_data['AverageCost'] > 1500
    
    recommended_restaurants = restaurant_data[mask].head(5)
    
    if recommended_restaurants.empty:
        raise HTTPException(status_code=404, detail="No restaurants found matching the criteria")
    
    results = []
    for _, row in recommended_restaurants.iterrows():
        # Make sure to handle empty strings for optional fields
        popular_dishes = row['PopularDishes'] if row['PopularDishes'] and row['PopularDishes'] != 'nan' else None
        known_for = row['KnownFor'] if row['KnownFor'] and row['KnownFor'] != 'nan' else None
        
        results.append(
            Restaurant(
                name=row['Name'],
                cuisines=row['Cuisines'],
                area=row['Area'],
                address=row['Full_Address'],
                dinner_rating=float(row['Dinner Ratings']),
                delivery_rating=float(row['Delivery Ratings']),
                popular_dishes=popular_dishes,
                known_for=known_for,
                average_cost=float(row['AverageCost']),
                home_delivery=bool(row['IsHomeDelivery']),
                takeaway=bool(row['isTakeaway']),
                indoor_seating=bool(row['isIndoorSeating'])
            )
        )
    
    return results

app.mount("/", StaticFiles(directory="static", html=True), name="static")