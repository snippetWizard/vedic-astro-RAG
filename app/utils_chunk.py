import json
from typing import List, Dict, Any


def load_domain_jsons() -> List[Dict[str, Any]]:
    """
    Loads all domain JSON files (astrology houses, planets, planets_in_house) and
    returns them as python dicts in a list. We'll use this for ingestion.
    """
    files = [
        "app/domain/astrology_houses.json",
        "app/domain/astrology_planets.json",
        "app/domain/planets_in_house.json"
    ]
    docs = []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
            docs.append({"source_file": fp, "data": data})
    return docs


def flatten_astrology_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert the structured astrology JSON into retrievable text chunks.

    We’ll emit chunks shaped like:
    {
      "text": "...",
      "metadata": {...}
    }

    Strategy:
    - houses -> each house becomes one chunk
    - planets -> each planet becomes one chunk
    - planets_in_house -> each planet-in-house relationship becomes one chunk

    You can tune chunk granularity here.
    """
    chunks: List[Dict[str, Any]] = []

    for d in docs:
        src = d["source_file"]
        data = d["data"]

        # 1. houses
        if "vedic_astrology" in data and "houses" in data["vedic_astrology"]:
            for h in data["vedic_astrology"]["houses"]:
                text_block = (
                    f"House {h.get('house_number')} - {h.get('house_name')}:\n"
                    f"Sign: {h.get('zodiac_sign')}\n"
                    f"Ruling Planet(s): {h.get('ruling_planet')}\n"
                    f"Meaning: {h.get('meaning')}\n"
                    f"Influence: {h.get('influence')}\n"
                    f"Gemstone: {h.get('recommended_gemstone', {}).get('name')}\n"
                    f"Gemstone Effects: {h.get('recommended_gemstone', {}).get('effects')}\n"
                    f"Notes: {h.get('note', 'N/A')}\n"
                )
                chunks.append({
                    "text": text_block,
                    "metadata": {
                        "type": "house",
                        "house_number": h.get("house_number"),
                        "zodiac_sign": h.get("zodiac_sign"),
                        "source_file": src
                    }
                })

        # 2. planets
        if "vedic_astrology" in data and "planets" in data["vedic_astrology"]:
            for p in data["vedic_astrology"]["planets"]:
                gem = p.get("gemstone", {})
                text_block = (
                    f"Planet: {p.get('name')}\n"
                    f"Sanskrit: {p.get('sanskrit_name', 'N/A')}\n"
                    f"Description: {p.get('description')}\n"
                    f"Influence: {p.get('influence')}\n"
                    f"Gemstone: {gem.get('name')}, Color: {gem.get('color')}, Effects: {gem.get('effects')}\n"
                )
                chunks.append({
                    "text": text_block,
                    "metadata": {
                        "type": "planet",
                        "planet_name": p.get("name"),
                        "source_file": src
                    }
                })

        # 3. planets_in_house
        if "planets_in_house" in data:
            house_data = data["planets_in_house"]
            house_no = house_data.get("house_number")
            for planet_obj in house_data.get("planets", []):
                text_block = (
                    f"Planet {planet_obj.get('planet')} in House {house_no}:\n"
                    f"Summary: {planet_obj.get('summary', '')}\n"
                    f"Positive: {', '.join(planet_obj.get('positive_manifestations', planet_obj.get('positive_traits', [])))}\n"
                    f"Negative: {', '.join(planet_obj.get('negative_manifestations', planet_obj.get('negative_traits', [])))}\n"
                )
                chunks.append({
                    "text": text_block,
                    "metadata": {
                        "type": "planet_in_house",
                        "house_number": house_no,
                        "planet_name": planet_obj.get("planet"),
                        "source_file": src
                    }
                })

    return chunks
