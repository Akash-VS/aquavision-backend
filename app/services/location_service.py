"""
File: location_service.py
Purpose: Find nearby water bodies using OpenStreetMap Overpass API.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import math
import requests

from app.core.logging import logger


class LocationService:

    OVERPASS_URL = "https://overpass-api.de/api/interpreter"

    SEARCH_RADIUS = 15000  # 15 KM

    def _distance_km(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """
        Calculate distance using Haversine Formula.
        """

        R = 6371

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )

        return round(R * c, 2)

    def get_nearby_water_bodies(
        self,
        latitude: float,
        longitude: float,
    ):

        logger.info("Searching nearby water bodies...")

        query = f"""
        [out:json][timeout:30];

        (

        node["natural"="water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        way["natural"="water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        relation["natural"="water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});

        node["water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        way["water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        relation["water"](around:{self.SEARCH_RADIUS},{latitude},{longitude});

        node["waterway"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        way["waterway"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        relation["waterway"](around:{self.SEARCH_RADIUS},{latitude},{longitude});

        node["landuse"="reservoir"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        way["landuse"="reservoir"](around:{self.SEARCH_RADIUS},{latitude},{longitude});
        relation["landuse"="reservoir"](around:{self.SEARCH_RADIUS},{latitude},{longitude});

        );

        out center;
        """

        try:

            response = requests.post(
                self.OVERPASS_URL,
                data={"data": query},
                headers={
                    "User-Agent": "AquaVisionAI/1.0"
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

        except Exception as e:

            logger.exception("Failed to fetch nearby water bodies.")

            raise RuntimeError(str(e))

        water_bodies = []

        seen = set()

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            name = tags.get(
                "name",
                "Unnamed Water Body"
            )

            if name in seen:
                continue

            seen.add(name)

            if "center" in item:

                lat = item["center"]["lat"]
                lon = item["center"]["lon"]

            else:

                lat = item.get("lat")
                lon = item.get("lon")

            if lat is None or lon is None:
                continue

            water_type = (
                tags.get("water")
                or tags.get("waterway")
                or tags.get("natural")
                or tags.get("landuse")
                or "Water Body"
            )

            water_bodies.append(
                {
                    "name": name,
                    "type": water_type.title(),
                    "latitude": lat,
                    "longitude": lon,
                    "distance_km": self._distance_km(
                        latitude,
                        longitude,
                        lat,
                        lon,
                    ),
                }
            )

        water_bodies.sort(
            key=lambda x: x["distance_km"]
        )

        logger.info(
            f"Found {len(water_bodies)} nearby water bodies."
        )

        return water_bodies


location_service = LocationService()