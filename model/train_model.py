import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import joblib
import os

def preprocess_data():
    # Load restaurant data
    res_data = pd.read_csv('Zomato.csv')[['Name', 'Cuisines', 'Area', 'Full_Address', 
                                         'Dinner Ratings', 'Delivery Ratings', 'PopularDishes',
                                         'KnownFor', 'AverageCost', 'IsHomeDelivery', 
                                         'isTakeaway', 'isIndoorSeating']]
    
    # Convert ratings to numeric
    res_data['Dinner Ratings'] = pd.to_numeric(res_data['Dinner Ratings'], errors='coerce')
    res_data['Delivery Ratings'] = pd.to_numeric(res_data['Delivery Ratings'], errors='coerce')
    res_data['AverageCost'] = pd.to_numeric(res_data['AverageCost'], errors='coerce')
    
    # Fill missing values properly
    res_data['Dinner Ratings'] = res_data['Dinner Ratings'].fillna(0)
    res_data['Delivery Ratings'] = res_data['Delivery Ratings'].fillna(0)
    res_data['AverageCost'] = res_data['AverageCost'].fillna(0)
    
    # Ensure all string columns are properly handled
    res_data['PopularDishes'] = res_data['PopularDishes'].fillna('').astype(str)
    res_data['PopularDishes'] = res_data['PopularDishes'].replace('nan', '')
    res_data['KnownFor'] = res_data['KnownFor'].fillna('').astype(str)
    res_data['KnownFor'] = res_data['KnownFor'].replace('nan', '')
    
    # Convert boolean columns to proper booleans
    res_data['IsHomeDelivery'] = res_data['IsHomeDelivery'].astype(bool)
    res_data['isTakeaway'] = res_data['isTakeaway'].astype(bool)
    res_data['isIndoorSeating'] = res_data['isIndoorSeating'].astype(bool)
    
    # Load food choices data
    food_data = pd.read_csv('food_choices.csv')[['comfort_food_reasons', 'comfort_food']]
    food_data['comfort_food_reasons'] = food_data['comfort_food_reasons'].fillna('')
    food_data['comfort_food'] = food_data['comfort_food'].fillna('')
    
    return res_data, food_data

def prepare_vector_model(food_data):
    # Vectorize comfort food reasons
    vectorizer = TfidfVectorizer(stop_words='english')
    reason_vectors = vectorizer.fit_transform(food_data['comfort_food_reasons'])
    
    # Create a dictionary mapping reason indices to associated foods
    reason_to_food_mapping = {}
    for idx, (_, row) in enumerate(food_data.iterrows()):
        if pd.notna(row['comfort_food']) and row['comfort_food'] != '':
            foods = [food.strip() for food in str(row['comfort_food']).split(',') if food.strip()]
            if foods:  # Only add if there are actual foods
                reason_to_food_mapping[idx] = foods
    
    # Save the reason vectors for later similarity matching
    # We'll use this directly in the API to match user moods with reasons
    reason_data = {
        'reason_vectors': reason_vectors,
        'reason_to_food_mapping': reason_to_food_mapping
    }
    
    # Also save example moods for the frontend to use as suggestions
    example_moods = ["happy", "sad", "stressed", "hungry", "tired", "bored", "lonely"]
    
    return reason_data, vectorizer, example_moods

def train_model():
    print("Starting model training...")
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Preprocess data
    res_data, food_data = preprocess_data()
    print(f"Loaded restaurant data with {len(res_data)} entries")
    print(f"Loaded food choices data with {len(food_data)} entries")
    
    # Prepare vector model
    reason_data, vectorizer, example_moods = prepare_vector_model(food_data)
    print(f"Created reason vectors with {len(reason_data['reason_to_food_mapping'])} mappings")
    
    # Save the preprocessed data and models
    print("Saving model files...")
    with open('model/reason_data.pkl', 'wb') as f:
        pickle.dump(reason_data, f)
    
    with open('model/example_moods.pkl', 'wb') as f:
        pickle.dump(example_moods, f)
    
    joblib.dump(vectorizer, 'model/vectorizer.joblib')
    res_data.to_pickle('model/restaurant_data.pkl')
    
    print("Model training completed successfully!")
    return {
        'status': 'success',
        'message': 'Model trained and saved successfully'
    }

if __name__ == '__main__':
    train_model() 