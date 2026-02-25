"""
Unified person entity that spans platforms.
A single real-world person may have identities on Facebook, LinkedIn, Twitter, etc.
This model holds all of them and tracks which are confirmed vs inferred.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any

@dataclass
class PlatformIdentity:
    platform: str               # "facebook", "linkedin", "twitter", "powermem"
    handle: str                 # Platform-specific identifier
    display_name: str           # Name as shown on platform
    profile_url: str            # Full URL
    numeric_id: Optional[str]   # Platform numeric ID if available
    title: Optional[str]        # Professional title (primarily LinkedIn)
    company: Optional[str]      # Company association
    verified: bool              # Has this identity been confirmed?
    raw_data: Dict[str, Any]    # Original platform data preserved

@dataclass
class UnifiedEntity:
    entity_id: str              # Generated UUID
    canonical_name: str         # Best-guess real name
    identities: List[PlatformIdentity]
    platforms_present: Set[str]
    confidence_scores: Dict[str, float] = field(default_factory=dict)  # Per-identity-pair confidence
    overall_confidence: float = 0.0   # Aggregate confidence that all identities are same person
    merge_history: List[Dict[str, Any]] = field(default_factory=list)   # Audit trail of merges
    metadata: Dict[str, Any] = field(default_factory=dict)              # Arbitrary additional data
