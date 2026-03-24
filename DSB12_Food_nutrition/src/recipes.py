import pickle
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os
import random
import re

class RecipePredictor:
    def __init__(self, model_path: str = '../data/best_recipe_classifier.pkl'):
        if not os.path.exists(model_path):
            raise ValueError(f"Model file not found at {model_path}.")
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        cols_path = '../data/ingredient_columns.csv'
        if os.path.exists(cols_path):
            col_df = pd.read_csv(cols_path, header=None)
            self.feature_names = col_df[0].tolist()
        else:
            raise ValueError(f"Ingredient columns file not found at {cols_path}.")

    def _prepare_input(self, ingredients: List[str]) -> pd.DataFrame:
        input_dict = {col: [0] for col in self.feature_names}
        clean_ingredients = [ing.strip().lower() for ing in ingredients]
        
        for ing in clean_ingredients:
            if ing in input_dict:
                input_dict[ing][0] = 1
        
        return pd.DataFrame(input_dict)

    def predict(self, ingredients: List[str]) -> str:
        if not ingredients:
            return "No ingredients provided."
            
        X = self._prepare_input(ingredients)
        prediction = self.model.predict(X)[0]
        
        if prediction == 'bad':
            return ("You might find it tasty, but in our opinion, it is a bad idea to have a\n"
                    "dish with that list of ingredients.")
        elif prediction == 'so-so':
            return ("It's an okay combination. You might find it tasty, but it's just a\n"
                    "so-so idea for a dish.")
        else:
            return ("Great choice! This combination of ingredients is likely to make a\n"
                    "delicious dish.")

class NutritionFacts:
    def __init__(self, nutrition_csv_path: str = '../data/nutrition_facts.csv'):
        if not os.path.exists(nutrition_csv_path):
            raise ValueError(f"Nutrition file not found at {nutrition_csv_path}.")
        
        self.df = pd.read_csv(nutrition_csv_path)
        self.df['ingredient'] = self.df['ingredient'].str.lower().str.strip()
        self.df.set_index('ingredient', inplace=True)

    def get_nutrition(self, ingredients: List[str]) -> List[Dict]:
        results = []
        clean_ingredients = [ing.strip().lower() for ing in ingredients]
        
        for ing in clean_ingredients:
            if ing in self.df.index:
                row = self.df.loc[ing]
                results.append({
                    'ingredient': ing.capitalize(),
                    'protein_pct': float(row['protein_pct']),
                    'calories_pct': float(row['calories_pct']),
                    'fat_pct': float(row['fat_pct']),
                    'sodium_pct': float(row['sodium_pct'])
                })
        return results

class SimilarRecipes:
    def __init__(self, recipes_csv_path: str = '../data/similar_recipes.csv', data_csv_path: str = '../data/epi_r.csv'):
        if not os.path.exists(recipes_csv_path):
            raise ValueError(f"Recipes file not found at {recipes_csv_path}.")
        if not os.path.exists(data_csv_path):
            raise ValueError(f"Data file not found at {data_csv_path}.")
        
        self.recipes_df = pd.read_csv(recipes_csv_path)
        self.full_data = pd.read_csv(data_csv_path, low_memory=False)
        
        self.full_data['title_clean'] = self.full_data['title'].str.lower().str.strip()
        self.recipes_df['title_clean'] = self.recipes_df['recipe_name'].str.lower().str.strip()

    def _get_recipe_ingredients(self, title: str) -> set:
        match = self.full_data[self.full_data['title_clean'] == title.lower().strip()]
        if match.empty:
            return set()
        
        row = match.iloc[0]
        ingredients = set()
        exclude_cols = ['rating', 'calories', 'fat', 'sodium', 'protein', 'title', 'title_clean', 'leftovers', 
                        'california', 'dominican republic', 'low cholesterol', 'pan-fry', 'fruit', 'stew', 'braise']
        
        for col in match.columns:
            if col not in exclude_cols:
                if row[col] == 1.0:
                    ingredients.add(col.lower())
        return ingredients

    def find_similar(self, user_ingredients: List[str], top_k: int = 3) -> List[Dict]:
        user_set = set([ing.strip().lower() for ing in user_ingredients])
        if not user_set:
            return []
            
        scores = []
        for idx, row in self.recipes_df.iterrows():
            title = row['title_clean']
            recipe_ings = self._get_recipe_ingredients(title)
            
            if not recipe_ings:
                continue
                
            intersection = user_set.intersection(recipe_ings)
            score = len(intersection)
            
            if score > 0:
                scores.append({
                    'score': score,
                    'recipe_name': row['recipe_name'],
                    'rating': row['rating'],
                    'url': row['url']
                })
        
        scores.sort(key=lambda x: (x['score'], x['rating']), reverse=True)
        return scores[:top_k]

class DailyMenuGenerator:
    def __init__(self, data_csv_path: str = '../data/epi_r.csv', nutrition_csv_path: str = '../data/nutrition_facts.csv'):
        if not os.path.exists(data_csv_path):
            raise ValueError(f"Data file not found at {data_csv_path}.")
        if not os.path.exists(nutrition_csv_path):
            raise ValueError(f"Nutrition file not found at {nutrition_csv_path}.")

        self.df = pd.read_csv(data_csv_path, low_memory=False)
        self.nutrition_df = pd.read_csv(nutrition_csv_path)
        
        self.nutrition_df['ingredient'] = self.nutrition_df['ingredient'].str.lower().str.strip()
        self.nutrition_dict = self.nutrition_df.set_index('ingredient')[['protein_pct', 'fat_pct', 'sodium_pct', 'calories_pct']].T.to_dict('list')
        
        self.ing_cols = [col for col in self.df.columns if col not in ['rating', 'title', 'calories', 'protein', 'fat', 'sodium']]
        
        self.breakfast_keys = {'egg', 'oat', 'pancake', 'waffle', 'cereal', 'yogurt', 'toast', 'bacon', 'sausage', 'coffee', 'juice', 'milk/cream', 'muffin', 'crepe', 'honey', 'jam'}
        self.dinner_keys = {'steak', 'chicken', 'beef', 'pork', 'lamb', 'fish', 'salmon', 'shrimp', 'lobster', 'crab', 'roast', 'braise', 'stew', 'rib'}
        self.lunch_keys = {'soup', 'salad', 'sandwich', 'wrap', 'burger', 'pasta', 'noodle', 'rice'}

    def _get_recipe_ingredients(self, row) -> List[str]:
        ings = []
        for col in self.ing_cols:
            if row.get(col, 0) == 1.0:
                ings.append(col.lower())
        return ings

    def _calculate_recipe_nutrients(self, ingredients: List[str]) -> Dict[str, float]:
        totals = {'protein_pct': 0.0, 'fat_pct': 0.0, 'sodium_pct': 0.0, 'calories_pct': 0.0}
        for ing in ingredients:
            if ing in self.nutrition_dict:
                vals = self.nutrition_dict[ing]
                totals['protein_pct'] += vals[0]
                totals['fat_pct'] += vals[1]
                totals['sodium_pct'] += vals[2]
                totals['calories_pct'] += vals[3]
        return totals

    def _determine_meal_type(self, ingredients: List[str]) -> str:
        ing_set = set(ingredients)
        
        b_score = len(ing_set.intersection(self.breakfast_keys))
        d_score = len(ing_set.intersection(self.dinner_keys))
        l_score = len(ing_set.intersection(self.lunch_keys))
        
        if b_score > 0 and b_score >= d_score:
            return 'breakfast'
        elif d_score > 0:
            return 'dinner'
        elif l_score > 0:
            return 'lunch'
        else:
            if len(ingredients) > 15:
                return 'dinner'
            elif len(ingredients) < 6:
                return 'breakfast'
            return 'lunch'

    def generate_menu(self, max_tries: int = 5000) -> Optional[Dict]:
        best_menu = None
        best_total_rating = -1
        
        MAX_DAILY_LIMIT = 280.0 
        
        candidates = {'breakfast': [], 'lunch': [], 'dinner': []}
        
        for idx, row in self.df.iterrows():
            if pd.isna(row['title']) or row['rating'] <= 0:
                continue
            
            ings = self._get_recipe_ingredients(row)
            if not ings:
                continue
                
            nutrients = self._calculate_recipe_nutrients(ings)
            
            if (nutrients['protein_pct'] > 90 or nutrients['fat_pct'] > 90 or 
                nutrients['sodium_pct'] > 90 or nutrients['calories_pct'] > 90):
                continue
                
            meal_type = self._determine_meal_type(ings)
            
            recipe_data = {
                'title': row['title'],
                'rating': row['rating'],
                'ingredients': ings,
                'nutrients': nutrients,
                'type': meal_type
            }
            candidates[meal_type].append(recipe_data)

        all_recipes = candidates['breakfast'] + candidates['lunch'] + candidates['dinner']
        for key in candidates:
            if len(candidates[key]) < 20:
                existing_titles = {x['title'] for x in candidates[key]}
                extra = [x for x in sorted(all_recipes, key=lambda x: x['rating'], reverse=True) if x['title'] not in existing_titles]
                candidates[key].extend(extra[:30])
            else:
                candidates[key] = sorted(candidates[key], key=lambda x: x['rating'], reverse=True)[:100]

        for _ in range(max_tries):
            try:
                if not candidates['breakfast'] or not candidates['lunch'] or not candidates['dinner']:
                    continue

                r1 = random.choice(candidates['breakfast'])
                r2 = random.choice(candidates['lunch'])
                r3 = random.choice(candidates['dinner'])
                
                titles = {r1['title'], r2['title'], r3['title']}
                if len(titles) < 3:
                    continue
                
                sum_p = r1['nutrients']['protein_pct'] + r2['nutrients']['protein_pct'] + r3['nutrients']['protein_pct']
                sum_f = r1['nutrients']['fat_pct'] + r2['nutrients']['fat_pct'] + r3['nutrients']['fat_pct']
                sum_s = r1['nutrients']['sodium_pct'] + r2['nutrients']['sodium_pct'] + r3['nutrients']['sodium_pct']
                sum_c = r1['nutrients']['calories_pct'] + r2['nutrients']['calories_pct'] + r3['nutrients']['calories_pct']
                
                if sum_p <= MAX_DAILY_LIMIT and sum_f <= MAX_DAILY_LIMIT and sum_s <= MAX_DAILY_LIMIT and sum_c <= MAX_DAILY_LIMIT:
                    total_rating = r1['rating'] + r2['rating'] + r3['rating']
                    
                    if total_rating > best_total_rating:
                        best_total_rating = total_rating
                        best_menu = {
                            'BREAKFAST': r1,
                            'LUNCH': r2,
                            'DINNER': r3,
                            'totals': {'p': sum_p, 'f': sum_f, 's': sum_s, 'c': sum_c}
                        }
            except IndexError:
                continue

        return best_menu