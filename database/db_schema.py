"""Going to use sqlalchemy to create a PostgreSQL database
which is populated upon startup from our nested json package
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Relationship
from database import Base
