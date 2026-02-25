"""
Configuration with sensible defaults.
All values overridable via environment variables.
"""
import os

# PowerMem
POWERMEM_URL = os.getenv("POWERMEM_URL", "http://127.0.0.1:43117")
POWERMEM_TIMEOUT = int(os.getenv("POWERMEM_TIMEOUT", "10"))

# Centrality
EIGENVECTOR_MAX_ITER = int(os.getenv("EIGENVECTOR_MAX_ITER", "1000"))
EIGENVECTOR_TOLERANCE = float(os.getenv("EIGENVECTOR_TOLERANCE", "1e-06"))

# Community
MIN_COMMUNITY_SIZE = int(os.getenv("MIN_COMMUNITY_SIZE", "2"))

# Output
TOP_N_RESULTS = int(os.getenv("TOP_N_RESULTS", "10"))
JSON_INDENT = int(os.getenv("JSON_INDENT", "2"))

# Identity Resolution
IDENTITY_CONFIDENCE_THRESHOLD = float(os.getenv("IDENTITY_CONFIDENCE_THRESHOLD", "0.70"))
IDENTITY_AUTO_MERGE_THRESHOLD = float(os.getenv("IDENTITY_AUTO_MERGE_THRESHOLD", "0.90"))
IDENTITY_MANUAL_REVIEW_THRESHOLD = float(os.getenv("IDENTITY_MANUAL_REVIEW_THRESHOLD", "0.50"))

# Visualization
VIZ_OUTPUT_DIR = os.getenv("VIZ_OUTPUT_DIR", "./output/visualizations")
VIZ_DPI = int(os.getenv("VIZ_DPI", "200"))
VIZ_DARK_MODE = os.getenv("VIZ_DARK_MODE", "true").lower() == "true"
VIZ_FIGSIZE_LARGE = (24, 18)
VIZ_FIGSIZE_MEDIUM = (16, 12)
VIZ_FIGSIZE_SMALL = (12, 8)

# Platform colors (consistent across all visualizations)
PLATFORM_COLORS = {
    "facebook": "#1877F2",
    "linkedin": "#0A66C2",
    "twitter": "#1DA1F2",
    "powermem": "#10B981",
    "inferred": "#6B7280",
    "multi_platform": "#F59E0B"
}

# PowerMem tags
TAGS_DECISION_MAKER = "decision-maker"
TAGS_COMPANY_INTEL = "company-intel"
TAGS_PROFILE = "profile"
TAGS_ENUMERATED = "enumerated"
TAGS_CONTACT_VERIFIED = "contact-verified"
TAGS_NETWORK_PROXIMITY = "network-proximity"
TAGS_NETWORK_ANALYSIS = "network-analysis"

# Large dataset processing
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "50000"))
PROGRESS_REPORT_INTERVAL = int(os.getenv("PROGRESS_REPORT_INTERVAL", "10000"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
