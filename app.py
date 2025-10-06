from __future__ import annotations
from flask import Flask, jsonify, render_template, request
from datetime import datetime
from typing import List, Dict, Any

app = Flask(__name__)

# --- In-memory sample data (demo only) ---
movies: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Klusā Pilsēta",
        "year": 2022,
        "rating": 8.4,
        "genres": ["drāma", "misterija"],
        "description": "Stāsts par pilsētu, kur katrai ielai ir sava noslēpumaina skaņa.",
        "popular": True,
        "poster": "https://picsum.photos/seed/klusa-pilseta/400/600",
    },
    {
        "id": 2,
        "title": "Zvaigžņu Tilts",
        "year": 2021,
        "rating": 7.9,
        "genres": ["sci-fi", "drāma"],
        "description": "Inženieris mēģina uzbūvēt tiltu starp divām pasaulēm.",
        "popular": True,
        "poster": "https://picsum.photos/seed/zvaigznu-tilts/400/600",
    },
    {
        "id": 3,
        "title": "Vēja Pēdas",
        "year": 2020,
        "rating": 6.8,
        "genres": ["avantūra"],
        "description": "Ceļojums pāri kalniem, kur katrs solis maina varoņu likteni.",
        "popular": False,
        "poster": "https://picsum.photos/seed/veja-pedas/400/600",
    },
    {
        "id": 4,
        "title": "Melnbalta Nakts",
        "year": 2019,
        "rating": 8.8,
        "genres": ["noārs"],
        "description": "Detektīvs atšķetina noslēpumu pilsētā, kur viss ir pelēks.",
        "popular": True,
        "poster": "https://picsum.photos/seed/melnbalta-nakts/400/600",
    },
    {
        "id": 5,
        "title": "Jūras Elpa",
        "year": 2023,
        "rating": 7.2,
        "genres": ["drāma"],
        "description": "Mazpilsētas zvejnieku ģimenes stāsts par drosmi un cerību.",
        "popular": False,
        "poster": "https://picsum.photos/seed/juras-elpa/400/600",
    },
    {
        "id": 6,
        "title": "Neona Lietus",
        "year": 2024,
        "rating": 9.1,
        "genres": ["sci-fi", "trilleris"],
        "description": "Kibermetropole, atmiņu tirgus un pazudis hakeris.",
        "popular": True,
        "poster": "https://picsum.photos/seed/neona-lietus/400/600",
    },
    {
        "id": 7,
        "title": "Pazudušais Orķestris",
        "year": 2018,
        "rating": 7.0,
        "genres": ["mūzika", "drāma"],
        "description": "Jauna diriģente meklē orķestri, kas nespēlē nevienā zālē.",
        "popular": False,
        "poster": "https://picsum.photos/seed/pazudusais-orkestris/400/600",
    },
    {
        "id": 8,
        "title": "Aizsniedzamais Horizonts",
        "year": 2022,
        "rating": 6.5,
        "genres": ["avantūra", "drāma"],
        "description": "Divi draugi dzenas pakaļ sapnim, kas vienmēr vienu soli tālāk.",
        "popular": False,
        "poster": "https://picsum.photos/seed/horizonts/400/600",
    },
    {
        "id": 9,
        "title": "Naktstauriņi",
        "year": 2017,
        "rating": 8.0,
        "genres": ["romantika"],
        "description": "Mīlas stāsts starp fotogrāfu un nakts dārznieci.",
        "popular": False,
        "poster": "https://picsum.photos/seed/naktstaurini/400/600",
    },
    {
        "id": 10,
        "title": "Zibsnis",
        "year": 2016,
        "rating": 5.9,
        "genres": ["trilleris"],
        "description": "Pilsētu pārņem neskaidras izdzišanas, un tikai viena žurnāliste meklē patiesību.",
        "popular": False,
        "poster": "https://picsum.photos/seed/zibsnis/400/600",
    },
    {
        "id": 11,
        "title": "Sudraba Mežs",
        "year": 2020,
        "rating": 7.6,
        "genres": ["fantāzija"],
        "description": "Leģenda par mežu, kur koki atceras visu.",
        "popular": True,
        "poster": "https://picsum.photos/seed/sudraba-mezs/400/600",
    },
    {
        "id": 12,
        "title": "Smilšu Pulss",
        "year": 2021,
        "rating": 6.2,
        "genres": ["drāma"],
        "description": "Pilsēta tuksnesī elpo pāri laikam.",
        "popular": False,
        "poster": "https://picsum.photos/seed/smilsu-pulss/400/600",
    },
]

reviews: List[Dict[str, Any]] = [
    {
        "id": 1,
        "movieId": 1,
        "author": "Aija",
        "rating": 9,
        "content": "Ļoti atmosfēriska un jūtīga filma.",
        "createdAt": datetime(2024, 6, 12, 10, 30).isoformat(),
    },
    {
        "id": 2,
        "movieId": 2,
        "author": "Jānis",
        "rating": 8,
        "content": "Idejas par tiltiem starp pasaulēm paliek prātā.",
        "createdAt": datetime(2024, 9, 5, 9, 12).isoformat(),
    },
    {
        "id": 3,
        "movieId": 4,
        "author": "Zane",
        "rating": 9,
        "content": "Estētiski spēcīga – kadri kā fotogrāfijas.",
        "createdAt": datetime(2023, 11, 2, 19, 45).isoformat(),
    },
]

next_review_id = 4

# --- Views ---
@app.get("/")
def index():
    return render_template("index.html")

# --- API: Movies ---
@app.get("/api/movies")
def api_movies():
    min_rating = request.args.get("min_rating", type=float)
    genre = request.args.get("genre", type=str)

    filtered = movies
    if min_rating is not None:
        filtered = [m for m in filtered if m["rating"] >= min_rating]
    if genre:
        filtered = [m for m in filtered if genre.lower() in (g.lower() for g in m["genres"])]

    return jsonify({"movies": filtered})

@app.get("/api/movies/popular")
def api_movies_popular():
    popular = [m for m in movies if m.get("popular")]
    return jsonify({"movies": popular})

@app.get("/api/movies/<int:movie_id>")
def api_movie_by_id(movie_id: int):
    movie = next((m for m in movies if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(movie)

# --- API: Reviews ---
@app.get("/api/reviews")
def api_reviews():
    movie_id = request.args.get("movie_id", type=int)
    if movie_id is None:
        return jsonify({"reviews": reviews})
    return jsonify({"reviews": [r for r in reviews if r["movieId"] == movie_id]})

@app.post("/api/reviews")
def api_create_review():
    global next_review_id
    data = request.get_json(force=True, silent=True) or {}

    movie_id = data.get("movieId")
    author = data.get("author")
    content = data.get("content")
    rating = data.get("rating")

    if not movie_id or not author or not content:
        return jsonify({"error": "Trūkst lauku: movieId, author, content"}), 400

    if not any(m["id"] == movie_id for m in movies):
        return jsonify({"error": "Filma nav atrasta"}), 404

    review = {
        "id": next_review_id,
        "movieId": movie_id,
        "author": author,
        "content": content,
        "rating": int(rating) if isinstance(rating, (int, float, str)) and str(rating).isdigit() else None,
        "createdAt": datetime.utcnow().isoformat(),
    }
    reviews.append(review)
    next_review_id += 1
    return jsonify(review), 201

# --- API: Contact ---
@app.post("/api/contact")
def api_contact():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name", "")
    email = data.get("email", "")
    message = data.get("message", "")
    if not name or not email or not message:
        return jsonify({"error": "Lūdzu aizpildiet visus laukus"}), 400

    # Demo: log to console; real app would email/store
    app.logger.info("Contact message from %s <%s>: %s", name, email, message)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
