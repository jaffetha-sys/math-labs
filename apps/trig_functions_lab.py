import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


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
        label="Function"
    )

    A = mo.ui.slider(
        start=1,
        stop=5,
        step=0.5,
        value=1,
        label="Amplitude A"
    )

    B = mo.ui.slider(
        start=0.5,
        stop=4,
        step=0.5,
        value=1,
        label="Frequency factor B"
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
        label="Phase shift C"
    )

    D = mo.ui.slider(
        start=-5,
        stop=5,
        step=0.5,
        value=0,
        label="Vertical shift D"
    )

    mo.vstack([
        mo.md(
            """
    # Trig Functions Lab

    Explore how each parameter transforms the graph.
    """
        ),
        function_type,
        A,
        B,
        C,
        D,
    ])
    return A, B, C, D, function_type


@app.cell
def _(A, B, C, D, function_tex, function_type):
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

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(x, y)

    # Axes
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    # Midline y = D
    ax.axhline(
        D.value,
        linestyle="--",
        linewidth=1
    )

    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    ax.set_ylim(-10.5, 10.5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_title(
        rf"$y = {function_tex}$"
    )

    ax.grid(True, alpha=0.25)

    fig
    return


@app.cell
def _(A, B, C, D, function_type, mo):
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
    period = 2 * sp.pi / abs(B_sym)
    phase_shift = C_sym
    midline = D_sym
    maximum = D_sym + amplitude
    minimum = D_sym - amplitude

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

    mo.md(
        f"""
    ## Function Analysis

    ### Current function

    $$
    y = {function_tex}
    $$

    | Property | Value |
    |---|---|
    | **Amplitude** | ${sp.latex(amplitude)}$ |
    | **Period** | ${sp.latex(period)}$ |
    | **Phase shift** | ${sp.latex(phase_shift)}$ |
    | **Midline** | $y={sp.latex(midline)}$ |
    | **Maximum** | ${sp.latex(maximum)}$ |
    | **Minimum** | ${sp.latex(minimum)}$ |
    """
    )
    return (function_tex,)


if __name__ == "__main__":
    app.run()
