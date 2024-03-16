from dotenv import dotenv_values
import os, maara

#loading credentials for the tool
def load_credentials():
    config = dotenv_values(".env")
    os.environ["GOOGLE_CSE_ID"] = config["GOOGLE_CSE_ID"]
    os.environ["GOOGLE_API_KEY"] = config["GOOGLE_API_KEY"]
    os.environ["OPENAI_API_KEY"] = config["openai_api"]
    os.environ["serp_api"] = config["serp_api"]
    os.environ["GOOGLE_MAP_API_KEY"] = config["GOOGLE_MAP_API_KEY"] 
    

load_credentials()

from maara.google_search import *
from maara.phrasing_tool import *
from maara.google_map import *
from maara.location import *
from maara.image_processor import *
