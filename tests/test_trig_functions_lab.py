"""Behavioral checks of the production notebook through Marimo's public API.

Run with: uv run --locked python -m pytest
Cell tests use lightweight widget values; the app smoke test uses real controls.
"""

from html import unescape
from html.parser import HTMLParser
from itertools import product
from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
import sympy as sp

from apps.trig_functions_lab import analyze_function, app, plot_function


PHASES = {
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


class AnalysisTable(HTMLParser):
    """Read visible table values without depending on CSS or HTML whitespace."""

    def __init__(self, output):
        super().__init__()
        self.rows = {}
        self._row = []
        self._text = None
        self.feed(output.text)

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag == "td":
            self._text = []

    def handle_data(self, data):
        if self._text is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "td":
            text = "".join(self._text).strip()
            # Marimo wraps inline TeX in these delimiters before typesetting.
            self._row.append(text.removeprefix("||(").removesuffix("||)"))
            self._text = None
        elif tag == "tr" and len(self._row) == 2:
            self.rows[self._row[0]] = self._row[1]


def inputs(kind="Sine", a=1, b=1, phase="0", d=0):
    return {
        "function_type": SimpleNamespace(value=kind),
        "A": SimpleNamespace(value=a),
        "B": SimpleNamespace(value=b),
        "C": SimpleNamespace(value=float(PHASES[phase]), selected_key=phase),
        "D": SimpleNamespace(value=d),
    }


@pytest.fixture(scope="module")
def default_app():
    outputs, definitions = app.run()
    yield outputs, definitions
    plt.close("all")


def test_default_app_connects_real_controls_plot_and_analysis(default_app):
    outputs, values = default_app
    assert [values[k].value for k in ("A", "B", "C", "D", "function_type")] == [
        1, 1, 0, 0, "Sine"
    ]
    ranges = {"A": (-5, 5, 0.5), "B": (0.5, 4, 0.5), "D": (-2, 2, 0.5)}
    for name, expected in ranges.items():
        widget = values[name]
        assert (widget.start, widget.stop, widget.step) == expected
    assert list(values["C"].options) == list(PHASES)
    np.testing.assert_allclose(
        list(values["C"].options.values()), [float(v) for v in PHASES.values()]
    )

    layout = next(
        o for o in outputs if "Trig Functions Lab" in getattr(o, "text", "")
    )
    assert "Controls" in layout.text
    # Script mode returns the figure; browser mode performs image rendering.
    assert isinstance(values["graph"], plt.Figure)
    analysis = next(
        o for o in outputs if "Function Analysis" in getattr(o, "text", "")
    )
    assert AnalysisTable(analysis).rows == {
        "Amplitude": "1",
        "Period": r"2 \pi",
        "Phase shift": "0",
        "Midline": "y=0",
        "Maximum": "1",
        "Minimum": "-1",
        "Reflection across midline": "No",
    }
    assert values["expr_sym"] == sp.sin(values["x_sym"])
    assert values["function_tex"] == r"\sin\left(x\right)"
    assert f"y = {values['function_tex']}" in unescape(analysis.text)
    line = values["graph"].axes[0].lines[0]
    np.testing.assert_allclose(
        line.get_ydata(), np.sin(line.get_xdata()), atol=1e-12, rtol=1e-12
    )


@pytest.mark.parametrize("kind", ["Sine", "Cosine"])
@pytest.mark.parametrize("phase", PHASES)
@pytest.mark.parametrize(
    "a,b,d", [(0.5, 0.5, -2), (-0.5, 4, 2), (5, 1, 0), (-5, 1, -0.5)]
)
def test_exact_nonconstant_analysis_and_display(kind, phase, a, b, d):
    output, values = analyze_function.run(**inputs(kind, a, b, phase, d))
    a_exact, b_exact, d_exact = map(lambda v: sp.Rational(str(v)), (a, b, d))
    expected = {
        "amplitude": abs(a_exact),
        "period": 2 * sp.pi / b_exact,
        "phase_shift": PHASES[phase],
        "midline": d_exact,
        "maximum": d_exact + abs(a_exact),
        "minimum": d_exact - abs(a_exact),
    }
    for name, value in expected.items():
        assert values[name] == value
    trig = sp.sin if kind == "Sine" else sp.cos
    expression = (
        a_exact * trig(b_exact * (values["x_sym"] - PHASES[phase])) + d_exact
    )
    assert sp.simplify(values["expr_sym"] - expression) == 0
    rows = AnalysisTable(output).rows
    for label, name in [
        ("Amplitude", "amplitude"),
        ("Period", "period"),
        ("Phase shift", "phase_shift"),
        ("Maximum", "maximum"),
        ("Minimum", "minimum"),
    ]:
        assert rows[label] == sp.latex(expected[name])
    assert rows["Midline"] == f"y={sp.latex(d_exact)}"
    assert rows["Reflection across midline"] == ("Yes" if a < 0 else "No")
    tex = values["function_tex"]
    assert (r"\sin" if kind == "Sine" else r"\cos") in tex
    assert (r"\cos" if kind == "Sine" else r"\sin") not in tex
    assert f"y = {tex}" in unescape(output.text)


@pytest.mark.parametrize(
    "kind,b,phase,d",
    list(product(
        ["Sine", "Cosine"], [0.5, 1, 4], ["-π", "0", "π/2"], [-2, 0, 0.5, 2]
    )),
)
def test_constant_analysis_and_display(kind, b, phase, d):
    output, values = analyze_function.run(**inputs(kind, 0, b, phase, d))
    exact = sp.Rational(str(d))
    assert values["expr_sym"] == exact
    assert values["amplitude"] == 0
    assert values["maximum"] == values["minimum"] == values["midline"] == exact
    assert values["period"] is None
    assert values["phase_shift"] is None
    assert values["function_tex"] == sp.latex(exact)
    assert f"y = {sp.latex(exact)}" in unescape(output.text)
    assert AnalysisTable(output).rows == {
        "Amplitude": "0",
        "Period": "No fundamental period (constant function)",
        "Phase shift": "Not applicable (constant function)",
        "Midline": f"y={sp.latex(exact)}",
        "Maximum": sp.latex(exact),
        "Minimum": sp.latex(exact),
        "Reflection across midline": "Not applicable (constant function)",
    }


PLOT_CASES = [
    (1, 1, "0", 0),
    (5, 1, "0", 2),       # Confirmed upper clipping case.
    (5, 1, "0", -2),      # Corresponding lower extreme.
    (-5, 4, "-π", -2),
    (0.5, 0.5, "-3π/4", 0.5),
    (-0.5, 4, "-π/2", -0.5),
    (1, 0.5, "-π/4", 0),
    (-1, 1, "π/4", 0),
    (1, 1, "π/2", 0),
    (1, 4, "3π/4", 2),
    (-5, 0.5, "π", 2),
    (0, 0.5, "-π", -2),
    (0, 1, "0", 0),
    (0, 4, "π/2", 2),
]


@pytest.mark.parametrize("kind", ["Sine", "Cosine"])
@pytest.mark.parametrize("a,b,phase,d", PLOT_CASES)
def test_production_plot_agrees_with_symbolic_analysis(
    default_app, kind, a, b, phase, d
):
    refs = inputs(kind, a, b, phase, d)
    _, analysis = analyze_function.run(**refs)
    _, plotted = plot_function.run(**refs)
    figure = plotted["graph"]
    try:
        axis = figure.axes[0]
        x, y = axis.lines[0].get_data()
        expected = sp.lambdify(analysis["x_sym"], analysis["expr_sym"], "numpy")(x)
        np.testing.assert_allclose(
            y, np.broadcast_to(expected, y.shape), atol=1e-12, rtol=1e-12
        )
        assert len(x) == 600
        np.testing.assert_allclose([x[0], x[-1]], [-2 * np.pi, 2 * np.pi])
        np.testing.assert_allclose(axis.get_xlim(), [-2 * np.pi, 2 * np.pi])
        assert axis.get_ylim() == default_app[1]["graph"].axes[0].get_ylim()
        lower, upper = axis.get_ylim()
        assert lower < float(analysis["minimum"]) <= float(analysis["maximum"]) < upper
        np.testing.assert_allclose(axis.lines[-1].get_ydata(), [d, d])
    finally:
        plt.close(figure)


def test_fixed_plot_bounds_cover_entire_allowed_range(default_app):
    _, values = default_app
    lower, upper = values["graph"].axes[0].get_ylim()
    a_control, d_control = values["A"], values["D"]
    # Theoretical extrema, independent of sampling, B, phase, or trig family.
    for a, d in product(
        np.arange(a_control.start, a_control.stop + a_control.step, a_control.step),
        np.arange(d_control.start, d_control.stop + d_control.step, d_control.step),
    ):
        assert lower < d - abs(a)
        assert upper > d + abs(a)


@pytest.mark.parametrize("kind,expected", [
    ("Sine", r"\sin\left(x - \frac{\pi}{2}\right)"),
    ("Cosine", r"\cos\left(x - \frac{\pi}{2}\right)"),
])
def test_quarter_turn_keeps_transformation_equation(kind, expected):
    _, values = analyze_function.run(**inputs(kind, phase="π/2"))
    assert values["function_tex"] == expected
