"""
Visual theme for all graph outputs.
Dark mode by default. Clean, high-contrast, publication-quality.
"""

DARK_THEME = {
    "background": "#0D1117",         # GitHub dark background
    "node_default": "#8B949E",       # Muted gray
    "node_highlight": "#F0883E",     # Warm orange for highlights
    "node_client": "#58A6FF",        # Blue for client node
    "node_target": "#F85149",        # Red for target node
    "node_gatekeeper": "#D2A8FF",    # Purple for gatekeepers
    "edge_default": "#21262D",       # Very subtle edges
    "edge_path": "#3FB950",          # Green for highlighted paths
    "edge_facebook": "#1877F2",
    "edge_linkedin": "#0A66C2",
    "edge_twitter": "#1DA1F2",
    "edge_powermem": "#10B981",
    "text_primary": "#F0F6FC",
    "text_secondary": "#8B949E",
    "community_palette": [           # Distinct colors for communities
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
        "#BB8FCE", "#85C1E9", "#F8C471", "#82E0AA"
    ],
    "font_family": "sans-serif",
    "title_size": 18,
    "label_size": 8,
    "legend_size": 10
}

LIGHT_THEME = {
    "background": "#FFFFFF",
    "node_default": "#6B7280",
    "node_highlight": "#F59E0B",
    "node_client": "#2563EB",
    "node_target": "#DC2626",
    "node_gatekeeper": "#9333EA",
    "edge_default": "#E5E7EB",
    "edge_path": "#16A34A",
    "edge_facebook": "#1877F2",
    "edge_linkedin": "#0A66C2",
    "edge_twitter": "#1DA1F2",
    "edge_powermem": "#10B981",
    "text_primary": "#111827",
    "text_secondary": "#4B5563",
    "community_palette": DARK_THEME["community_palette"],
    "font_family": "sans-serif",
    "title_size": 18,
    "label_size": 8,
    "legend_size": 10
}
