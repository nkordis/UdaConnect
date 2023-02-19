from datetime import datetime
from typing import Dict
import logging
import sys
import json
from models import Location
from __init__ import db


DATE_FORMAT = "%Y-%m-%d"
logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
logger = logging.getLogger("location-consumer")


class LocationService:
    @staticmethod
    def create(message: bytes) -> None:
        location = json.loads(message.decode('utf-8'))
        new_location = Location()
    
        new_location.person_id = location["user_id"]
        new_location.creation_time = datetime.now().strftime(DATE_FORMAT)
        #new_location.latitude = location[1] #location["latitude"]
        #new_location.longitude = location[2]#location["longitude"]
        #new_location.coordinate = f"POINT({location[2]} {location[1]})"
        new_location.coordinate = f"POINT({location['longitude']} {location['latitude']})"
        db.session.add(new_location)
        db.session.commit()
        logger.info(f"New location record created for user {new_location.person_id}")
