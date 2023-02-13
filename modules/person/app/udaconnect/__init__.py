from app.udaconnect.models import Person 
from app.udaconnect.schemas import PersonSchema 


def register_routes(api, app, root="api/v2"):
    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
