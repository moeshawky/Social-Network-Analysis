import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any
from network_intelligence.visualization.styles import DARK_THEME, LIGHT_THEME
from network_intelligence import config

class CentralityVisualizer:
    def __init__(self, theme: str = "dark"):
        self.theme = DARK_THEME if theme == "dark" else LIGHT_THEME

    def visualize_bar_chart(self, centrality_results: List[Dict], output_path: str = None,
                            title: str = "Centrality Distribution") -> plt.Figure:
        """Top 10 bar chart."""
        data = centrality_results[:10]
        nodes = [d["node"] for d in data]
        scores = [d["score"] for d in data]

        fig, ax = plt.subplots(figsize=config.VIZ_FIGSIZE_SMALL)
        fig.patch.set_facecolor(self.theme["background"])
        ax.set_facecolor(self.theme["background"])

        y_pos = np.arange(len(nodes))
        bars = ax.barh(y_pos, scores, align='center', color=self.theme["node_highlight"])

        ax.set_yticks(y_pos)
        ax.set_yticklabels(nodes, color=self.theme["text_primary"])
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Score', color=self.theme["text_secondary"])
        ax.set_title(title, color=self.theme["text_primary"], fontsize=self.theme["title_size"])

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.theme["text_secondary"])
        ax.spines['left'].set_color(self.theme["text_secondary"])
        ax.tick_params(axis='x', colors=self.theme["text_secondary"])

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=config.VIZ_DPI)

        return fig

    def visualize_radar_chart(self, person_comparison: Dict[str, Dict[str, float]],
                              output_path: str = None) -> plt.Figure:
        """Radar chart comparing centrality across platforms for a person."""
        # This one is tricky as it's cross-platform
        # person_comparison: {"facebook": {"degree": 0.5, "betweenness": 0.2}, ...}

        platforms = list(person_comparison.keys())
        if not platforms: return None

        metrics = list(next(iter(person_comparison.values())).keys())

        # Normalize data (optional but radar usually needs normalization)

        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=config.VIZ_FIGSIZE_SMALL, subplot_kw=dict(polar=True))
        fig.patch.set_facecolor(self.theme["background"])
        ax.set_facecolor(self.theme["background"])

        for plt_name in platforms:
            values = [person_comparison[plt_name].get(m, 0) for m in metrics]
            values += values[:1]

            c = self.theme.get(f"edge_{plt_name}", self.theme["edge_default"])

            ax.plot(angles, values, color=c, linewidth=2, label=plt_name)
            ax.fill(angles, values, color=c, alpha=0.25)

        ax.set_thetagrids(np.degrees(angles[:-1]), metrics)
        ax.tick_params(axis='x', colors=self.theme["text_primary"])
        ax.tick_params(axis='y', colors=self.theme["text_secondary"])

        # Grid color
        ax.grid(color=self.theme["text_secondary"], alpha=0.3)
        ax.spines['polar'].set_color(self.theme["text_secondary"])

        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=config.VIZ_DPI)

        return fig
