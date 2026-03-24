#!/Users/arthur/.pyenv/shims/python

import sys
import re
from typing import List
from recipes import RecipePredictor, NutritionFacts, SimilarRecipes, DailyMenuGenerator

def print_forecast(prediction: str):
    print("I. OUR FORECAST")
    print(prediction)
    print()

def print_nutrition_facts(ingredients: List[str], nutrition_facts: NutritionFacts):
    print("II. NUTRITION FACTS")
    nutrients_data = nutrition_facts.get_nutrition(ingredients)
    if not nutrients_data:
        print("No nutrition data available for these ingredients.")
        return
    for item in nutrients_data:
        ingredient = item['ingredient']
        print(ingredient)
        print(f"  Protein - {item['protein_pct']:.1f}% of Daily Value")
        print(f"  Calories - {item['calories_pct']:.1f}% of Daily Value")
        print(f"  Total Fat - {item['fat_pct']:.1f}% of Daily Value")
        print(f"  Sodium - {item['sodium_pct']:.1f}% of Daily Value")
    print()

def print_similar_recipes(ingredients: List[str], similar_recipes: SimilarRecipes):
    print("III. TOP-3 SIMILAR RECIPES:")
    top_recipes = similar_recipes.find_similar(ingredients, top_k=3)
    if not top_recipes:
        print("No similar recipes found.")
        return
    for recipe in top_recipes:
        print(f"- {recipe['recipe_name']}, rating: {recipe['rating']:.1f}, URL: {recipe['url']}")
    print()

def print_daily_menu(menu: dict):
    print("\n" + "=" * 60)
    print("DAILY MENU")
    print("=" * 60)
    
    for meal_name in ['BREAKFAST', 'LUNCH', 'DINNER']:
        recipe = menu[meal_name]
        print(f"\n{meal_name}")
        print("-" * 20)
        print(f"{recipe['title']} (rating: {recipe['rating']})")
        print("Ingredients:")
        for ing in recipe['ingredients'][:7]:
            print(f"- {ing}")
        if len(recipe['ingredients']) > 7:
            print(f"... and {len(recipe['ingredients'])-7} more")
            
        print("Nutrients:")
        n = recipe['nutrients']
        print(f"- protein: {n['protein_pct']:.1f}%")
        print(f"- fat: {n['fat_pct']:.1f}%")
        print(f"- sodium: {n['sodium_pct']:.1f}%")
        print(f"- calories: {n['calories_pct']:.1f}%")
        
        slug = re.sub(r'[^a-z0-9\s-]', '', str(recipe['title']).lower())
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        url = f"https://www.epicurious.com/recipes/food/views/{slug}"
        print(f"URL: {url}")
    
    print("\n" + "=" * 60)
    print("TOTAL DAILY INTAKE:")
    t = menu['totals']
    print(f"Protein: {t['p']:.1f}% | Fat: {t['f']:.1f}% | Sodium: {t['s']:.1f}% | Calories: {t['c']:.1f}%")
    total_rating = menu['BREAKFAST']['rating'] + menu['LUNCH']['rating'] + menu['DINNER']['rating']
    print(f"Total Rating Score: {total_rating:.2f}")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./nutritionist.py <ingredient1>, <ingredient2>, ...")
        print("       ./nutritionist.py --menu")
        sys.exit(1)

    if sys.argv[1] == '--menu':
        try:
            generator = DailyMenuGenerator(
                data_csv_path='../data/epi_r.csv',
                nutrition_csv_path='../data/nutrition_facts.csv'
            )
            menu = generator.generate_menu()
            if menu:
                print_daily_menu(menu)
            else:
                print("Could not find a suitable menu satisfying all constraints.")
        except Exception as e:
            print(f"Error generating menu: {e}")
            sys.exit(1)
        sys.exit(0)

    ingredients_input = ' '.join(sys.argv[1:])
    
    if ',' in ingredients_input:
        ingredients = [ing.strip().lower() for ing in ingredients_input.split(',') if ing.strip()]
    else:
        ingredients = [ing.strip().lower() for ing in ingredients_input.split() if ing.strip()]

    if not ingredients:
        print("Error: No ingredients provided.")
        sys.exit(1)

    print(f"Analyzing ingredients: {', '.join(ingredients)}")
    print()

    try:
        predictor = RecipePredictor(model_path='../data/best_recipe_classifier.pkl')
        nutrition_facts = NutritionFacts(nutrition_csv_path='../data/nutrition_facts.csv')
        similar_recipes = SimilarRecipes(
            recipes_csv_path='../data/similar_recipes.csv',
            data_csv_path='../data/epi_r.csv'
        )

        prediction = predictor.predict(ingredients)
        print_forecast(prediction)

        print_nutrition_facts(ingredients, nutrition_facts)

        print_similar_recipes(ingredients, similar_recipes)

    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()