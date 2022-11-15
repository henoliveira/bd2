from pydantic import BaseModel as __BaseModel
from typing import Union


class ModelDepartments(__BaseModel):
    id: int
    title: str


class ModelArtworkTypes(__BaseModel):
    id: int
    title: str


class ModelCategories(__BaseModel):
    id: int
    title: str
    subtype: str


class ModelArtists(__BaseModel):
    id: int
    title: str
    sort_title: Union[str, None]
    is_artist: bool
    birth_date: Union[int, None]
    death_date: Union[int, None]
    description: Union[str, None]


class ModelArtworks(__BaseModel):
    id: int
    id_artist: Union[int, None]
    id_department: Union[int, None]
    id_artwork_type: Union[int, None]
    id_gallery: Union[int, None]
    date_start: Union[int, None]
    date_end: Union[int, None]
    date_display: Union[str, None]
    place_of_origin: Union[str, None]
    title: Union[str, None]
    medium_display: Union[str, None]
    dimensions: Union[str, None]
    api_link: Union[str, None]


class ModelArtworksCategories(__BaseModel):
    id: int
    id_artwork: int
    id_category: int
