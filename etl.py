import requests
import db.models as models
from db.config import DbConfig

base_url = "https://api.artic.edu/api/v1/$ROUTE?limit=100"
db = DbConfig()


def load_departments():
    print("Loading departments...")
    url = base_url.replace("$ROUTE", "departments")
    request = requests.get(url).json()
    total_pages = request["pagination"]["total_pages"]

    for page in range(1, total_pages + 1):
        departments = request["data"]
        for department in departments:
            department = models.ModelDepartments(
                id=department["id"][3:], title=department["title"]
            )
            status = db.alter(
                "INSERT INTO departments (id, title) VALUES (%s, %s)",
                (department.id, department.title),
            )
            if status != "sucesso":
                print("Error inserting department with id: " + str(department.id))
        if page < total_pages:
            request = requests.get(request["pagination"]["next_url"]).json()


def load_artwork_types():
    print("Loading artwork types...")
    url = base_url.replace("$ROUTE", "artwork-types")
    request = requests.get(url).json()
    total_pages = request["pagination"]["total_pages"]

    for page in range(1, total_pages + 1):
        artwork_types = request["data"]
        for artwork_type in artwork_types:
            artwork_type = models.ModelArtworkTypes(
                id=artwork_type["id"], title=artwork_type["title"]
            )
            status = db.alter(
                "INSERT INTO artwork_types (id, title) VALUES (%s, %s)",
                (artwork_type.id, artwork_type.title),
            )
            if status != "sucesso":
                print("Error inserting artwork type with id: " + str(artwork_type.id))
        if page < total_pages:
            request = requests.get(request["pagination"]["next_url"]).json()


def load_categories():
    print("Loading categories...")
    url = base_url.replace("$ROUTE", "categories")
    request = requests.get(url).json()
    total_pages = request["pagination"]["total_pages"]

    for page in range(1, total_pages + 1):
        categories = request["data"]
        for category in categories:
            category = models.ModelCategories(
                id=category["id"][3:],
                title=category["title"],
                subtype=category["subtype"],
            )
            status = db.alter(
                "INSERT INTO categories (id, title, subtype) VALUES (%s, %s, %s)",
                (category.id, category.title, category.subtype),
            )
            if status != "sucesso":
                print("Error inserting category with id: " + str(category.id))
        if page < total_pages:
            request = requests.get(request["pagination"]["next_url"]).json()


def load_artists():
    print("Loading artists...")
    url = base_url.replace("$ROUTE", "agents")
    request = requests.get(url).json()
    total_pages = request["pagination"]["total_pages"]

    for page in range(1, total_pages + 1):
        artists = request["data"]
        for artist in artists:
            artist = models.ModelArtists(
                id=artist["id"],
                title=artist["title"],
                sort_title=artist["sort_title"],
                is_artist=artist["is_artist"],
                birth_date=artist["birth_date"],
                death_date=artist["death_date"],
                description=artist["description"],
            )
            status = db.alter(
                "INSERT INTO artists (id, title, sort_title, is_artist, birth_date, death_date, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    artist.id,
                    artist.title,
                    artist.sort_title,
                    artist.is_artist,
                    artist.birth_date,
                    artist.death_date,
                    artist.description,
                ),
            )
            if status != "sucesso":
                print("Error inserting artist with id: " + str(artist.id))
        if page < total_pages:
            request = requests.get(request["pagination"]["next_url"]).json()


def load_artworks():
    print("Loading artworks...")
    url = base_url.replace("$ROUTE", "artworks")
    request = requests.get(url).json()
    total_pages = request["pagination"]["total_pages"]
    if total_pages > 250:
        total_pages = 250

    for page in range(1, total_pages + 1):
        artworks = request["data"]
        for artwork in artworks:

            try:
                department_id = artwork["department_id"][3:]
            except:
                department_id = None

            artwork_to_insert = models.ModelArtworks(
                id=artwork["id"],
                id_artist=artwork["artist_id"],
                id_department=department_id,
                id_artwork_type=artwork["artwork_type_id"],
                date_start=artwork["date_start"],
                date_display=artwork["date_display"],
                date_end=artwork["date_end"],
                place_of_origin=artwork["place_of_origin"],
                title=artwork["title"],
                medium_display=artwork["medium_display"],
                dimensions=artwork["dimensions"],
                api_link=artwork["api_link"],
            )
            status = db.alter(
                "INSERT INTO artworks (id, id_artist, id_department, id_artwork_type, date_start, date_display, date_end, place_of_origin, title, medium_display, dimensions, api_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    artwork_to_insert.id,
                    artwork_to_insert.id_artist,
                    artwork_to_insert.id_department,
                    artwork_to_insert.id_artwork_type,
                    artwork_to_insert.date_start,
                    artwork_to_insert.date_display,
                    artwork_to_insert.date_end,
                    artwork_to_insert.place_of_origin,
                    artwork_to_insert.title,
                    artwork_to_insert.medium_display,
                    artwork_to_insert.dimensions,
                    artwork_to_insert.api_link,
                ),
            )
            if status != "sucesso":
                print("Error inserting artwork with id: " + str(artwork_to_insert.id))

            for category in artwork["category_ids"]:
                category_id = str(category).replace("PC-", "")
                status = db.alter(
                    "INSERT INTO artworks_categories (id_artwork, id_category) VALUES (%s, %s)",
                    (artwork_to_insert.id, category_id),
                )
                if status != "sucesso":
                    print(
                        "Error inserting artwork category with id: "
                        + str(artwork_to_insert.id)
                    )

        if page < total_pages:
            request = requests.get(request["pagination"]["next_url"]).json()


def load_full_database():
    load_departments()
    load_artwork_types()
    load_categories()
    load_artists()
    load_artworks()


if __name__ == "__main__":
    load_full_database()
    # load_galleries()
    # load_artworks()
