from pydantic import BaseModel

class PredictRequest(BaseModel):
    image_base64: str

