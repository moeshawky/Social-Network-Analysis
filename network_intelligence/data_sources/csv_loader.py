import csv
import os
from typing import List, Tuple, Dict, Any
from network_intelligence.identity.entity import PlatformIdentity

class CSVLoader:
    def load(self, filepath: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """
        Generic CSV loader.
        Expects columns: source, target, relationship, weight, platform
        OR
        id, name, title, company, platform
        """
        if not os.path.exists(filepath):
            return [], []

        identities = []
        edges = []

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            for row in reader:
                # Relationship format
                if "source" in headers and "target" in headers:
                    edges.append({
                        "source": row["source"],
                        "target": row["target"],
                        "platform": row.get("platform", "csv"),
                        "relationship": row.get("relationship", "connected"),
                        "weight": float(row.get("weight", 1.0)),
                        "source_data_origin": filepath
                    })

                # Identity format
                if "id" in headers or "name" in headers:
                    identities.append(PlatformIdentity(
                        platform=row.get("platform", "csv"),
                        handle=row.get("id") or row.get("name"),
                        display_name=row.get("name") or row.get("id"),
                        profile_url=row.get("url", ""),
                        numeric_id=row.get("numeric_id"),
                        title=row.get("title"),
                        company=row.get("company"),
                        verified=False,
                        raw_data=row
                    ))

        return identities, edges
