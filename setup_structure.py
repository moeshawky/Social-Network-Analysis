import os

dirs = [
    "network_intelligence",
    "network_intelligence/graph",
    "network_intelligence/identity",
    "network_intelligence/data_sources",
    "network_intelligence/analysis",
    "network_intelligence/visualization",
    "network_intelligence/output",
    "tests",
    "tests/fixtures",
    "tests/fixtures/expected_outputs",
    "examples"
]

files = [
    "network_intelligence/__init__.py",
    "network_intelligence/graph/__init__.py",
    "network_intelligence/identity/__init__.py",
    "network_intelligence/data_sources/__init__.py",
    "network_intelligence/analysis/__init__.py",
    "network_intelligence/visualization/__init__.py",
    "network_intelligence/output/__init__.py",
    "tests/__init__.py"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created directory: {d}")

for f in files:
    with open(f, 'w') as file:
        pass
    print(f"Created file: {f}")
