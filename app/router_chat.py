from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import os

from .logic_interpret import load_house_lords_map, interpret_chart

router = APIRouter(prefix="/chart", tags=["chart"])


# ---------- Request / Response Schemas ----------

class ChartRequest(BaseModel):
    name: str = Field(..., description="User name")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD")
    lat: float = Field(..., description="Latitude")
    long: float = Field(..., description="Longitude")
    houses: Dict[str, str] = Field(
        ...,
        description="Map of house_number -> planet. Example: { '1': 'Sun', '2': 'Mars', ... }"
    )


@router.post("/analyze")
async def analyze_chart(body: ChartRequest) -> Any:
    """
    Generate interpretation for the provided chart placements.

    This:
    - Loads house_lords.json (natural rulers, themes)
    - Uses PLANET_IN_HOUSE_LIBRARY to get positives/negatives for each placement
    - Generates host-guest dynamic
    - Returns final structured JSON
    """

    house_lords_path = os.path.join("app", "domain", "house_lords.json")
    try:
        house_lords_map = load_house_lords_map(house_lords_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="house_lords.json not found on server")

    user_payload = body.model_dump()
    result = interpret_chart(user_payload, house_lords_map)
    return result
