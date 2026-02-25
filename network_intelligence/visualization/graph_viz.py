import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List, Any, Optional
from network_intelligence.visualization.styles import DARK_THEME, LIGHT_THEME
from network_intelligence import config

class NetworkVisualizer:
    def __init__(self, theme: str = "dark"):
        self.theme = DARK_THEME if theme == "dark" else LIGHT_THEME

    def _setup_plot(self, figsize):
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(self.theme["background"])
        ax.set_facecolor(self.theme["background"])
        return fig, ax

    def visualize_full_network(self, G: nx.Graph, highlight_nodes: Dict[str, str] = None,
                                highlight_path: List[str] = None, output_path: str = None,
                                title: str = "Network Visualization") -> plt.Figure:

        # Large graph handling: Subgraph if > 500 nodes
        if G.number_of_nodes() > 500:
            # Keep top nodes by degree + highlighted nodes + path nodes
            top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:300]
            nodes_to_keep = set([n for n, d in top_nodes])
            if highlight_nodes:
                nodes_to_keep.update(highlight_nodes.keys())
            if highlight_path:
                nodes_to_keep.update(highlight_path)

            subG = G.subgraph(nodes_to_keep)
        else:
            subG = G

        fig, ax = self._setup_plot(config.VIZ_FIGSIZE_MEDIUM)

        pos = nx.spring_layout(subG, k=0.15, iterations=50, seed=42)

        # Node sizes
        degrees = dict(subG.degree())
        node_sizes = [v * 10 + 20 for v in degrees.values()]

        # Node colors
        # If community info is in node attributes, use it
        # Else use default
        node_colors = []
        for node in subG.nodes():
            if highlight_nodes and node in highlight_nodes:
                # Custom highlight type map to color
                h_type = highlight_nodes[node]
                if h_type == "client": color = self.theme["node_client"]
                elif h_type == "target": color = self.theme["node_target"]
                elif h_type == "gatekeeper": color = self.theme["node_gatekeeper"]
                else: color = self.theme["node_highlight"]
            elif highlight_path and node in highlight_path:
                 color = self.theme["node_highlight"]
            else:
                # Community color
                comm_id = subG.nodes[node].get("community_id")
                if comm_id is not None:
                    color = self.theme["community_palette"][comm_id % len(self.theme["community_palette"])]
                else:
                    color = self.theme["node_default"]
            node_colors.append(color)

        # Draw edges
        edge_colors = []
        edge_widths = []
        path_edges = []
        if highlight_path:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))

        for u, v, data in subG.edges(data=True):
            if highlight_path and ((u, v) in path_edges or (v, u) in path_edges):
                edge_colors.append(self.theme["edge_path"])
                edge_widths.append(2.0)
            else:
                # Platform color
                plt_name = data.get("platform")
                if plt_name == "facebook": c = self.theme["edge_facebook"]
                elif plt_name == "linkedin": c = self.theme["edge_linkedin"]
                elif plt_name == "twitter": c = self.theme["edge_twitter"]
                elif plt_name == "powermem": c = self.theme["edge_powermem"]
                else: c = self.theme["edge_default"]
                edge_colors.append(c)
                edge_widths.append(0.5)

        nx.draw_networkx_edges(subG, pos, edge_color=edge_colors, width=edge_widths, alpha=0.6, ax=ax)
        nx.draw_networkx_nodes(subG, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, ax=ax)

        # Labels for top nodes only
        top_degree_sub = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:15]
        labels = {n: subG.nodes[n].get("canonical_name", str(n)) for n, d in top_degree_sub}

        # Always label highlighted nodes
        if highlight_nodes:
            for n in highlight_nodes:
                if n in subG:
                     labels[n] = subG.nodes[n].get("canonical_name", str(n))

        nx.draw_networkx_labels(subG, pos, labels, font_size=self.theme["label_size"],
                                font_color=self.theme["text_primary"], ax=ax)

        ax.set_title(title, fontsize=self.theme["title_size"], color=self.theme["text_primary"])
        ax.axis('off')

        if output_path:
            plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=config.VIZ_DPI, bbox_inches='tight')

        return fig

    def visualize_ego_network(self, G: nx.Graph, center_node: str, radius: int = 2,
                               output_path: str = None) -> plt.Figure:
        """Show only nodes within N hops of a center node."""
        if center_node not in G:
            return None

        subG = nx.ego_graph(G, center_node, radius=radius)

        return self.visualize_full_network(
            subG,
            highlight_nodes={center_node: "target"},
            output_path=output_path,
            title=f"Ego Network: {G.nodes[center_node].get('canonical_name', center_node)} (Radius {radius})"
        )
