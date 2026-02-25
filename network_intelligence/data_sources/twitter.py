import json
import os
from typing import List, Tuple, Dict, Any
from network_intelligence.identity.entity import PlatformIdentity

class TwitterLoader:
    def load_archive(self, directory: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load Twitter data archive."""
        # following.js usually contains list of following
        # data/following.js
        # Needs stripping "window.YTD.following.part0 = "

        filepath = os.path.join(directory, "data/following.js")
        if not os.path.exists(filepath):
            return [], []

        identities = []
        edges = []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove JS wrapper
            start_index = content.find('[')
            if start_index != -1:
                json_data = json.loads(content[start_index:])
            else:
                return [], []

        for item in json_data:
            following = item.get("following", {})
            account_id = following.get("accountId")
            user_link = following.get("userLink") # usually https://twitter.com/Handle
            handle = user_link.split('/')[-1] if user_link else f"id_{account_id}"

            identities.append(PlatformIdentity(
                platform="twitter",
                handle=handle,
                display_name=handle, # Archive often just gives ID/Link
                profile_url=user_link,
                numeric_id=account_id,
                title=None,
                company=None,
                verified=False,
                raw_data=following
            ))

            # Edges assume self is source
            pass

        return identities, edges

    def load_scraped(self, filepath: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load scraped Twitter data (JSON)."""
        if not os.path.exists(filepath):
            return [], []

        with open(filepath, 'r') as f:
            data = json.load(f)

        identities = []
        edges = []

        if isinstance(data, dict):
            data = [data]

        for p in data:
            handle = p.get("screen_name") or p.get("username")
            identities.append(PlatformIdentity(
                platform="twitter",
                handle=handle,
                display_name=p.get("name"),
                profile_url=f"https://twitter.com/{handle}",
                numeric_id=str(p.get("id")),
                title=p.get("description"), # Bio as title proxy
                company=None,
                verified=p.get("verified", False),
                raw_data=p
            ))

            # Followers/Following if present
            for f_user in p.get("following", []):
                edges.append({
                    "source": handle,
                    "target": f_user.get("screen_name") or f_user.get("username"),
                    "platform": "twitter",
                    "relationship": "follows",
                    "weight": 1.0,
                    "source_data_origin": filepath
                })

        return identities, edges
