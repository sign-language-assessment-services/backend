from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from app.core.models.media_types import MediaType


class CreateMultimediaFileRequest(BaseModel):
    media_type: MediaType


class NotAsJson:
    """Class to fix representing right schema in OpenAPI docs

    https://github.com/fastapi/fastapi/discussions/8406
    """
    @classmethod
    def __get_pydantic_json_schema__(
            cls,
            core_schema: CoreSchema,
            handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        if "contentSchema" in json_schema:
            return json_schema["contentSchema"]
        return json_schema
