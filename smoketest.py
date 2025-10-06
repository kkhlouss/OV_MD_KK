import json
from app import app

with app.test_client() as c:
    r = c.get('/api/movies?min_rating=7')
    print('Movies >=7:', len(r.get_json()['movies']))
    r = c.get('/api/movies/popular')
    print('Popular:', len(r.get_json()['movies']))
    r = c.post('/api/reviews', json={"movieId": 1, "author": "Tests", "content": "Ļoti laba filma!", "rating": 8})
    print('Create review:', r.status_code)
    r = c.get('/api/reviews?movie_id=1')
    print('Reviews for 1:', len(r.get_json()['reviews']))
