import requests
import json
import time
from typing import List, Tuple, Dict, Any, Optional
from network_intelligence.identity.entity import PlatformIdentity
from network_intelligence import config

class PowerMemClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or config.POWERMEM_URL
        self.timeout = timeout or config.POWERMEM_TIMEOUT

    def health_check(self) -> bool:
        """Ping the PowerMem service."""
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def query(self, query: str, tags: List[str] = None, limit: int = 200) -> List[Dict]:
        """Query PowerMem for memories."""
        url = f"{self.base_url}/api/search"
        payload = {
            "query": query,
            "limit": limit
        }
        if tags:
            payload["tags"] = tags

        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("results", [])
        except requests.RequestException as e:
            # Log error
            print(f"PowerMem query failed: {e}")
            return []

    def load_company_graph(self, company: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Pull all people data for a company from PowerMem."""
        # Search for company name in content or metadata
        results = self.query(company, tags=[config.TAGS_PROFILE, config.TAGS_COMPANY_INTEL])

        identities = []
        edges = []

        for r in results:
            content = r.get("content", "")
            meta = r.get("metadata", {})

            # Assuming metadata holds structured info
            name = meta.get("name") or meta.get("person") or "Unknown"

            identities.append(PlatformIdentity(
                platform="powermem",
                handle=name.lower().replace(" ", "_"), # Generated handle
                display_name=name,
                profile_url="",
                numeric_id=r.get("id"), # PowerMem ID
                title=meta.get("title"),
                company=meta.get("company"),
                verified=True, # Trusted source
                raw_data=r
            ))

            # Check for relationships in metadata
            relationships = meta.get("relationships", [])
            for rel in relationships:
                edges.append({
                    "source": name,
                    "target": rel.get("target"),
                    "platform": "powermem",
                    "relationship": rel.get("type", "related"),
                    "weight": rel.get("weight", 1.0),
                    "source_data_origin": "powermem"
                })

        return identities, edges

    def write_analysis(self, content: str, tags: List[str], metadata: Dict[str, Any]) -> bool:
        """Store analysis results back to PowerMem."""
        url = f"{self.base_url}/api/memory"
        payload = {
            "content": content,
            "tags": tags,
            "metadata": metadata
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"PowerMem write failed: {e}")
            return False
