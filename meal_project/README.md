# MealFinder — Django Recipe App
Menampilkan resep dari TheMealDB API

## Cara Menjalankan

### 1. Install Django
```bash
pip install django
```

### 2. Jalankan Server
```bash
cd meal_project
python manage.py runserver
```

### 3. Buka Browser
```
http://127.0.0.1:8000/
```

## Struktur Project
```
meal_project/
├── manage.py
├── requirements.txt
├── meal_project/
│   ├── settings.py
│   └── urls.py
└── meals/
    ├── views.py       ← Fungsi API request ada di sini
    ├── urls.py
    └── templates/
        └── meals/
            ├── index.html   ← Halaman utama
            └── detail.html  ← Halaman detail resep
```

## Fitur
- Pencarian resep berdasarkan kata kunci
- Tampilan kartu resep dengan gambar
- Halaman detail resep (bahan + cara membuat)
- Link ke video YouTube
- API: https://www.themealdb.com
