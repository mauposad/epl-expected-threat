import os
from dotenv import load_dotenv
import kagglehub
from kagglehub import KaggleDatasetAdapter
from kaggle.api.kaggle_api_extended import KaggleApi


load_dotenv()

api = KaggleApi()
api.authenticate()
