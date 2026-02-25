import unicodedata
import re
from difflib import SequenceMatcher

class NameNormalizer:
    SUFFIXES = {
        "jr", "sr", "iii", "phd", "pmp", "mba", "pe", "cpa", "eng", "esq"
    }
    PREFIXES = {
        "dr", "mr", "mrs", "ms", "prof", "eng", "arch"
    }

    def normalize(self, name: str) -> str:
        """Canonical normalized form."""
        if not name:
            return ""

        # Unicode normalization
        normalized = unicodedata.normalize('NFKD', name)

        # Lowercase and strip
        normalized = normalized.lower().strip()

        # Remove punctuation (keep spaces and hyphens if meaningful, but for now simple)
        normalized = re.sub(r'[^\w\s]', '', normalized)

        parts = normalized.split()

        # Strip prefixes and suffixes
        cleaned_parts = []
        for part in parts:
            if part not in self.PREFIXES and part not in self.SUFFIXES:
                cleaned_parts.append(part)

        return " ".join(cleaned_parts)

    def generate_variants(self, name: str) -> list[str]:
        """All plausible variants of this name."""
        norm_name = self.normalize(name)
        parts = norm_name.split()
        variants = {norm_name}

        if len(parts) > 1:
            # First Last
            variants.add(f"{parts[0]} {parts[-1]}")
            # Last, First (handled by set if normalized)
            # variants.add(f"{parts[-1]} {parts[0]}") # Usually we want canonical "First Last"

            if len(parts) > 2:
                # First M. Last
                variants.add(f"{parts[0]} {parts[1][0]} {parts[-1]}")
                # F. Last
                variants.add(f"{parts[0][0]} {parts[-1]}")

        # Hyphen handling
        if "-" in name:
             variants.add(name.replace("-", " "))
             # Split parts
             subparts = name.replace("-", " ").split()
             variants.add(f"{subparts[0]} {subparts[-1]}")

        return list(variants)

    def similarity(self, name_a: str, name_b: str) -> float:
        """Similarity score 0.0-1.0 between two names."""
        norm_a = self.normalize(name_a)
        norm_b = self.normalize(name_b)

        if not norm_a or not norm_b:
            return 0.0

        if norm_a == norm_b:
            return 1.0

        # Jaro-Winkler or Levenshtein. Using SequenceMatcher (Ratcliff/Obershelp) for simplicity/std lib
        return SequenceMatcher(None, norm_a, norm_b).ratio()
