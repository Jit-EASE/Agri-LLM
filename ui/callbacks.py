# ui/callbacks.py
from dash import Input, Output, State
import dash
import plotly.graph_objs as go
import html as _html  # for type consistency, we’ll use dash.html in layout

from ingestion.pdf_async import launch_pdf_task, pdf_tasks
from orchestrator import run_policy_pipeline


def register_callbacks(app):

    @app.callback(
        [
            Output("pdf-progress", "children"),
            Output("policy-intel-output", "children"),
            Output("prepare-console", "children"),
            Output("retrieve-console", "children"),
            Output("signal-list", "children"),
            Output("signal-graph", "figure"),

            Output("extra-metrics-graph", "figure"),
            Output("rl-output", "children"),
            Output("ai-act-output", "children"),
            Output("shock-output", "children"),
            Output("qa-output", "children"),
            Output("alt-agent-output", "children"),
            Output("csv-output", "children"),
            Output("csv-graph", "figure"),
            Output("csv-acf", "figure"),
            Output("csv-pacf", "figure"),
            Output("csv-forecast", "figure"),
            Output("fan-forecast-graph", "figure"),

            Output("full-explanation", "data"),
            Output("typing-interval", "disabled"),
            Output("typing-interval", "n_intervals"),
            Output("related-questions", "children"),
            Output("pdf-progress-interval", "disabled"),
            Output("pdf-task-id", "data"),
        ],
        [
            Input("run-button", "n_clicks"),
            Input("csv-upload", "contents"),
            Input("policy-pdf-upload", "contents"),
            Input("pdf-progress-interval", "n_intervals"),
        ],
        [
            State("query-input", "value"),
            State("domain-dropdown", "value"),
            State("pdf-task-id", "data"),
        ],
        prevent_initial_call=True,
    )
    def run_pipeline(
        n_clicks,
        uploaded_csv,
        uploaded_pdf,
        pdf_progress_n,
        query,
        domain,
        pdf_task_id,
    ):
        """
        PDF + GPT-4o-mini policy layer + orchestrated decision pipeline.
        """
        ctx = dash.callback_context
        triggered = [t["prop_id"] for t in (ctx.triggered or [])]

        # === 1. Run button with PDF → launch async task ===
        if "run-button.n_clicks" in triggered and uploaded_pdf:
            try:
                import base64, time, hashlib as _hashlib
                content_type, content_string = uploaded_pdf.split(",")
                pdf_bytes = base64.b64decode(content_string)
                task_id = _hashlib.sha256(str(time.time()).encode()).hexdigest()
                launch_pdf_task(task_id, pdf_bytes)

                return (
                    "Parsing (async)…",
                    "Processing PDF…",
                    "Awaiting query...",
                    "No chunks.",
                    [],
                    go.Figure(),
                    go.Figure(),
                    "No RL data.",
                    "No AI Act scan.",
                    "No shocks.",
                    "No QA.",
                    "No alt-agent output.",
                    "No CSV.",
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    "",
                    True,
                    0,
                    [],
                    False,
                    task_id,
                )
            except Exception:
                return (
                    "PDF could not be parsed.",
                    "[Policy Intelligence] Could not extract text.",
                    "Awaiting query...",
                    "No chunks.",
                    [],
                    go.Figure(),
                    go.Figure(),
                    "No RL data.",
                    "No AI Act scan.",
                    "No shocks.",
                    "No QA.",
                    "No alt-agent output.",
                    "No CSV.",
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    "",
                    True,
                    0,
                    [],
                    True,
                    None,
                )

        # === 2. Polling PDF progress ===
        if "pdf-progress-interval.n_intervals" in triggered and pdf_task_id:
            task = pdf_tasks.get(pdf_task_id)
            if task and task["future"].done():
                try:
                    pdf_text = task["future"].result()
                except Exception:
                    pdf_text = ""
                if not pdf_text:
                    return (
                        "PDF could not be parsed.",
                        "[Policy Intelligence] Could not extract text.",
                        "Awaiting query...",
                        "No chunks.",
                        [],
                        go.Figure(),
                        go.Figure(),
                        "No RL data.",
                        "No AI Act scan.",
                        "No shocks.",
                        "No QA.",
                        "No alt-agent output.",
                        "No CSV.",
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        "",
                        True,
                        0,
                        [],
                        True,
                        None,
                    )

                # === GPT-4o-mini summary call ===
                try:
                    from openai import OpenAI

                    client = OpenAI()

                    file_label = "policy.pdf"
                    system_msg = (
                        "You are a specialised policy engine for Irish and EU agri-food strategy. "
                        "Given raw text from a policy PDF, you must:\n"
                        "- Identify the high-level goals and pillars\n"
                        "- Extract key instruments (subsidies, regulations, schemes)\n"
                        "- Extract KPIs / targets (numbers, dates, metrics)\n"
                        "- Flag main risks / trade-offs\n"
                        "- Keep output compact but information-dense."
                    )
                    user_msg = (
                        f"FILE NAME: {file_label}\n\n"
                        "Below is extracted text from the first pages of a policy PDF. "
                        "Summarise it in 8–12 structured bullet points as requested.\n\n"
                        f"{pdf_text[:8000]}"
                    )

                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": user_msg},
                        ],
                        temperature=0.2,
                    )
                    summary = resp.choices[0].message.content.strip()

                    # === Orchestrated policy pipeline ===
                    results = run_policy_pipeline(query or "", domain or "Climate")
                    serve = results["serve"]
                    full_expl = serve["explanation"]
                    related_q = [  # dash.html is imported in layout; here we use simple strings.
                        _html.escape(q) for q in serve["related"]
                    ]

                    # For visual list, we still need dash.html.Li in layout, so we output raw strings here
                    related_children = [  # UI will render them directly as <li> via layout
                        _html.escape(q) for q in serve["related"]
                    ]

                    # Minimal wiring: we only update explanation + what-ifs for now
                    return (
                        "PDF parsed successfully.",
                        summary,
                        "Prepared query will appear here.",
                        "Retrieved chunks will appear here.",
                        [],
                        go.Figure(),
                        go.Figure(),           # extra-metrics-graph
                        "RL output pending.",
                        "AI Act scan pending.",
                        "Shock data pending.",
                        "QA pending.",
                        "Alt-agent pending.",
                        "CSV output pending.",
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        full_expl,
                        False,
                        0,
                        related_children,
                        True,
                        None,
                    )
                except Exception as e:
                    return (
                        f"[Policy Intelligence]\nOpenAI / GPT-4o-mini call failed: {e}",
                        "",
                        "Awaiting query...",
                        "No chunks.",
                        [],
                        go.Figure(),
                        go.Figure(),
                        "No RL data.",
                        "No AI Act scan.",
                        "No shocks.",
                        "No QA.",
                        "No alt-agent output.",
                        "No CSV.",
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        go.Figure(),
                        "",
                        True,
                        0,
                        [],
                        True,
                        None,
                    )
            else:
                # Still processing
                return (
                    "Processing…",
                    "Processing PDF…",
                    "Awaiting query...",
                    "No chunks.",
                    [],
                    go.Figure(),
                    go.Figure(),
                    "No RL data.",
                    "No AI Act scan.",
                    "No shocks.",
                    "No QA.",
                    "No alt-agent output.",
                    "No CSV.",
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    go.Figure(),
                    "",
                    True,
                    0,
                    [],
                    False,
                    pdf_task_id,
                )

        # === 3. No PDF scenario – behaviour stays as in your original (no pipeline) ===
        return (
            "",
            "",
            "Awaiting query...",
            "No chunks.",
            [],
            go.Figure(),
            go.Figure(),
            "No RL data.",
            "No AI Act scan.",
            "No shocks.",
            "No QA.",
            "No alt-agent output.",
            "No CSV.",
            go.Figure(),
            go.Figure(),
            go.Figure(),
            go.Figure(),
            go.Figure(),
            "",
            True,
            0,
            [],
            True,
            None,
        )
