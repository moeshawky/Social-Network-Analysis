import argparse
import sys
import os
import logging
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from network_intelligence import config
from network_intelligence.identity.resolver import IdentityResolver
from network_intelligence.graph.builder import GraphBuilder
from network_intelligence.graph.exporter import GraphExporter
from network_intelligence.data_sources.edge_list import EdgeListLoader
from network_intelligence.data_sources.facebook import FacebookLoader
from network_intelligence.data_sources.linkedin import LinkedInLoader
from network_intelligence.data_sources.twitter import TwitterLoader
from network_intelligence.data_sources.powermem import PowerMemClient
from network_intelligence.data_sources.csv_loader import CSVLoader
from network_intelligence.analysis.centrality import CentralityAnalyzer
from network_intelligence.analysis.metrics import NetworkMetrics
from network_intelligence.analysis.community import CommunityDetector
from network_intelligence.analysis.pathfinding import PathFinder
from network_intelligence.analysis.platform_analysis import PlatformAnalyzer
from network_intelligence.visualization.graph_viz import NetworkVisualizer
from network_intelligence.visualization.community_viz import CommunityVisualizer
from network_intelligence.visualization.path_viz import PathVisualizer
from network_intelligence.visualization.centrality_viz import CentralityVisualizer
from network_intelligence.visualization.platform_viz import PlatformVisualizer
from network_intelligence.output.json_output import JSONOutputGenerator
from network_intelligence.output.markdown_output import MarkdownOutputGenerator
from network_intelligence.output.powermem_writer import PowerMemWriter

def main():
    parser = argparse.ArgumentParser(description="Network Intelligence Engine")

    # Data Sources
    parser.add_argument("--from-edge-list", help="Load from SNAP edge list file")
    parser.add_argument("--from-facebook", help="Load from Facebook data directory")
    parser.add_argument("--from-linkedin", help="Load from LinkedIn export directory")
    parser.add_argument("--from-twitter", help="Load from Twitter archive directory")
    parser.add_argument("--from-powermem", action="store_true", help="Load from PowerMem (requires --company)")
    parser.add_argument("--from-file", help="Load from generic CSV file")

    # Context
    parser.add_argument("--company", help="Target company context")
    parser.add_argument("--client", help="Client name (source node)")
    parser.add_argument("--target", help="Target name (target node)")

    # Operations
    parser.add_argument("--health-check", action="store_true", help="Check PowerMem connection")
    parser.add_argument("--resolve-identities", action="store_true", help="Run identity resolution explicitly")

    # Analysis
    parser.add_argument("--all-centrality", action="store_true", help="Compute all centrality measures")

    # Visualization
    parser.add_argument("--visualize", choices=["full", "communities", "path", "centrality", "platforms", "ego"], help="Generate visualization")
    parser.add_argument("--output-dir", default="./output", help="Directory for outputs")

    # Output
    parser.add_argument("--output-format", choices=["json", "markdown"], default="json", help="Output format")
    parser.add_argument("--write-to-powermem", action="store_true", help="Store analysis in PowerMem")

    args = parser.parse_args()

    # Ensure output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Health Check
    if args.health_check:
        client = PowerMemClient()
        status = client.health_check()
        print(f"PowerMem Service Status: {'ONLINE' if status else 'OFFLINE'}")
        return

    # Initialize components
    resolver = IdentityResolver()
    builder = GraphBuilder(resolver)

    # Load Data
    data_loaded = False

    if args.from_edge_list:
        loader = EdgeListLoader()
        # If filename matches standard SNAP name, use ensure_dataset logic inside loader if path is simple name
        nodes, edges = loader.load(args.from_edge_list)
        builder.add_data_source(nodes, edges, "facebook_snap")
        data_loaded = True

    if args.from_facebook:
        loader = FacebookLoader()
        nodes, edges = loader.load_data_export(args.from_facebook)
        builder.add_data_source(nodes, edges, "facebook")
        data_loaded = True

    if args.from_linkedin:
        loader = LinkedInLoader()
        nodes, edges = loader.load_export(args.from_linkedin)
        builder.add_data_source(nodes, edges, "linkedin")
        data_loaded = True

    if args.from_twitter:
        loader = TwitterLoader()
        nodes, edges = loader.load_archive(args.from_twitter)
        builder.add_data_source(nodes, edges, "twitter")
        data_loaded = True

    if args.from_powermem and args.company:
        client = PowerMemClient()
        nodes, edges = client.load_company_graph(args.company)
        builder.add_data_source(nodes, edges, "powermem")
        data_loaded = True

    if args.from_file:
        loader = CSVLoader()
        nodes, edges = loader.load(args.from_file)
        builder.add_data_source(nodes, edges, "csv")
        data_loaded = True

    if not data_loaded:
        logger.warning("No data sources specified or loaded.")
        if not args.health_check:
            parser.print_help()
        return

    # Build Graph
    logger.info("Building graph...")
    G = builder.build()
    simple_G = builder.get_simplified_graph()
    logger.info(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    if G.number_of_nodes() == 0:
        logger.error("Graph is empty.")
        return

    # Analysis results container
    results = {
        "company": args.company,
        "graph_stats": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges()
        }
    }

    # Run Analysis
    logger.info("Running analysis...")

    # Metrics
    metrics_analyzer = NetworkMetrics()
    results["metrics"] = metrics_analyzer.compute_all(simple_G)

    # Centrality
    cent_analyzer = CentralityAnalyzer()
    results["centrality"] = cent_analyzer.compute_all(simple_G)
    results["gatekeepers"] = cent_analyzer.find_gatekeepers(simple_G)

    # Communities
    comm_detector = CommunityDetector()
    comm_results = comm_detector.detect_communities(simple_G, method="greedy_modularity") # Default fast
    results["communities"] = comm_results

    # Path Analysis
    if args.client and args.target:
        logger.info(f"Finding path from {args.client} to {args.target}...")
        # Need to find node IDs for names
        # Simple lookup in builder.handle_map?
        # Or search in G nodes
        # Let's search by canonical name or handle

        # Helper to find node by name
        def find_node(name):
            for n, attrs in G.nodes(data=True):
                if attrs.get("canonical_name") == name or name in attrs.get("platforms", []): # unlikely
                     return n
                # Check handle map from builder if accessible? No, cleaner to search graph attrs
            # Fallback: check if name is in node IDs
            if G.has_node(name): return name
            return None

        src_id = find_node(args.client)
        tgt_id = find_node(args.target)

        if src_id and tgt_id:
            path_finder = PathFinder()
            path_res = path_finder.find_shortest_weighted_path(G, src_id, tgt_id) # Using MultiGraph for pathfinding
            chain_res = path_finder.generate_introduction_chain(G, src_id, tgt_id)

            results["path_analysis"] = {
                "source": args.client,
                "target": args.target,
                "path_found": path_res["found"],
                "path_details": path_res,
                "introduction_chain": chain_res
            }
        else:
            logger.warning(f"Could not find client '{args.client}' or target '{args.target}' in graph.")
            results["path_analysis"] = {"error": "Nodes not found"}

    # Visualization
    if args.visualize:
        logger.info(f"Generating visualization: {args.visualize}...")
        viz_path = os.path.join(args.output_dir, f"{args.visualize}_viz.png")

        if args.visualize == "full":
            viz = NetworkVisualizer()
            viz.visualize_full_network(simple_G, output_path=viz_path, title=f"Network: {args.company or 'Full'}")

        elif args.visualize == "communities":
            viz = CommunityVisualizer()
            viz.visualize_communities(simple_G, comm_results["partition"], output_path=viz_path)

        elif args.visualize == "path" and "path_analysis" in results and "introduction_chain" in results["path_analysis"]:
            viz = PathVisualizer()
            path = results["path_analysis"]["introduction_chain"].get("path", [])
            viz.visualize_path(simple_G, path, output_path=viz_path)

        elif args.visualize == "centrality":
            viz = CentralityVisualizer()
            viz.visualize_bar_chart(results["centrality"]["eigenvector"], output_path=viz_path, title="Top Influencers (Eigenvector)")

        elif args.visualize == "platforms":
            viz = PlatformVisualizer()
            viz.visualize_platform_subgraphs(G, output_path=viz_path)

        logger.info(f"Visualization saved to {viz_path}")
        results.setdefault("visualizations", []).append(viz_path)

    # Output Generation
    if args.output_format == "json":
        gen = JSONOutputGenerator()
        out_path = os.path.join(args.output_dir, "analysis_output.json")
        gen.generate(results, out_path)
        logger.info(f"JSON output saved to {out_path}")
        print(gen.generate(results)) # Print to stdout

    elif args.output_format == "markdown":
        gen = MarkdownOutputGenerator()
        out_path = os.path.join(args.output_dir, "analysis_briefing.md")
        gen.generate(results, out_path)
        logger.info(f"Markdown output saved to {out_path}")
        print(gen.generate(results))

    # Write to PowerMem
    if args.write_to_powermem:
        writer = PowerMemWriter()
        success = writer.write_analysis_results(results)
        if success:
            logger.info("Successfully wrote analysis to PowerMem.")
        else:
            logger.error("Failed to write to PowerMem.")

if __name__ == "__main__":
    main()
