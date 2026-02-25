import uuid
from typing import List, Dict, Tuple, Optional
from network_intelligence.identity.entity import PlatformIdentity, UnifiedEntity
from network_intelligence.identity.normalizer import NameNormalizer
from network_intelligence.identity.confidence import ConfidenceScorer

class IdentityResolver:
    def __init__(self):
        self.normalizer = NameNormalizer()
        self.scorer = ConfidenceScorer()
        self.review_queue = []

    def resolve(self, identities: List[PlatformIdentity]) -> List[UnifiedEntity]:
        """Main resolution pipeline."""
        self.review_queue = [] # Reset queue for new resolution run
        unified_entities: List[UnifiedEntity] = []

        # Initial blocking
        blocks = self.block_by_name(identities)

        for block_key, block_identities in blocks.items():
            if not block_identities:
                continue

            # Within each block, compare pairs.
            # We treat the block as a set of candidates to be clustered.
            # Simple greedy clustering:
            # 1. Take an identity
            # 2. Compare against all existing clusters (unified entities)
            # 3. Find best match above threshold
            # 4. If found, merge. Else create new cluster.

            local_entities: List[UnifiedEntity] = []

            for identity in block_identities:
                best_match_entity = None
                best_score = 0.0

                for entity in local_entities:
                    # Compare new identity with existing unified entity
                    # In a real system, we'd compare against all identities in the entity
                    # For now, let's just pick the first identity in the entity as representative
                    rep_identity = entity.identities[0]
                    score = self.compare_pair(rep_identity, identity)

                    if score > best_score:
                        best_score = score
                        best_match_entity = entity

                if best_match_entity:
                    if best_score >= 0.90:
                        # Auto-merge
                        self.merge_entities(best_match_entity, identity, best_score)
                        continue
                    elif best_score >= 0.50:
                        # Flag for review
                        self.review_queue.append({
                            "type": "potential_merge",
                            "entity_id": best_match_entity.entity_id,
                            "entity_name": best_match_entity.canonical_name,
                            "new_identity_handle": identity.handle,
                            "new_identity_platform": identity.platform,
                            "score": best_score
                        })

                # If not merged (even if flagged), create new entity
                new_entity = UnifiedEntity(
                        entity_id=str(uuid.uuid4()),
                        canonical_name=identity.display_name, # or normalized
                        identities=[identity],
                        platforms_present={identity.platform},
                        confidence_scores={},
                        overall_confidence=1.0,
                        merge_history=[]
                    )
                    local_entities.append(new_entity)

            unified_entities.extend(local_entities)

        return unified_entities

    def compare_pair(self, a: PlatformIdentity, b: PlatformIdentity) -> float:
        """Compare two identities, return confidence score 0.0-1.0."""
        # Calculate signals
        name_sim = self.normalizer.similarity(a.display_name, b.display_name)

        handle_sim = 0.0
        if a.handle and b.handle:
             if a.handle == b.handle:
                 handle_sim = 1.0
             elif a.handle in b.handle or b.handle in a.handle:
                 handle_sim = 0.8

        company_match = 0.0
        if a.company and b.company:
            comp_a = self.normalizer.normalize(a.company)
            comp_b = self.normalizer.normalize(b.company)
            if comp_a and comp_b and comp_a == comp_b:
                company_match = 1.0

        title_match = 0.0
        if a.title and b.title:
             tit_a = self.normalizer.normalize(a.title)
             tit_b = self.normalizer.normalize(b.title)
             if tit_a and tit_b and tit_a == tit_b:
                 title_match = 1.0

        # Signals dictionary
        signals = {
            "name_similarity": name_sim,
            "handle_similarity": handle_sim,
        }

        # Only include signals if they carry information (positive or negative check possible)
        # But here we only have positive matches.
        # If we include 0.0 for missing company, it penalizes.
        # Let's include them only if we actually compared them (i.e. both had data)
        # BUT, if we have different companies, we want to penalize (score 0).
        # So:
        if a.company and b.company:
            signals["company_match"] = company_match

        if a.title and b.title:
            signals["title_match"] = title_match

        # mutual_connections is not implemented yet, so excluding it allows
        # the score to normalize over the other weights (e.g. 0.75 total weight).
        # This makes auto-merge possible for perfect profile matches.

        return self.scorer.score(signals)

    def block_by_name(self, identities: List[PlatformIdentity]) -> Dict[str, List[PlatformIdentity]]:
        """Group identities into comparison blocks to reduce O(n²)."""
        blocks: Dict[str, List[PlatformIdentity]] = {}
        for identity in identities:
            normalized_name = self.normalizer.normalize(identity.display_name)
            if not normalized_name:
                key = "unknown"
            else:
                parts = normalized_name.split()
                # Block by first 3 chars of last name, or whole name if short
                if len(parts) > 1:
                    last_name = parts[-1]
                    key = last_name[:3]
                else:
                    key = normalized_name[:3]

            if key not in blocks:
                blocks[key] = []
            blocks[key].append(identity)
        return blocks

    def merge_entities(self, entity: UnifiedEntity, new_identity: PlatformIdentity, confidence: float) -> UnifiedEntity:
        """Add a new identity to an existing entity."""
        entity.identities.append(new_identity)
        entity.platforms_present.add(new_identity.platform)

        # Store the confidence score for this merge
        # Key could be tuple of (existing_id, new_id) or just a simple list append
        # Using a simple list of merges in merge_history
        entity.merge_history.append({
            "action": "merge",
            "added_identity_handle": new_identity.handle,
            "added_identity_platform": new_identity.platform,
            "confidence": confidence
        })

        # Update overall confidence (simple average for now)
        # In a real system this would be more complex
        current_conf = entity.overall_confidence
        # Weighted average towards the new confidence?
        # Let's just keep it simple: min of all merge confidences
        if confidence < current_conf:
            entity.overall_confidence = confidence

        return entity

    def export_review_queue(self) -> List[Dict]:
        """Export all provisional matches (0.50-0.89) for manual review."""
        return self.review_queue
