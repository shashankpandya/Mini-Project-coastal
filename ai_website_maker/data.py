from typing import Dict, List
PALETTES: Dict[str, Dict[str, str]] = {
    "Coastal Blue": {
        "primary": "#0B4F6C",
        "secondary": "#1F7A8C",
        "accent": "#E36414",
        "background": "#F5F9FC",
        "surface": "#FFFFFF",
        "text": "#132A3B",
    },
    "Forest Commerce": {
        "primary": "#1F5C3A",
        "secondary": "#2B8A57",
        "accent": "#E9A23B",
        "background": "#F4F8F4",
        "surface": "#FFFFFF",
        "text": "#1A2A22",
    },
    "Metro Slate": {
        "primary": "#1E293B",
        "secondary": "#334155",
        "accent": "#F97316",
        "background": "#F8FAFC",
        "surface": "#FFFFFF",
        "text": "#0F172A",
    },
    "Midnight Violet": {
        "primary": "#4C1D95",
        "secondary": "#6D28D9",
        "accent": "#F59E0B",
        "background": "#F5F3FF",
        "surface": "#FFFFFF",
        "text": "#1E0A3C",
    },
    "Rose Luxury": {
        "primary": "#881337",
        "secondary": "#BE123C",
        "accent": "#CA8A04",
        "background": "#FFF1F2",
        "surface": "#FFFFFF",
        "text": "#3B0015",
    },
}

TEMPLATES: List[Dict[str, str]] = [
    {
        "name": "Agency Showcase",
        "description": "Bold hero + service cards + pricing strip + trust badges.",
        "home_preview": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80",
        "portfolio_preview": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&q=80",
    },
    {
        "name": "Studio Minimal",
        "description": "Minimal layout with strong typography and product storytelling.",
        "home_preview": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=600&q=80",
        "portfolio_preview": "https://images.unsplash.com/photo-1497215842964-222b430dc094?w=600&q=80",
    },
    {
        "name": "Retail Launch",
        "description": "Product-forward landing with pricing and enquiry conversion blocks.",
        "home_preview": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&q=80",
        "portfolio_preview": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?w=600&q=80",
    },
]

DEFAULT_PRODUCTS = [
    {"type": "Service", "name": "Starter Consulting", "description": "Discovery + strategy", "price": 499.0},
    {"type": "Product", "name": "Business Website Pack", "description": "5-page responsive site", "price": 1499.0},
]



