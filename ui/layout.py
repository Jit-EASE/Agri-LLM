# ui/layout.py
from dash import html, dcc


def build_layout():
    return html.Div(
        className="spectre-root",
        children=[
            # Header
            html.Div(
                className="spectre-header",
                children=[
                    html.Div("SPECTRE NEURAL SEARCH ENGINE", className="spectre-title"),
                    html.Div(
                        "Domain-aware AI search for research and policy design • Prepare → Retrieve → Signal → Serve",
                        className="spectre-subtitle",
                    ),
                ],
            ),

            dcc.Interval(id="typing-interval", interval=40, n_intervals=0, disabled=True),
            dcc.Store(id="full-explanation"),

            html.Div(
                className="spectre-grid",
                children=[
                    # LEFT COLUMN
                    html.Div(
                        children=[
                            html.Div(
                                className="spectre-card",
                                children=[
                                    html.Div(
                                        className="spectre-card-header",
                                        children=[
                                            html.Span("Query & Context", className="spectre-card-title"),
                                            html.Span("Input Bus", className="spectre-badge"),
                                        ],
                                    ),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="Decision / Research Query",
                                    ),
                                    dcc.Textarea(
                                        id="query-input",
                                        className="spectre-textarea",
                                        placeholder=(
                                            "e.g. Design a resilience policy for Irish dairy farms "
                                            "facing climate-driven price shocks."
                                        ),
                                    ),
                                    html.Div(style={"height": "8px"}),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="Domain",
                                    ),
                                    dcc.Dropdown(
                                        id="domain-dropdown",
                                        className="spectre-dropdown domain-tint",
                                        options=[
                                            {"label": "☁ Climate", "value": "Climate"},
                                            {"label": "⚖ Policy", "value": "Policy"},
                                            {"label": "🚚 Supply Chain", "value": "Supply Chain"},
                                        ],
                                        value="Climate",
                                        clearable=False,
                                    ),
                                    html.Div(style={"height": "8px"}),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="Upload CSV",
                                    ),
                                    dcc.Upload(
                                        id="csv-upload",
                                        children=html.Div("Drag & Drop or Select CSV", style={"padding": "6px"}),
                                        style={
                                            "border": "1px dashed rgba(0,242,255,0.35)",
                                            "borderRadius": "12px",
                                            "padding": "10px",
                                            "textAlign": "center",
                                            "cursor": "pointer",
                                            "fontSize": "10px",
                                            "color": "var(--text-soft)",
                                        },
                                        accept=".csv",
                                    ),
                                    html.Div(style={"height": "12px"}),
                                    html.Div(
                                        className="spectre-card",
                                        children=[
                                            html.Div(
                                                className="spectre-card-header",
                                                children=[
                                                    html.Span("Policy Intelligence", className="spectre-card-title"),
                                                    html.Span("PDF Layer", className="spectre-badge"),
                                                ],
                                            ),
                                            html.Div(
                                                className="spectre-section-caption",
                                                children="Upload Food Vision 2030, CAP Strategic Plan, or other agri-policy PDFs.",
                                            ),
                                            html.Div(
                                                className="spectre-input-label",
                                                children="Policy PDF Upload",
                                            ),
                                            dcc.Upload(
                                                id="policy-pdf-upload",
                                                children=html.Div("Drag & Drop or Select PDF", style={"padding": "6px"}),
                                                accept=".pdf",
                                                style={
                                                    "border": "1px dashed rgba(0,242,255,0.35)",
                                                    "borderRadius": "12px",
                                                    "padding": "10px",
                                                    "textAlign": "center",
                                                    "cursor": "pointer",
                                                    "fontSize": "10px",
                                                    "color": "var(--text-soft)",
                                                },
                                            ),
                                            dcc.Interval(
                                                id="pdf-progress-interval",
                                                interval=500,
                                                n_intervals=0,
                                                disabled=True,
                                            ),
                                            dcc.Store(id="pdf-task-id"),
                                            html.Div(style={"height": "8px"}),
                                            html.Div(
                                                className="spectre-input-label",
                                                children="Policy Intelligence Summary",
                                            ),
                                            html.Div(
                                                id="pdf-progress",
                                                className="spectre-console",
                                                children="",
                                            ),
                                            html.Div(
                                                id="policy-intel-output",
                                                className="spectre-console",
                                                children="Upload a PDF to view high-level policy intelligence.",
                                            ),
                                        ],
                                    ),
                                    html.Div(style={"height": "8px"}),
                                    html.Button(
                                        "Run Pipeline",
                                        id="run-button",
                                        n_clicks=0,
                                        className="spectre-button",
                                    ),
                                    html.Div(
                                        className="spectre-section-caption",
                                        children=(
                                            "Offline-capable shell. Swap in real RAG, econometric engines or QUBO solvers "
                                            "behind the same orchestration."
                                        ),
                                    ),
                                ],
                            ),
                            html.Div(style={"height": "12px"}),

                            # Prepare & Retrieve consoles
                            html.Div(
                                className="spectre-card",
                                children=[
                                    html.Div(
                                        className="spectre-card-header",
                                        children=[
                                            html.Span("Prepare & Retrieve", className="spectre-card-title"),
                                            html.Span("Semantic Bus", className="spectre-badge"),
                                        ],
                                    ),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="NLU / Synonym Expansion / Time Conditioning",
                                    ),
                                    html.Div(
                                        id="prepare-console",
                                        className="spectre-console",
                                        children="Awaiting query...",
                                    ),
                                    html.Div(style={"height": "6px"}),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="Top Evidence Chunks (mocked)",
                                    ),
                                    html.Div(
                                        id="retrieve-console",
                                        className="spectre-console",
                                        children="Chunks will appear here after running the pipeline.",
                                    ),
                                ],
                            ),
                        ]
                    ),

                    # RIGHT COLUMN
                    html.Div(
                        children=[
                            html.Div(
                                className="spectre-card",
                                children=[
                                    html.Div(
                                        className="spectre-card-header",
                                        children=[
                                            html.Span("Ranking Signals", className="spectre-card-title"),
                                            html.Span("Jetstream / PCTR", className="spectre-badge"),
                                        ],
                                    ),
                                    html.Div(
                                        className="spectre-section-caption",
                                        children=(
                                            "Multi-signal stack: semantic, contextual, BM25, click-through priors, "
                                            "freshness, and explicit boost/bury rules."
                                        ),
                                    ),
                                    html.Ul(
                                        id="signal-list",
                                        className="spectre-signal-list",
                                    ),
                                    dcc.Graph(
                                        id="signal-graph",
                                        style={"height": "220px", "marginTop": "6px"},
                                        config={"displayModeBar": False},
                                    ),
                                ],
                            ),
                            html.Div(style={"height": "12px"}),

                            html.Div(
                                className="spectre-card",
                                children=[
                                    html.Div(
                                        className="spectre-card-header",
                                        children=[
                                            html.Span("Serve Layer Output", className="spectre-card-title"),
                                            html.Span("Decision Console", className="spectre-badge"),
                                        ],
                                    ),
                                    html.Div(
                                        id="serve-explanation",
                                        className="spectre-console typing-output",
                                        children="Run the pipeline to generate a narrative explanation.",
                                    ),
                                    html.Div(style={"height": "6px"}),
                                    html.Div(
                                        className="spectre-input-label",
                                        children="Related What-If Questions",
                                    ),
                                    html.Ul(
                                        id="related-questions",
                                        className="spectre-related",
                                    ),
                                ],
                            ),
                        ]
                    ),

                    # FULL-WIDTH DECKS
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("Monte Carlo Risk Visualiser", className="spectre-card-title"),
                                    html.Span("Simulation Engine", className="spectre-badge"),
                                ],
                            ),
                            dcc.Graph(
                                id="extra-metrics-graph",
                                style={"height": "260px", "marginTop": "6px"},
                                config={"displayModeBar": False},
                            ),
                        ],
                    ),
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("RL-Teacher Policy Optimiser", className="spectre-card-title"),
                                    html.Span("Reinforcement Engine", className="spectre-badge"),
                                ],
                            ),
                            html.Div(id="rl-output", className="spectre-console"),
                        ],
                    ),
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("EU AI Act Compliance Scanner", className="spectre-card-title"),
                                    html.Span("Governance Layer", className="spectre-badge"),
                                ],
                            ),
                            html.Div(id="ai-act-output", className="spectre-console"),
                        ],
                    ),
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("Shock Engine & Quantum Annealing", className="spectre-card-title"),
                                    html.Span("Volatility + QUBO", className="spectre-badge"),
                                ],
                            ),
                            html.Div(id="shock-output", className="spectre-console"),
                            html.Div(style={"height": "8px"}),
                            html.Div(id="qa-output", className="spectre-console"),
                        ],
                    ),
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("Secondary Neural Agent", className="spectre-card-title"),
                                    html.Span("Dual Reasoning", className="spectre-badge"),
                                ],
                            ),
                            html.Div(id="alt-agent-output", className="spectre-console"),
                        ],
                    ),
                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("CSV Processor Output", className="spectre-card-title"),
                                    html.Span("Data Ingestion", className="spectre-badge"),
                                ],
                            ),
                            html.Div(id="csv-output", className="spectre-console"),
                            html.Div(style={"height": "8px"}),
                            dcc.Graph(
                                id="csv-graph",
                                style={"height": "260px", "marginTop": "6px"},
                                config={"displayModeBar": False},
                            ),
                        ],
                    ),

                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("CSV ACF & PACF Diagnostics", className="spectre-card-title"),
                                    html.Span("Autocorrelation Engine", className="spectre-badge"),
                                ],
                            ),
                            dcc.Graph(id="csv-acf", style={"height": "240px"}, config={"displayModeBar": False}),
                            html.Div(style={"height": "8px"}),
                            dcc.Graph(id="csv-pacf", style={"height": "240px"}, config={"displayModeBar": False}),
                        ],
                    ),

                    html.Div(style={"height": "14px"}),
                    html.Div(
                        className="spectre-card",
                        style={"gridColumn": "1 / -1"},
                        children=[
                            html.Div(
                                className="spectre-card-header",
                                children=[
                                    html.Span("CSV Forecasting (ARIMA)", className="spectre-card-title"),
                                    html.Span("Time-Series Engine", className="spectre-badge"),
                                ],
                            ),
                            dcc.Graph(id="csv-forecast", style={"height": "260px"}, config={"displayModeBar": False}),
                            dcc.Graph(id="fan-forecast-graph", className="spectre-panel"),
                        ],
                    ),

                    html.Div(style={"height": "14px"}),
                ],
            ),
        ],
    )
