import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    num_of_movies = Movie.objects.count()
    assert num_of_movies == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Big Lebowski", "genre": "comedy", "year": "1998"},
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "Big Lebowski"

    movies_quantity = Movie.objects.count()
    assert movies_quantity == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    num_of_movies = Movie.objects.count()
    assert num_of_movies == 0

    resp = client.post("/api/movies/", {}, content_type="application/json")
    assert resp.status_code == 400
    num_of_movies = Movie.objects.count()
    num_of_movies == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    num_of_movies = Movie.objects.count()
    assert num_of_movies == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Big Lebowski", "genre": "comedy"},
        content_type="application/json",
    )

    assert resp.status_code == 400

    num_of_movies = Movie.objects.count()
    assert num_of_movies == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "The Big Lebowski"


def test_get_single_movie_invalid_id(client):
    resp = client.get("/api/moives/foo/")

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    movie_two = add_movie(title="No Country For Old Men", genre="thriller", year="2007")
    resp = client.get("/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title
