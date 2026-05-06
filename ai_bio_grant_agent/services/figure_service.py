from pathlib import Path
from clients.nanobanana_client import NanoBananaClient
from config.settings import FIGURE_DIR


def generate_two_figures(fig1_prompt: str, fig2_prompt: str):
    client = NanoBananaClient()
    fig1 = client.generate_image(fig1_prompt, Path(FIGURE_DIR / "figure_1.png"))
    fig2 = client.generate_image(fig2_prompt, Path(FIGURE_DIR / "figure_2.png"))
    return fig1, fig2
