"""Starter figure style for print-ready matplotlib panels. Copy into a project and adjust.

- Arial everywhere; 7 pt body text, 6 pt ticks (journal sizes at 100% scale).
- Figures are created at final print size in mm (`MM`); never rescale them later.
- Vector export: SVG keeps text editable (`svg.fonttype = none`), PDF embeds TrueType (Type 42).
- Dense layers (scatter points, maps, renders) are rasterized on the artist (`rasterized=True`) at RASTER_DPI,
  so axes, text and legends stay vector while files stay small enough for a vector editor.
- Every panel is saved as .svg + .pdf (for editing) and .png (for quick review).
"""
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

MM = 1 / 25.4  # inches per mm; journal widths: single column 89 mm, 1.5 column 120 mm, double 183 mm
RASTER_DPI = 600

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": 7,
    "axes.titlesize": 7,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "legend.title_fontsize": 7,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2,
    "ytick.major.size": 2,
    "lines.linewidth": 0.75,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": RASTER_DPI,
    "figure.dpi": 150,
})

# bars and boxes: color at FILL_ALPHA with a thin dark edge; medians and marks in the same color, opaque
FILL_ALPHA = 0.5
EDGE_COLOR = "#333333"
UNCLASSIFIED = "#D9D9D9"

# light sequential colormap (apricot -> pink -> lavender -> violet): the low end is tinted, not white,
# so low values stay visible on a white page; lightness falls monotonically
LIGHT_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "light", ["#FCE6CF", "#F8CDB8", "#F4B0CC", "#D79BD6", "#A58BDB", "#7D74C9"])


def save(fig, out_dir, name, formats=("svg", "pdf", "png"), png_dpi=300, tight=True, transparent=False):
    """Write `name`.svg/.pdf/.png into out_dir (a pathlib.Path).

    tight=False keeps the canvas exactly, for panels placed by mm coordinates in a composed figure;
    transparent=True drops the backgrounds, for panels laid over a tinted figure background."""
    out_dir.mkdir(parents=True, exist_ok=True)
    kw = dict(bbox_inches="tight", pad_inches=0.02) if tight else {}
    kw["transparent"] = transparent
    for fmt in formats:
        fig.savefig(out_dir / f"{name}.{fmt}", dpi=png_dpi if fmt == "png" else RASTER_DPI, **kw)
    plt.close(fig)


def fill(color):
    """RGBA fill for bars and boxes: `color` at FILL_ALPHA (edges stay opaque)."""
    return mcolors.to_rgba(color, FILL_ALPHA)


def clean_axes(ax):
    """Remove frame and ticks (embedding and spatial panels)."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def box_axes(ax):
    """Closed frame (all four spines), for QC histograms and box plots."""
    for spine in ax.spines.values():
        spine.set_visible(True)


def header(ax, text, y=1.06):
    """Panel title centered above the axes with a rule on each side ("—— text ——")."""
    ax.plot([0, 1], [y, y], transform=ax.transAxes, color="black", lw=0.6, clip_on=False, zorder=1)
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="center", fontsize=7, zorder=2,
            bbox=dict(boxstyle="square,pad=0.4", fc="white", ec="none"))
