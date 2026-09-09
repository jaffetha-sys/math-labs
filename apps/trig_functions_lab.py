import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    A = mo.ui.slider(
        start=1,
        stop=5,
        step=0.5,
        value=1,
        label="Amplitude A"
    )

    A
    return (A,)


@app.cell
def _(A, B, C, D):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)

    y = A.value * np.sin(
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
        f"y = {A.value} sin({B.value}(x - {C.value})) + {D.value}"
    )

    ax.grid(True, alpha=0.25)

    fig
    return


@app.cell
def _(mo):
    B = mo.ui.slider(
        start=0.5,
        stop=4,
        step=0.5,
        value=1,
        label="Frequency factor B"
    )

    B
    return (B,)


@app.cell
def _(A, B, C, D, mo):
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

    expr_sym = (
        A_sym
        * sp.sin(B_sym * (x_sym - C_sym))
        + D_sym
    )

    mo.md(
        f"""
    ## Function Analysis

    ### Current function

    $$
    y = {sp.latex(expr_sym)}
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
    return


@app.cell
def _(mo):
    import math

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

    mo.vstack([C, D])
    return C, D


if __name__ == "__main__":
    app.run()
