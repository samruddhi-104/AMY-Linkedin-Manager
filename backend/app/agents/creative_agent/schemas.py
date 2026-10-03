from pydantic import BaseModel


class CreativeResult(BaseModel):

    post_id: str

    concept: str

    image_prompt: str

    aspect_ratio: str

    asset_id: str

    asset_path: str