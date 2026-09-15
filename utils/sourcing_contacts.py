"""Verified sourcing-contact metadata for the winning-products catalog.

Phone numbers are intentionally omitted until they can be verified from an
official market or supplier source. The dashboard must not present guessed
numbers as real business contacts.
"""

from typing import Dict, Any
from urllib.parse import quote


SOURCING_CONTACTS: Dict[str, Dict[str, Any]] = {
    "faisalabad textile market": {
        "store_name": "Faisalabad Textile",
        "city": "Faisalabad",
        "phone": "+92 324 7634343",
        "verification": "Public Google Maps business listing checked on 15 Sep 2026",
        "contact_method": "Call or WhatsApp the listed business and confirm wholesale availability",
        "source_url": "https://www.google.com/maps/search/?api=1&query=Faisalabad+Textile+Sona+Plaza+Rail+Bazar",
    },
    "shah alam market": {
        "store_name": "Shahalami.pk — Lahore's Largest Wholesale Market",
        "city": "Lahore",
        "phone": "+92 302 4055050",
        "verification": "Public Google Maps business listing checked on 15 Sep 2026",
        "contact_method": "Call the listed market service and confirm the relevant supplier lane",
        "source_url": "https://www.google.com/maps/search/?api=1&query=Shahalami.pk+Lahore",
    },
    "bolton market": {
        "store_name": "Bolton Market & Light House",
        "city": "Karachi",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit the cosmetics/electronics wholesale lanes",
    },
    "hall road": {
        "store_name": "Hall Road Wholesale Market",
        "city": "Lahore",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit the relevant product lane and request a verified supplier contact",
    },
    "denso hall": {
        "store_name": "Denso Hall Wholesale Market",
        "city": "Karachi",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit the market and verify the supplier before paying",
    },
    "raja bazaar": {
        "store_name": "Raja Bazaar Wholesale Market",
        "city": "Rawalpindi",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit Gakhar Plaza/wholesale lanes and request a supplier WhatsApp number",
    },
    "gole market": {
        "store_name": "Gole Market",
        "city": "Faisalabad",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit the footwear wholesale area and verify the shop identity",
    },
    "mochi gate": {
        "store_name": "Mochi Gate Footwear Market",
        "city": "Lahore",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Visit the wholesale footwear lane and verify the supplier",
    },
    "gujranwala metal works": {
        "store_name": "Gujranwala Metal Works Cluster",
        "city": "Gujranwala",
        "phone": None,
        "verification": "No official public market phone number verified",
        "contact_method": "Request a factory contact through the local manufacturers' association",
    },
}


def get_sourcing_contact(hub_name: str) -> Dict[str, Any]:
    """Return the best matching verified contact record for a hub label."""
    normalized = hub_name.lower()
    for key, contact in SOURCING_CONTACTS.items():
        if key in normalized:
            return _with_listing_link(contact)
    return _with_listing_link({
        "store_name": hub_name,
        "city": "Not specified",
        "phone": None,
        "verification": "Supplier contact not verified",
        "contact_method": "Verify the supplier identity before placing an order",
    })


def _with_listing_link(contact: Dict[str, Any]) -> Dict[str, Any]:
    """Attach a public map/listing search without inventing a supplier number."""
    search = quote(f"{contact['store_name']} {contact['city']} wholesale")
    return {
        **contact,
        "listing_url": contact.get(
            "source_url",
            f"https://www.google.com/maps/search/?api=1&query={search}",
        ),
        "verified_on": "15 Sep 2026",
    }
