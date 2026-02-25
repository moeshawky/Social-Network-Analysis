import json
import os
import csv
from typing import List, Tuple, Dict, Any
from network_intelligence.identity.entity import PlatformIdentity

class LinkedInLoader:
    def load_export(self, directory: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load LinkedIn data export CSV files."""
        # Connections.csv usually contains: First Name, Last Name, Email Address, Company, Position, Connected On
        filepath = os.path.join(directory, "Connections.csv")
        if not os.path.exists(filepath):
            return [], []

        identities = []
        edges = []

        with open(filepath, 'r', encoding='utf-8') as f:
            # Skip first 3 lines if LinkedIn export includes header info
            # Usually header is line 4
            reader = csv.DictReader(f)

            for row in reader:
                first_name = row.get("First Name", "")
                last_name = row.get("Last Name", "")
                full_name = f"{first_name} {last_name}".strip()
                company = row.get("Company", "")
                title = row.get("Position", "")
                email = row.get("Email Address", "")

                identities.append(PlatformIdentity(
                    platform="linkedin",
                    handle=email if email else full_name.lower().replace(" ", "."),
                    display_name=full_name,
                    profile_url="", # Export doesn't include URL
                    numeric_id=None,
                    title=title,
                    company=company,
                    verified=False, # Imported connections are just connections
                    raw_data=row
                ))

                # Assume self connection (need self identity passed in ideally)
                pass

        return identities, edges

    def load_scraped(self, filepath: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load scraped LinkedIn profile data (JSON)."""
        if not os.path.exists(filepath):
            return [], []

        with open(filepath, 'r') as f:
            profiles = json.load(f)

        identities = []
        edges = []

        # Determine if list or single object
        if isinstance(profiles, dict):
            profiles = [profiles]

        for p in profiles:
            identities.append(PlatformIdentity(
                platform="linkedin",
                handle=p.get("public_identifier") or p.get("urn_id") or p.get("name"),
                display_name=p.get("name"),
                profile_url=p.get("url", ""),
                numeric_id=p.get("urn_id"), # usually urn:li:fs_miniProfile:<id>
                title=p.get("occupation") or p.get("headline"),
                company=p.get("company"), # scraping structure varies
                verified=False,
                raw_data=p
            ))

            # Connections if available
            for connection in p.get("connections", []):
                # Add edge
                edges.append({
                    "source": p.get("urn_id") or p.get("name"),
                    "target": connection.get("urn_id") or connection.get("name"),
                    "platform": "linkedin",
                    "relationship": "connected",
                    "weight": 1.5,
                    "source_data_origin": filepath
                })

        return identities, edges
