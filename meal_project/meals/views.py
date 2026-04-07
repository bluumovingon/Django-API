import urllib.request
import json

# ============================================================
# FUNGSI: fetch_meals_from_api
# Mengambil data resep dari TheMealDB API berdasarkan keyword
# ============================================================
def fetch_meals_from_api(search_query):
    """
    Mengirim request ke TheMealDB API dan mengembalikan
    list resep yang sesuai dengan kata kunci pencarian.
    
    Args:
        search_query (str): Kata kunci pencarian resep
    
    Returns:
        list: Daftar resep, atau list kosong jika tidak ditemukan
    """
    base_url = "https://www.themealdb.com/api/json/v1/1/search.php"
    url = f"{base_url}?s={urllib.parse.quote(search_query)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            meals = data.get('meals') or []
            result = []
            for meal in meals:
                # Kumpulkan bahan-bahan (ingredient + measure)
                ingredients = []
                for i in range(1, 21):
                    ingredient = meal.get(f'strIngredient{i}', '').strip()
                    measure = meal.get(f'strMeasure{i}', '').strip()
                    if ingredient:
                        ingredients.append(f"{measure} {ingredient}".strip())

                result.append({
                    'id': meal.get('idMeal'),
                    'name': meal.get('strMeal'),
                    'category': meal.get('strCategory'),
                    'area': meal.get('strArea'),
                    'instructions': meal.get('strInstructions'),
                    'thumbnail': meal.get('strMealThumb'),
                    'tags': [t.strip() for t in meal.get('strTags', '').split(',')] if meal.get('strTags') else [],
                    'youtube': meal.get('strYoutube'),
                    'ingredients': ingredients,
                })
            return result

    except Exception as e:
        print(f"[ERROR] Gagal mengambil data API: {e}")
        return []


# ============================================================
# Perlu import urllib.parse juga
# ============================================================
import urllib.parse
from django.shortcuts import render


# ============================================================
# VIEW: index
# Halaman utama — menampilkan hasil pencarian resep
# ============================================================
def index(request):
    """
    View utama untuk halaman pencarian resep.
    Menerima parameter GET 's' sebagai kata kunci pencarian.
    """
    query = request.GET.get('s', 'chicken')  # default: chicken
    meals = fetch_meals_from_api(query)

    context = {
        'meals': meals,
        'query': query,
        'total': len(meals),
    }
    return render(request, 'meals/index.html', context)


# ============================================================
# VIEW: detail
# Halaman detail satu resep berdasarkan ID
# ============================================================
def detail(request, meal_id):
    """
    View untuk menampilkan detail lengkap satu resep.
    Mengambil data dari API berdasarkan meal ID.
    """
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    meal = None

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            meals_data = data.get('meals') or []
            if meals_data:
                m = meals_data[0]
                ingredients = []
                for i in range(1, 21):
                    ingredient = m.get(f'strIngredient{i}', '').strip()
                    measure = m.get(f'strMeasure{i}', '').strip()
                    if ingredient:
                        ingredients.append(f"{measure} {ingredient}".strip())

                meal = {
                    'id': m.get('idMeal'),
                    'name': m.get('strMeal'),
                    'category': m.get('strCategory'),
                    'area': m.get('strArea'),
                    'instructions': m.get('strInstructions'),
                    'thumbnail': m.get('strMealThumb'),
                    'tags': [t.strip() for t in m.get('strTags', '').split(',')] if m.get('strTags') else [],
                    'youtube': m.get('strYoutube'),
                    'ingredients': ingredients,
                }
    except Exception as e:
        print(f"[ERROR] Gagal mengambil detail resep: {e}")

    return render(request, 'meals/detail.html', {'meal': meal})
