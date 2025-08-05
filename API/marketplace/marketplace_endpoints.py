# =============================
# Pratibimb Marketplace Endpoints
# =============================
from fastapi import APIRouter, Request
import requests
import uuid
from datetime import datetime
import json
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# --- Marketplace Router ---
router = APIRouter()




# --- Beckn Protocol Example Endpoints ---
class BecknProductSearchRequest(BaseModel):
    product: str

@router.post("/marketplace/beckn/search")
async def beckn_send_search(request: BecknProductSearchRequest):
    """
    Send a Beckn Protocol search request to the ONDC sandbox gateway (dynamic product search)
    and return the list of products found.
    """
    import requests
    import uuid
    import json
    from datetime import datetime

    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    BAP_URI = "https://a0b73638c65a.ngrok-free.app"  # Your ngrok URL

    payload = {
        "context": {
            "domain": "retail",
            "country": "IND",
            "city": "std:011",
            "action": "search",
            "core_version": "1.1.0",
            "bap_id": "buyer-app.ondc.org",
            "bap_uri": BAP_URI,
            "transaction_id": transaction_id,
            "message_id": message_id,
            "timestamp": timestamp
        },
        "message": {
            "intent": {
                "item": {
                    "descriptor": {
                        "name": request.product
                    }
                },
                "fulfillment": {
                    "end": {
                        "location": {
                            "gps": "28.6139,77.2090",
                            "address": {
                                "area_code": "110001"
                            }
                        }
                    }
                }
            }
        }
    }

    try:
        print(f"\U0001F4E4 Sending Beckn search request to ONDC sandbox for product: {request.product}")
        res = requests.post(
            "https://gateway.ondc.org/sandbox/search",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        res.raise_for_status()
        data = res.json()

        # Extract product list from response (adjust according to actual response structure)
        products = []
        # The products are usually nested inside message.catalog.bpp[].items
        bpp_list = data.get("message", {}).get("catalog", {}).get("bpp", [])
        for bpp in bpp_list:
            for item in bpp.get("items", []):
                products.append({
                    "id": item.get("id"),
                    "descriptor": item.get("descriptor", {}),
                    "price": item.get("price", {}),
                    "fulfillment": item.get("fulfillment", {}),
                    "location_id": item.get("location_id")
                })

        print(f"\u2705 Received {len(products)} products.")
        return {"products": products}

    except Exception as e:
        print("Error sending Beckn search request:", str(e))
        return {"error": str(e)}, 500


class MarketplaceListing(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    price: float
    seller: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class MarketplaceSearchRequest(BaseModel):
    query: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    seller: Optional[str] = None

@router.get("/marketplace/listings")
async def get_marketplace_listings():
    """Get all marketplace listings (placeholder)."""
    return {
        "status": "success",
        "listings": [],
        "message": "Marketplace listings fetched successfully (placeholder)."
    }

@router.get("/marketplace/listing/{listing_id}")
async def get_marketplace_listing(listing_id: str):
    """Get a single marketplace listing by ID (placeholder)."""
    return {
        "status": "success",
        "listing": None,
        "message": f"Marketplace listing {listing_id} fetched successfully (placeholder)."
    }

@router.post("/marketplace/create")
async def create_marketplace_listing(listing: MarketplaceListing):
    """Create a new marketplace listing (placeholder)."""
    return {
        "status": "success",
        "listing": listing,
        "message": "Marketplace listing created successfully (placeholder)."
    }

@router.put("/marketplace/update/{listing_id}")
async def update_marketplace_listing(listing_id: str, listing: MarketplaceListing):
    """Update an existing marketplace listing (placeholder)."""
    return {
        "status": "success",
        "listing": listing,
        "message": f"Marketplace listing {listing_id} updated successfully (placeholder)."
    }

@router.delete("/marketplace/delete/{listing_id}")
async def delete_marketplace_listing(listing_id: str):
    """Delete a marketplace listing (placeholder)."""
    return {
        "status": "success",
        "message": f"Marketplace listing {listing_id} deleted successfully (placeholder)."
    }

@router.post("/marketplace/search")
async def search_marketplace_listings(request: MarketplaceSearchRequest):
    """Search marketplace listings (placeholder)."""
    return {
        "status": "success",
        "results": [],
        "message": "Marketplace search completed successfully (placeholder)."
    }
