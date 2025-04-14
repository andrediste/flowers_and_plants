from sqlalchemy import MetaData, Text
from sqlalchemy.orm import DeclarativeBase


metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {str: Text()}
