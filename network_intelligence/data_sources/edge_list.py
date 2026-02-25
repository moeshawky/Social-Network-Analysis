import os
import urllib.request
import gzip
import shutil
from typing import List, Tuple, Dict
from network_intelligence.identity.entity import PlatformIdentity

class EdgeListLoader:
    SNAP_URL = "https://snap.stanford.edu/data/facebook_combined.txt.gz"
    FILENAME_GZ = "facebook_combined.txt.gz"
    FILENAME_TXT = "facebook_combined.txt"

    def ensure_dataset(self) -> str:
        """Download SNAP Facebook dataset if not present."""
        if not os.path.exists(self.FILENAME_TXT):
            print(f"Downloading {self.FILENAME_GZ}...")
            urllib.request.urlretrieve(self.SNAP_URL, self.FILENAME_GZ)

            print(f"Extracting {self.FILENAME_GZ}...")
            with gzip.open(self.FILENAME_GZ, 'rb') as f_in:
                with open(self.FILENAME_TXT, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("Done.")
        else:
            print("Dataset already exists.")
        return self.FILENAME_TXT

    def load(self, filepath: str = None) -> Tuple[List[PlatformIdentity], List[Dict]]:
        """
        Load SNAP-format edge list. Returns (nodes, edges).
        SNAP format: node_id node_id
        """
        if filepath is None:
            filepath = self.ensure_dataset()

        identities = []
        edges = []
        seen_nodes = set()

        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue

                u, v = parts[0], parts[1]

                # Create identities if new
                if u not in seen_nodes:
                    identities.append(PlatformIdentity(
                        platform="facebook_snap",
                        handle=u,
                        display_name=f"Node {u}",
                        profile_url=f"http://facebook.com/{u}", # Fake URL
                        numeric_id=u,
                        title=None,
                        company=None,
                        verified=False,
                        raw_data={"id": u}
                    ))
                    seen_nodes.add(u)

                if v not in seen_nodes:
                    identities.append(PlatformIdentity(
                        platform="facebook_snap",
                        handle=v,
                        display_name=f"Node {v}",
                        profile_url=f"http://facebook.com/{v}", # Fake URL
                        numeric_id=v,
                        title=None,
                        company=None,
                        verified=False,
                        raw_data={"id": v}
                    ))
                    seen_nodes.add(v)

                edges.append({
                    "source": u,
                    "target": v,
                    "platform": "facebook_snap",
                    "relationship": "friend",
                    "weight": 1.0,
                    "source_data_origin": filepath
                })

        return identities, edges
