# ui/style_shell.py

SPECTRE_INDEX_STRING = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
        :root {
            --bg-main:#02040a;
            --bg-panel:rgba(6,10,22,0.94);
            --accent-primary:#00f2ff;
            --accent-secondary:#ff00d4;
            --text-main:#e8f5ff;
            --text-soft:#9ba7c4;
            --border-subtle:rgba(0,242,255,0.22);
        }
        body {
            margin:0;
            padding:0;
            background:
                linear-gradient(rgba(0,0,0,0.9),rgba(0,0,0,0.94)),
                repeating-linear-gradient(
                    to right,
                    rgba(0,255,255,0.04) 0px,
                    rgba(0,255,255,0.04) 1px,
                    transparent 1px,
                    transparent 40px
                ),
                repeating-linear-gradient(
                    to bottom,
                    rgba(0,255,255,0.04) 0px,
                    rgba(0,255,255,0.04) 1px,
                    transparent 1px,
                    transparent 40px
                ),
                radial-gradient(circle at top,#0b1222 0,#02040a 55%,#000 100%);
            color:var(--text-main);
            font-family:-apple-system,system-ui,"SF Pro Text",sans-serif;
        }
        .spectre-root{
            min-height:100vh;
            padding:20px 14px 26px 14px;
            box-sizing:border-box;
        }
        @media (min-width:1100px){
            .spectre-root{padding:24px 60px 34px 60px;}
        }
        .spectre-header{
            display:flex;
            flex-direction:column;
            gap:4px;
            margin-bottom:14px;
        }
        .spectre-title{
            font-size:20px;
            letter-spacing:0.12em;
            text-transform:uppercase;
        }
        .spectre-subtitle{
            font-size:11px;
            max-width:780px;
            color:var(--text-soft);
        }
        .spectre-grid{
            display:grid;
            grid-template-columns:minmax(0,1.1fr) minmax(0,1.3fr);
            gap:14px;
        }
        @media (max-width:900px){
            .spectre-grid{grid-template-columns:minmax(0,1fr);}
        }
        .spectre-card{
            position:relative;
            overflow:hidden;
            background:radial-gradient(circle at top,rgba(15,22,45,0.98),rgba(2,6,14,0.99));
            border-radius:16px;
            border:1px solid var(--border-subtle);
            box-shadow:0 14px 30px rgba(0,0,0,0.75);
            backdrop-filter:blur(18px) saturate(170%);
            padding:12px 12px 10px 12px;
            transition:.26s ease-out;
        }
        .spectre-card::before{
            content:"";
            position:absolute;
            inset:-40%;
            background:conic-gradient(from 210deg,
                rgba(0,242,255,0.08),
                rgba(255,0,212,0.14),
                transparent 40%,
                transparent);
            opacity:0;
            transition:.5s ease-out;
        }
        .spectre-card:hover{
            transform:translateY(-3px);
            border-color:rgba(0,242,255,0.6);
            box-shadow:0 0 22px rgba(0,242,255,0.7);
        }
        .spectre-card:hover::before{opacity:1;}
        body::after{
            content:"";
            pointer-events:none;
            position:fixed;
            inset:0;
            background:repeating-linear-gradient(
                to bottom,
                rgba(255,255,255,0.04),
                rgba(255,255,255,0.04) 1px,
                transparent 1px,
                transparent 3px
            );
            opacity:.12;
            animation:scanlines 6s linear infinite;
            z-index:9999;
        }
        @keyframes scanlines{
            from{transform:translateY(0);}
            to{transform:translateY(4px);}
        }
        .spectre-card-header{
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:6px;
        }
        .spectre-card-title{
            font-size:11px;
            text-transform:uppercase;
            letter-spacing:0.18em;
            color:var(--accent-primary);
        }
        .spectre-badge{
            font-size:9px;
            text-transform:uppercase;
            letter-spacing:0.15em;
            padding:2px 8px;
            border-radius:999px;
            border:1px solid rgba(0,242,255,0.4);
            color:var(--text-soft);
        }
        .spectre-input-label{
            font-size:9px;
            text-transform:uppercase;
            letter-spacing:0.16em;
            color:var(--text-soft);
            margin-bottom:4px;
        }
        .spectre-textarea,.spectre-dropdown{
            width:100%;
            border-radius:12px;
            border:1px solid rgba(0,242,255,0.3);
            background:#2b2f38 !important;
            background:linear-gradient(180deg,#2b2f38,#1e2229) !important;
            color:var(--text-main);
            font-size:11px;
            padding:7px 9px;
            box-sizing:border-box;
            outline:none;
            transition:.18s ease-out;
        }
        /* GLASS DROPDOWN */
        .spectre-dropdown .Select-control,
        #domain-dropdown .Select-control {
            background: rgba(255,255,255,0.08) !important;
            backdrop-filter: blur(14px) saturate(180%) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(0,242,255,0.35) !important;
            box-shadow: 0 0 12px rgba(0,242,255,0.20) inset !important;
            transition: 0.25s ease-out;
        }
        .spectre-dropdown .Select-placeholder,
        .spectre-dropdown .Select-value-label,
        #domain-dropdown .Select-placeholder,
        #domain-dropdown .Select-value-label {
            color: var(--text-main) !important;
            font-weight: 400 !important;
        }
        .spectre-dropdown .Select-menu-outer,
        #domain-dropdown .Select-menu-outer {
            background: rgba(0,0,0,0.55) !important;
            backdrop-filter: blur(18px) saturate(180%) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(0,242,255,0.35) !important;
        }
        .spectre-dropdown .Select-option,
        #domain-dropdown .Select-option {
            background: rgba(255,255,255,0.05) !important;
            color: var(--text-main) !important;
            padding: 6px 10px !important;
            transition: 0.22s ease-out;
        }
        .spectre-dropdown .Select-option:hover,
        #domain-dropdown .Select-option:hover {
            background: rgba(0,242,255,0.22) !important;
            color: #ffffff !important;
            box-shadow: 0 0 12px rgba(0,242,255,0.65) inset !important;
        }
        .domain-tint[value="Climate"] {
            border-color:#00f2ff !important;
            box-shadow:0 0 8px #00f2ff88 !important;
        }
        .domain-tint[value="Policy"] {
            border-color:#ff00d4 !important;
            box-shadow:0 0 8px #ff00d488 !important;
        }
        .domain-tint[value="Supply Chain"] {
            border-color:#ffbf3b !important;
            box-shadow:0 0 8px #ffbf3b88 !important;
        }
        .spectre-textarea,
        .spectre-dropdown,
        .spectre-textarea * {
            pointer-events:auto !important;
            z-index:99999 !important;
            position:relative !important;
        }
        .spectre-textarea{
            min-height:80px;
            resize:vertical;
        }
        .spectre-textarea:focus,.spectre-dropdown:focus{
            border-color:var(--accent-secondary);
            box-shadow:0 0 14px rgba(255,0,212,0.6);
        }
        .spectre-button{
            margin-top:10px;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            padding:7px 16px;
            border-radius:999px;
            border:none;
            background:linear-gradient(90deg,#00f2ff,#ff00d4);
            color:#02040a;
            font-size:9px;
            text-transform:uppercase;
            letter-spacing:0.2em;
            cursor:pointer;
            box-shadow:0 0 12px rgba(0,242,255,0.7);
            position:relative;
            overflow:hidden;
        }
        .spectre-button::after{
            content:"";
            position:absolute;
            inset:-4px;
            border-radius:999px;
            background:radial-gradient(circle,rgba(0,242,255,0.25),transparent 70%);
            opacity:0;
            animation:pulseGlow 2.5s ease-in-out infinite;
        }
        @keyframes pulseGlow{
            0%{opacity:.05;transform:scale(0.95);}
            50%{opacity:.5;transform:scale(1.05);}
            100%{opacity:.05;transform:scale(0.95);}
        }
        .spectre-console{
            margin-top:6px;
            font-family:"SF Mono",Menlo,Consolas,monospace;
            font-size:10px;
            background:radial-gradient(circle at top,rgba(3,8,18,0.98),rgba(0,0,0,0.96));
            border-radius:12px;
            border:1px solid rgba(0,242,255,0.35);
            padding:8px 9px;
            max-height:160px;
            overflow:auto;
            white-space:pre-wrap;
        }
        .spectre-section-caption{
            margin-top:6px;
            font-size:10px;
            color:var(--text-soft);
        }
        .spectre-signal-list{
            list-style:none;
            margin:0;
            padding:0;
            font-size:10px;
        }
        .spectre-signal-list li{
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:2px 0;
            border-bottom:1px dashed rgba(0,242,255,0.18);
        }
        .spectre-signal-key{color:var(--text-soft);}
        .spectre-signal-val{
            color:var(--accent-primary);
            font-variant-numeric:tabular-nums;
        }
        .spectre-related{
            margin-top:4px;
            padding-left:16px;
            font-size:10px;
            color:var(--text-soft);
        }
        .spectre-related li{margin-bottom:2px;}
        .typing-output{
            font-family:"SF Mono",Menlo,Consolas,monospace;
            font-size:10px;
            white-space:pre-wrap;
        }
        .typing-cursor{
            display:inline-block;
            margin-left:2px;
            color:var(--accent-secondary);
            animation:blink .6s infinite;
        }
        @keyframes blink{
            0%,50%{opacity:1;}
            51%,100%{opacity:0;}
        }
        </style>
        <script>
        document.addEventListener("input", function(e){
            if(e.target && e.target.id === "domain-dropdown"){
                e.target.setAttribute("value", e.target.value);
            }
        });
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
