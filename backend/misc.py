from telegram import Update
from telegram.ext import ContextTypes
from shared import user_waiting_for_plant

from backend import get_recommendations
from data.connect import insert_plant

# while no db, store user location in memory
user_location = {}
user_data = {}
