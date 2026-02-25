import matplotlib.pyplot as plt
import networkx as nx
from network_intelligence.visualization.graph_viz import NetworkVisualizer
from network_intelligence.analysis.platform_analysis import PlatformAnalyzer
from network_intelligence import config

class PlatformVisualizer:
    def __init__(self):
        self.viz = NetworkVisualizer()
        self.analyzer = PlatformAnalyzer()

    def visualize_platform_overlay(self, G: nx.Graph, output_path: str = None) -> plt.Figure:
        """Full network with edges colored by platform."""
        # Already handled by default visualizer
        return self.viz.visualize_full_network(
            G,
            output_path=output_path,
            title="Cross-Platform Network Overlay"
        )

    def visualize_platform_subgraphs(self, G: nx.MultiGraph, output_path: str = None) -> plt.Figure:
        """Side-by-side comparison of platforms."""
        platforms = ["facebook", "linkedin", "twitter", "powermem"]
        present_platforms = []

        # Check which platforms have data
        # Quick check on edges
        for u, v, k, data in G.edges(keys=True, data=True):
            p = data.get("platform")
            if p and p not in present_platforms and p in platforms:
                present_platforms.append(p)

        if not present_platforms:
            return None

        fig, axes = plt.subplots(1, len(present_platforms), figsize=(6 * len(present_platforms), 6))
        if len(present_platforms) == 1:
            axes = [axes]

        fig.patch.set_facecolor(self.viz.theme["background"])

        for i, plt_name in enumerate(present_platforms):
            ax = axes[i]
            ax.set_facecolor(self.viz.theme["background"])

            subG = self.analyzer._get_platform_subgraph(G, plt_name)

            # Draw using simplified nx.draw for subplot
            pos = nx.spring_layout(subG, k=0.3, seed=42)

            edge_color = self.viz.theme.get(f"edge_{plt_name}", self.viz.theme["edge_default"])

            nx.draw_networkx_nodes(subG, pos, node_size=50, node_color=self.viz.theme["node_default"], ax=ax, alpha=0.8)
            nx.draw_networkx_edges(subG, pos, edge_color=edge_color, alpha=0.5, ax=ax)

            ax.set_title(f"{plt_name.capitalize()} Network", color=self.viz.theme["text_primary"])
            ax.axis('off')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=config.VIZ_DPI)

        return fig
