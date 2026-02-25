import json
import os
from typing import List, Tuple, Dict, Generator, Any
from network_intelligence.identity.entity import PlatformIdentity

class FacebookLoader:
    def load_edge_list(self, filepath: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load SNAP-format edge list. Returns (nodes, edges)."""
        identities = []
        edges = []
        seen_nodes = set()

        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue
                u, v = parts[0], parts[1]

                for node_id in [u, v]:
                    if node_id not in seen_nodes:
                        identities.append(PlatformIdentity(
                            platform="facebook",
                            handle=node_id,
                            display_name=f"User {node_id}",
                            profile_url=f"https://facebook.com/{node_id}",
                            numeric_id=node_id,
                            title=None,
                            company=None,
                            verified=False,
                            raw_data={"id": node_id}
                        ))
                        seen_nodes.add(node_id)

                edges.append({
                    "source": u,
                    "target": v,
                    "platform": "facebook",
                    "relationship": "friend",
                    "weight": 1.0,
                    "source_data_origin": filepath
                })
        return identities, edges

    def load_data_export(self, directory: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load Facebook 'Download Your Information' export (JSON)."""
        # Placeholder for actual JSON structure parsing
        # friends.json usually contains list of friends
        filepath = os.path.join(directory, "friends_and_followers/friends.json")
        if not os.path.exists(filepath):
            return [], []

        identities = []
        edges = []

        with open(filepath, 'r') as f:
            data = json.load(f)

        friends = data.get("friends_v2", [])
        for friend in friends:
            name = friend.get("name", "Unknown")
            # timestamp = friend.get("timestamp")

            identities.append(PlatformIdentity(
                platform="facebook",
                handle=name, # Using name as handle if no ID
                display_name=name,
                profile_url="",
                numeric_id=None,
                title=None,
                company=None,
                verified=True, # Assuming export is verified
                raw_data=friend
            ))

            # Edges assume "self" is the owner of the export
            # We don't have "self" info easily unless provided
            pass

        return identities, edges

    def load_scraped_profiles(self, filepath: str) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """Load JSON of scraped profiles."""
        with open(filepath, 'r') as f:
            profiles = json.load(f)

        identities = []
        edges = []

        for p in profiles:
            identities.append(PlatformIdentity(
                platform="facebook",
                handle=p.get("id") or p.get("username") or p.get("name"),
                display_name=p.get("name"),
                profile_url=p.get("url", ""),
                numeric_id=p.get("id"),
                title=p.get("work", [{}])[0].get("position") if p.get("work") else None,
                company=p.get("work", [{}])[0].get("company") if p.get("work") else None,
                verified=False,
                raw_data=p
            ))

            # Assume friends list in profile
            for friend in p.get("friends", []):
                edges.append({
                    "source": p.get("id") or p.get("name"),
                    "target": friend.get("id") or friend.get("name"),
                    "platform": "facebook",
                    "relationship": "friend",
                    "weight": 1.0,
                    "source_data_origin": filepath
                })

        return identities, edges

    def load_chunked(self, filepath: str, chunk_size: int = None, resume_from: int = 0) -> Generator[Tuple[List[PlatformIdentity], List[Dict]], None, None]:
        """Generator that yields chunks for massive files."""
        # Simplified implementation for line-based files like edge lists or NDJSON
        count = 0
        chunk_identities = []
        chunk_edges = []

        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if i < resume_from:
                    continue

                # Assume edge list format for chunking example
                parts = line.strip().split()
                if len(parts) == 2:
                    u, v = parts
                    chunk_edges.append({
                        "source": u,
                        "target": v,
                        "platform": "facebook",
                        "relationship": "friend",
                        "weight": 1.0,
                        "source_data_origin": filepath
                    })
                    # Add identities logic (omitted for brevity in chunking, usually handled by checking existence)

                count += 1
                if chunk_size and count >= chunk_size:
                    yield chunk_identities, chunk_edges
                    chunk_identities = []
                    chunk_edges = []
                    count = 0

            if chunk_edges:
                yield chunk_identities, chunk_edges

    def save_checkpoint(self, filepath: str, state: Dict[str, Any]) -> None:
        """Save processing checkpoint for resumable loading."""
        with open(filepath, 'w') as f:
            json.dump(state, f)

    def load_checkpoint(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load previous checkpoint if exists."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
