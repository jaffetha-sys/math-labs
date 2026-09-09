import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import math

    function_type = mo.ui.radio(
        options=["Sine", "Cosine"],
        value="Sine",
        label="Function",
        inline=True,
    )

    A = mo.ui.slider(
        start=-5,
        stop=5,
        step=0.5,
        value=1,
        label="Coefficient A",
        show_value=True,
        full_width=True,
    )

    B = mo.ui.slider(
        start=0.5,
        stop=4,
        step=0.5,
        value=1,
        label="Frequency factor B",
        show_value=True,
        full_width=True,
    )

    C = mo.ui.dropdown(
        options={
            "-π": -math.pi,
            "-3π/4": -3 * math.pi / 4,
            "-π/2": -math.pi / 2,
            "-π/4": -math.pi / 4,
            "0": 0.0,
            "π/4": math.pi / 4,
            "π/2": math.pi / 2,
            "3π/4": 3 * math.pi / 4,
            "π": math.pi,
        },
        value="0",
        label="Phase shift C",
        full_width=True,
    )

    D = mo.ui.slider(
        start=-2,
        stop=2,
        step=0.5,
        value=0,
        label="Vertical shift D",
        show_value=True,
        full_width=True,
    )

    # Widgets are created once here; presentation cells only reuse them.
    # Named groups provide context even where Marimo's slider thumb lacks
    # an accessible name. Do not patch the widget's generated DOM with scripts.
    controls_panel = mo.Html(f"""
        <aside class="trig-controls" aria-labelledby="trig-controls-heading">
          <h2 id="trig-controls-heading">Controls</h2>
          <div class="trig-function">{function_type.text}</div>
          <fieldset class="trig-group">
            <legend>Shape</legend>
            <div class="trig-control" role="group" aria-label="Coefficient A">{A.text}</div>
            <div class="trig-control" role="group" aria-label="Frequency factor B">{B.text}</div>
          </fieldset>
          <fieldset class="trig-group">
            <legend>Position</legend>
            <div class="trig-control">{C.text}</div>
            <div class="trig-control" role="group" aria-label="Vertical shift D">{D.text}</div>
          </fieldset>
        </aside>
    """)
    return A, B, C, D, controls_panel, function_type


@app.cell
def plot_function(A, B, C, D, function_type):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)

    if function_type.value == "Sine":
        y = A.value * np.sin(
            B.value * (x - C.value)
        ) + D.value
    else:
        y = A.value * np.cos(
            B.value * (x - C.value)
        ) + D.value

    fig, ax = plt.subplots(figsize=(4.8, 4), layout="constrained")
    fig.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    ax.plot(x, y, color="#245da8", linewidth=2.5)

    # Axes
    ax.axhline(0, linewidth=0.8, color="#718096")
    ax.axvline(0, linewidth=0.8, color="#718096")

    # Midline y = D
    ax.axhline(
        D.value,
        linestyle="--",
        linewidth=1.4,
        color="#536579",
    )

    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    # All allowed curves lie within [-7, 7]; keep padding and a fixed scale.
    ax.set_ylim(-7.5, 7.5)

    ax.set_xticks(
        [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi],
        [r"$-2\pi$", r"$-\pi$", "$0$", r"$\pi$", r"$2\pi$"],
    )
    ax.set_yticks([-6, -3, 0, 3, 6])
    ax.set_xlabel("x (radians)", fontsize=16, color="#243449")
    ax.set_ylabel("y", fontsize=16, color="#243449", rotation=0, labelpad=8)
    ax.tick_params(labelsize=16, colors="#243449", length=3)
    for _spine in ax.spines.values():
        _spine.set_color("#cbd3de")
        _spine.set_linewidth(0.8)

    ax.set_axisbelow(True)
    ax.grid(True, color="#e4e9ef", linewidth=0.6)

    graph = fig
    plt.close(fig)
    return (graph,)


@app.cell
def _(mo):
    def render_workspace(controls, equation, figure, table):
        """Compose the visible UI once, independently of the calculations."""
        import io

        _buffer = io.BytesIO()
        figure.savefig(_buffer, format="png", dpi=180)
        _image = mo.image(
            _buffer,
            alt=(
                "Graph of the current function for x from minus 2 pi to 2 pi "
                "radians, with y from minus 7.5 to 7.5. The equation above "
                "and Function Analysis below give its mathematical details. "
                "The dashed line marks the midline y = D."
            ),
            width="100%",
            style={"height": "auto", "display": "block"},
        )
        # Inline, app-scoped CSS travels with the notebook's WASM export.
        # light-dark() follows Marimo's existing color-scheme setting.
        return mo.Html(f"""
        <style>
          .trig-workspace {{
            --marimo-text-font: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            --marimo-heading-font: var(--marimo-text-font);
            --trig-ink: light-dark(#202d3d, #e8edf5);
            --trig-muted: light-dark(#536174, #b3bfd0);
            --trig-border: light-dark(#dce2eb, #465266);
            --trig-surface: light-dark(#f6f8fb, #202a39);
            --trig-accent: light-dark(#245da8, #98c1ff);
            box-sizing: border-box;
            width: 100%; max-width: 1160px; min-width: 0;
            margin: 0 auto; padding: 24px 0 32px;
            color: var(--trig-ink);
            font: 16px/1.5 var(--marimo-text-font);
          }}
          .trig-workspace *, .trig-workspace *::before,
          .trig-workspace *::after {{ box-sizing: border-box; }}
          .trig-workspace h1, .trig-workspace h2 {{
            font-family: var(--marimo-heading-font); color: inherit;
            line-height: 1.3; font-weight: 650; padding: 0;
          }}
          .trig-workspace h1 {{ font-size: 28px; margin: 0 0 8px; }}
          .trig-workspace h2 {{ font-size: 18px; margin: 0 0 16px; }}
          .trig-intro {{ margin-bottom: 24px; }}
          .trig-intro p {{ margin: 0; color: var(--trig-muted); }}
          .trig-grid {{
            display: grid; grid-template-columns: 280px minmax(0, 1fr);
            gap: 24px; align-items: start;
          }}
          .trig-controls {{
            padding: 24px; min-width: 0; border: 1px solid var(--trig-border);
            border-radius: 8px; background: var(--trig-surface);
          }}
          .trig-function {{ padding-bottom: 16px; }}
          .trig-group {{
            border: 0; border-top: 1px solid var(--trig-border);
            min-width: 0; padding: 16px 0 0; margin: 0 0 16px;
          }}
          .trig-group:last-child {{ margin-bottom: 0; }}
          .trig-group legend {{
            color: var(--trig-muted); font-size: 13px; font-weight: 650;
            padding: 0 8px 0 0;
          }}
          .trig-control {{ min-width: 0; margin: 0 0 16px; }}
          .trig-control:last-child {{ margin-bottom: 0; }}
          .trig-control marimo-slider::part(label),
          .trig-control marimo-dropdown::part(label) {{ font-size: 14px; }}
          .trig-control marimo-slider {{ display: block; padding: 4px 0 8px; }}
          .trig-workspace [tabindex]:focus-visible {{
            outline: 2px solid var(--trig-accent); outline-offset: 4px;
          }}
          .trig-control:focus-within {{
            outline: 2px solid var(--trig-accent); outline-offset: 4px;
            border-radius: 2px;
          }}
          .trig-display {{
            min-width: 0; border: 1px solid var(--trig-border); border-radius: 8px;
            padding: 24px;
          }}
          .trig-equation {{
            min-width: 0; max-width: 100%; overflow-x: auto;
            padding: 8px 0 16px; font-size: 18px;
          }}
          .trig-equation .katex-display {{ margin: 0; }}
          .trig-plot {{ margin: 0; min-width: 0; }}
          .trig-plot img {{ max-width: 560px; margin: 0 auto; border-radius: 4px; }}
          .trig-plot figcaption {{
            display: flex; align-items: center; gap: 8px;
            color: var(--trig-muted); font-size: 13px; margin: 8px 0 24px;
          }}
          .trig-midline-key {{
            width: 24px; flex: 0 0 24px; border-top: 2px dashed var(--trig-muted);
          }}
          .trig-analysis {{ border-top: 1px solid var(--trig-border); padding-top: 24px; }}
          .trig-workspace .trig-analysis table {{
            display: table; width: 100%; table-layout: fixed; border-collapse: collapse;
            font-size: 14px; margin: 0;
          }}
          .trig-workspace .trig-analysis :is(th, td) {{
            padding: 12px 16px; text-align: left; vertical-align: top;
            overflow-wrap: anywhere; border-bottom: 1px solid var(--trig-border);
          }}
          .trig-workspace .trig-analysis table tbody tr {{ background: transparent; }}
          .trig-workspace .trig-analysis table tbody tr:hover {{ background: var(--trig-surface); }}
          .trig-workspace .trig-analysis th {{ background: var(--trig-surface); font-weight: 650; }}
          .trig-workspace .trig-analysis :is(th, td):first-child {{ width: 44%; }}
          .trig-workspace .trig-analysis td strong {{ font-weight: 550; }}
          .trig-workspace .trig-analysis tbody tr:last-child td {{ border-bottom: 0; }}
          @media (max-width: 900px) {{
            .trig-grid {{ grid-template-columns: minmax(0, 1fr); gap: 16px; }}
            .trig-controls {{ padding: 16px; }}
            .trig-controls h2 {{ margin-bottom: 8px; }}
            .trig-control {{ margin-bottom: 8px; }}
            .trig-group {{ padding-top: 8px; margin-bottom: 8px; }}
            .trig-display {{ padding: 16px; }}
          }}
          @media (max-width: 480px) {{
            .trig-workspace {{ padding-top: 8px; font-size: 15px; }}
            .trig-workspace h1 {{ font-size: 24px; }}
            .trig-intro {{ margin-bottom: 16px; }}
            .trig-display {{ padding: 12px; }}
            .trig-equation {{ font-size: 17px; }}
            .trig-workspace .trig-analysis :is(th, td) {{ padding: 12px 8px; }}
          }}
        </style>
        <div class="trig-workspace">
          <header class="trig-intro">
            <h1>Trig Functions Lab</h1>
            <p>Explore how each parameter transforms sine and cosine functions.</p>
          </header>
          <div class="trig-grid">
            {controls.text}
            <div class="trig-display">
              <h2>Current function</h2>
              <div class="trig-equation" role="region" aria-label="Current function equation" tabindex="0">
                {equation.text}
              </div>
              <figure class="trig-plot">
                {_image.text}
                <figcaption><span class="trig-midline-key" aria-hidden="true"></span>Dashed line: midline y = D</figcaption>
              </figure>
              <section class="trig-analysis" aria-labelledby="trig-analysis-heading">
                <h2 id="trig-analysis-heading">Function Analysis</h2>
                {table.text}
              </section>
            </div>
          </div>
        </div>
        """)

    return (render_workspace,)


@app.cell
def analyze_function(A, B, C, D, controls_panel, function_type, graph, mo, render_workspace):
    import sympy as sp

    A_sym = sp.Rational(str(A.value))
    B_sym = sp.Rational(str(B.value))
    phase_map = {
        "-π": -sp.pi,
        "-3π/4": -3 * sp.pi / 4,
        "-π/2": -sp.pi / 2,
        "-π/4": -sp.pi / 4,
        "0": sp.Integer(0),
        "π/4": sp.pi / 4,
        "π/2": sp.pi / 2,
        "3π/4": 3 * sp.pi / 4,
        "π": sp.pi,
    }

    C_sym = phase_map[C.selected_key]
    D_sym = sp.Rational(str(D.value))

    amplitude = abs(A_sym)
    period = None if A_sym == 0 else 2 * sp.pi / abs(B_sym)
    phase_shift = None if A_sym == 0 else C_sym
    midline = D_sym
    maximum = D_sym + amplitude
    minimum = D_sym - amplitude
    reflection = (
        "Not applicable (constant function)"
        if A_sym == 0
        else "Yes" if A_sym < 0 else "No"
    )

    x_sym = sp.symbols("x")

    if function_type.value == "Sine":
        expr_sym = (
            A_sym
            * sp.sin(B_sym * (x_sym - C_sym))
            + D_sym
        )
        trig_tex = r"\sin"
    else:
        expr_sym = (
            A_sym
            * sp.cos(B_sym * (x_sym - C_sym))
            + D_sym
        )
        trig_tex = r"\cos"

    # Build a clean pedagogical version of the function
    # without allowing SymPy to rewrite sine as cosine

    A_tex = "" if A_sym == 1 else sp.latex(A_sym)

    if C_sym == 0:
        phase_tex = "x"
    elif C_sym > 0:
        phase_tex = rf"x - {sp.latex(C_sym)}"
    else:
        phase_tex = rf"x + {sp.latex(abs(C_sym))}"

    if B_sym == 1:
        argument_tex = phase_tex
    else:
        argument_tex = rf"{sp.latex(B_sym)}\left({phase_tex}\right)"

    function_tex = rf"{A_tex}{trig_tex}\left({argument_tex}\right)"

    if D_sym > 0:
        function_tex += rf" + {sp.latex(D_sym)}"
    elif D_sym < 0:
        function_tex += rf" - {sp.latex(abs(D_sym))}"

    if A_sym == 0:
        function_tex = sp.latex(D_sym)

    # A constant has every positive period, but no least positive period.
    _period_display = (
        "No fundamental period (constant function)"
        if period is None
        else f"${sp.latex(period)}$"
    )
    _phase_display = (
        "Not applicable (constant function)"
        if phase_shift is None
        else f"${sp.latex(phase_shift)}$"
    )

    _equation = mo.md(f"""
    $$
    y = {function_tex}
    $$
    """)
    _table = mo.md(
        f"""
    | Property | Value |
    |---|---|
    | **Amplitude** | ${sp.latex(amplitude)}$ |
    | **Period** | {_period_display} |
    | **Phase shift** | {_phase_display} |
    | **Midline** | $y={sp.latex(midline)}$ |
    | **Maximum** | ${sp.latex(maximum)}$ |
    | **Minimum** | ${sp.latex(minimum)}$ |
    | **Reflection across midline** | **{reflection}** |
    """
    )
    render_workspace(controls_panel, _equation, graph, _table)
    return


if __name__ == "__main__":
    app.run()
