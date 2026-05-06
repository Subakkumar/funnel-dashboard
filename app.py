import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── Load Data ─────────────────────────────────────────
df = pd.read_csv('data/funnel_data.csv')
df['date'] = pd.to_datetime(df['date'])

FUNNEL_STEPS = ['landing_page', 'product_view', 'add_to_cart', 'checkout', 'purchase']
STEP_LABELS  = ['Landing Page', 'Product View', 'Add to Cart', 'Checkout', 'Purchase']

COLORS = {
    'bg':        '#07080f',
    'panel':     '#0d1018',
    'panel2':    '#111520',
    'blue':      '#4fc3f7',
    'cyan':      '#00e5ff',
    'green':     '#00e676',
    'orange':    '#ff6b35',
    'purple':    '#7c4dff',
    'gold':      '#ffd740',
    'text':      '#e8f4f8',
    'muted':     '#6b8fa3',
    'line':      '#1e2d3d',
    'chart_colors': ['#4fc3f7','#00e676','#ff6b35','#7c4dff','#ffd740','#00e5ff','#ff4081','#69f0ae']
}

# ── App Init ───────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Funnel Analysis Dashboard'
)

# ── Helper functions ───────────────────────────────────
def get_funnel_counts(dff):
    counts = []
    for step in FUNNEL_STEPS:
        n = dff['reached_step'].apply(
            lambda x: FUNNEL_STEPS.index(x) >= FUNNEL_STEPS.index(step)
            if x in FUNNEL_STEPS else False
        ).sum()
        counts.append(n)
    return counts

def card_style(border_color=None):
    style = {
        'background': COLORS['panel'],
        'border': f'1px solid {border_color or COLORS["line"]}',
        'borderRadius': '4px',
        'padding': '1.25rem',
        'position': 'relative',
        'overflow': 'hidden'
    }
    return style

def chart_layout(title='', height=300):
    return dict(
        title=dict(text=title, font=dict(color=COLORS['muted'], size=11,
                   family='Share Tech Mono'), x=0, pad=dict(l=0, b=10)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], family='Rajdhani, sans-serif'),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor=COLORS['line'], showline=False,
                   tickfont=dict(size=10, color=COLORS['muted'])),
        yaxis=dict(gridcolor=COLORS['line'], showline=False,
                   tickfont=dict(size=10, color=COLORS['muted'])),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        hoverlabel=dict(bgcolor=COLORS['panel2'], bordercolor=COLORS['blue'],
                        font=dict(color=COLORS['text']))
    )

# ── KPI Card ───────────────────────────────────────────
def kpi_card(title, value, sub='', color=None):
    return html.Div([
        html.Div(style={
            'position': 'absolute', 'top': 1, 'left': 1, 'right': 1,
            'height': '3px',
            'background': f'linear-gradient(90deg, {color or COLORS["blue"]}, transparent)'
        }),
        html.Div(title, style={
            'fontFamily': 'Share Tech Mono, monospace',
            'fontSize': '0.62rem',
            'letterSpacing': '0.18em',
            'color': COLORS['muted'],
            'textTransform': 'uppercase',
            'marginBottom': '0.75rem',
            'whiteSpace': 'nowrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        }),
        html.Div(value, style={
            'fontFamily': 'Rajdhani, sans-serif',
            'fontWeight': '700',
            'fontSize': '2.2rem',
            'color': color or COLORS['cyan'],
            'lineHeight': '1',
            'marginBottom': '0.5rem',
            'textShadow': f'0 0 20px {color or COLORS["cyan"]}40'
        }),
        html.Div(sub, style={
            'fontFamily': 'Share Tech Mono, monospace',
            'fontSize': '0.6rem',
            'color': COLORS['muted'],
            'letterSpacing': '0.1em',
            'whiteSpace': 'nowrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        })
    ], style={
        **card_style(color),
        'height': '100%',
        'minHeight': '120px',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center'
    })

# ── Layout ─────────────────────────────────────────────
app.layout = html.Div([

    # Google Fonts
    html.Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&display=swap'),

    # Navbar
    html.Nav([
        html.Div([
            html.Span('◆', style={'color': COLORS['blue'], 'marginRight': '0.75rem'}),
            html.Span('FUNNEL ANALYSIS', style={
                'fontFamily': 'Share Tech Mono, monospace',
                'fontSize': '0.75rem',
                'letterSpacing': '0.25em',
                'color': COLORS['text']
            }),
            html.Span(' // E-COMMERCE CONVERSION INTELLIGENCE', style={
                'fontFamily': 'Share Tech Mono, monospace',
                'fontSize': '0.6rem',
                'letterSpacing': '0.15em',
                'color': COLORS['muted'],
                'marginLeft': '0.75rem'
            })
        ], style={'display': 'flex', 'alignItems': 'center'}),
        html.Div([
            html.Span('● LIVE', style={
                'fontFamily': 'Share Tech Mono, monospace',
                'fontSize': '0.6rem',
                'color': COLORS['green'],
                'letterSpacing': '0.15em'
            })
        ])
    ], style={
        'background': COLORS['panel'],
        'borderBottom': f'1px solid {COLORS["line"]}',
        'padding': '0.875rem 2rem',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'position': 'sticky',
        'top': '0',
        'zIndex': '100'
    }),

    # Main container
    html.Div([

        # ── FILTERS ROW ──────────────────────────────
        html.Div([
            html.Div([
                html.Label('DEVICE', style={
                    'fontFamily': 'Share Tech Mono, monospace',
                    'fontSize': '0.58rem',
                    'letterSpacing': '0.2em',
                    'color': COLORS['muted'],
                    'marginBottom': '0.4rem',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='filter-device',
                    options=[{'label': 'All Devices', 'value': 'all'}] +
                            [{'label': d.capitalize(), 'value': d}
                             for d in sorted(df['device'].unique())],
                    value='all',
                    clearable=False,
                    style={'background': COLORS['panel2']}
                )
            ], style={'flex': '1'}),

            html.Div([
                html.Label('TRAFFIC SOURCE', style={
                    'fontFamily': 'Share Tech Mono, monospace',
                    'fontSize': '0.58rem',
                    'letterSpacing': '0.2em',
                    'color': COLORS['muted'],
                    'marginBottom': '0.4rem',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='filter-source',
                    options=[{'label': 'All Sources', 'value': 'all'}] +
                            [{'label': s.replace('_', ' ').title(), 'value': s}
                             for s in sorted(df['traffic_source'].unique())],
                    value='all',
                    clearable=False,
                )
            ], style={'flex': '1'}),

            html.Div([
                html.Label('COUNTRY', style={
                    'fontFamily': 'Share Tech Mono, monospace',
                    'fontSize': '0.58rem',
                    'letterSpacing': '0.2em',
                    'color': COLORS['muted'],
                    'marginBottom': '0.4rem',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='filter-country',
                    options=[{'label': 'All Countries', 'value': 'all'}] +
                            [{'label': c, 'value': c}
                             for c in sorted(df['country'].unique())],
                    value='all',
                    clearable=False,
                )
            ], style={'flex': '1'}),

            html.Div([
                html.Label('CATEGORY', style={
                    'fontFamily': 'Share Tech Mono, monospace',
                    'fontSize': '0.58rem',
                    'letterSpacing': '0.2em',
                    'color': COLORS['muted'],
                    'marginBottom': '0.4rem',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='filter-category',
                    options=[{'label': 'All Categories', 'value': 'all'}] +
                            [{'label': c, 'value': c}
                             for c in sorted(df['category'].unique())],
                    value='all',
                    clearable=False,
                )
            ], style={'flex': '1'}),
        ], style={
            'display': 'flex',
            'gap': '1rem',
            'marginBottom': '1.5rem',
            'background': COLORS['panel'],
            'border': f'1px solid {COLORS["line"]}',
            'borderRadius': '4px',
            'padding': '1rem'
        }),

        # ── KPI ROW ───────────────────────────────────
        html.Div(id='kpi-row', style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(5, 1fr)',
            'gap': '1rem',
            'marginBottom': '1.5rem',
            'minHeight': '120px'
        }),

        # ── MAIN FUNNEL + DROPOFF ─────────────────────
        html.Div([
            html.Div([
                dcc.Graph(id='funnel-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['blue']), 'flex': '1.2'}),

            html.Div([
                dcc.Graph(id='dropoff-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['orange']), 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '1rem', 'marginBottom': '1.5rem'}),

        # ── DEVICE + SOURCE ───────────────────────────
        html.Div([
            html.Div([
                dcc.Graph(id='device-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['green']), 'flex': '1'}),

            html.Div([
                dcc.Graph(id='source-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['purple']), 'flex': '1'}),

            html.Div([
                dcc.Graph(id='category-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['gold']), 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '1rem', 'marginBottom': '1.5rem'}),

        # ── COUNTRY + MONTHLY + HOURLY ────────────────
        html.Div([
            html.Div([
                dcc.Graph(id='country-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['cyan']), 'flex': '1'}),

            html.Div([
                dcc.Graph(id='monthly-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['blue']), 'flex': '1.5'}),
        ], style={'display': 'flex', 'gap': '1rem', 'marginBottom': '1.5rem'}),

        # ── REVENUE INSIGHTS ──────────────────────────
        html.Div([
            html.Div([
                dcc.Graph(id='revenue-category', config={'displayModeBar': False})
            ], style={**card_style(COLORS['green']), 'flex': '1'}),

            html.Div([
                dcc.Graph(id='revenue-source', config={'displayModeBar': False})
            ], style={**card_style(COLORS['orange']), 'flex': '1'}),

            html.Div([
                dcc.Graph(id='day-chart', config={'displayModeBar': False})
            ], style={**card_style(COLORS['purple']), 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '1rem', 'marginBottom': '1.5rem'}),

    ], style={
        'maxWidth': 'none',
        'width': '100%',
        'margin': '0',
        'padding': '1.5rem 2rem'
    }),

    # Footer
    html.Footer([
        html.Span('◆ FUNNEL ANALYSIS DASHBOARD', style={
            'fontFamily': 'Share Tech Mono, monospace',
            'fontSize': '0.6rem',
            'letterSpacing': '0.2em',
            'color': COLORS['muted']
        }),
        html.Span('github.com/Subakkumar', style={
            'fontFamily': 'Share Tech Mono, monospace',
            'fontSize': '0.6rem',
            'color': COLORS['blue'],
            'letterSpacing': '0.1em'
        })
    ], style={
        'borderTop': f'1px solid {COLORS["line"]}',
        'padding': '1rem 2rem',
        'display': 'flex',
        'justifyContent': 'space-between',
        'background': COLORS['panel']
    })

], style={
    'background': COLORS['bg'],
    'minHeight': '100vh',
    'color': COLORS['text'],
    'fontFamily': 'Rajdhani, sans-serif'
})

# ── Callbacks ──────────────────────────────────────────
def filter_df(device, source, country, category):
    dff = df.copy()
    if device != 'all':
        dff = dff[dff['device'] == device]
    if source != 'all':
        dff = dff[dff['traffic_source'] == source]
    if country != 'all':
        dff = dff[dff['country'] == country]
    if category != 'all':
        dff = dff[dff['category'] == category]
    return dff

@app.callback(
    [Output('kpi-row', 'children'),
     Output('funnel-chart', 'figure'),
     Output('dropoff-chart', 'figure'),
     Output('device-chart', 'figure'),
     Output('source-chart', 'figure'),
     Output('category-chart', 'figure'),
     Output('country-chart', 'figure'),
     Output('monthly-chart', 'figure'),
     Output('revenue-category', 'figure'),
     Output('revenue-source', 'figure'),
     Output('day-chart', 'figure')],
    [Input('filter-device', 'value'),
     Input('filter-source', 'value'),
     Input('filter-country', 'value'),
     Input('filter-category', 'value')]
)
def update_all(device, source, country, category):
    dff = filter_df(device, source, country, category)
    total     = len(dff)
    converted = int(dff['converted'].sum())
    cvr       = converted / total * 100 if total > 0 else 0
    revenue   = dff['order_value'].sum()
    aov       = revenue / converted if converted > 0 else 0

    # ── KPIs ───────────────────────────────────────── FIXED
    kpis = [
        kpi_card('Total Users', f'{total:,}', 'Sessions analyzed', COLORS['blue']),
        kpi_card('Conversions', f'{converted:,}', 'Completed purchases', COLORS['green']),
        kpi_card('Conv. Rate', f'{cvr:.1f}%', 'Overall CVR', COLORS['cyan']),
        kpi_card('Revenue', f'${revenue:,.0f}', 'Total revenue', COLORS['gold']),
        kpi_card('Avg Order', f'${aov:.2f}', 'Per conversion', COLORS['orange']),
    ]

    # ── Funnel ────────────────────────────────────────
    counts = get_funnel_counts(dff)
    pcts   = [c / counts[0] * 100 if counts[0] > 0 else 0 for c in counts]

    funnel_fig = go.Figure(go.Funnel(
        y=STEP_LABELS,
        x=counts,
        textinfo='value+percent initial',
        marker=dict(
            color=[COLORS['blue'], '#3ba8d4', '#2a8ab5', COLORS['orange'], COLORS['green']],
            line=dict(width=0)
        ),
        connector=dict(line=dict(color=COLORS['line'], width=1)),
        textfont=dict(color=COLORS['text'], size=11)
    ))
    funnel_fig.update_layout(**chart_layout('CONVERSION FUNNEL', 320))

    # ── Drop-off ──────────────────────────────────────
    drops = [(counts[i] - counts[i+1]) / counts[i] * 100
             if counts[i] > 0 else 0
             for i in range(len(counts)-1)]
    drop_labels = [f'{STEP_LABELS[i]}→{STEP_LABELS[i+1]}' for i in range(4)]
    drop_colors = [COLORS['orange'] if d > 40 else '#f97316' if d > 25 else COLORS['gold']
                   for d in drops]

    dropoff_fig = go.Figure(go.Bar(
        x=drops,
        y=drop_labels,
        orientation='h',
        marker=dict(color=drop_colors, line=dict(width=0)),
        text=[f'{d:.1f}%' for d in drops],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=10)
    ))
    dropoff_fig.update_layout(**chart_layout('DROP-OFF RATES', 320))

    # ── Device ────────────────────────────────────────
    dev = dff.groupby('device')['converted'].mean() * 100
    dev = dev.sort_values(ascending=True)
    device_fig = go.Figure(go.Bar(
        x=dev.values, y=dev.index,
        orientation='h',
        marker=dict(
            color=COLORS['chart_colors'][:len(dev)],
            line=dict(width=0)
        ),
        text=[f'{v:.1f}%' for v in dev.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=10)
    ))
    device_fig.update_layout(**chart_layout('CVR BY DEVICE', 280))

    # ── Traffic Source ────────────────────────────────
    src = dff.groupby('traffic_source')['converted'].mean() * 100
    src = src.sort_values(ascending=True)
    source_fig = go.Figure(go.Bar(
        x=src.values,
        y=[s.replace('_', ' ').title() for s in src.index],
        orientation='h',
        marker=dict(color=COLORS['chart_colors'][:len(src)], line=dict(width=0)),
        text=[f'{v:.1f}%' for v in src.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=10)
    ))
    source_fig.update_layout(**chart_layout('CVR BY TRAFFIC SOURCE', 280))

    # ── Category ──────────────────────────────────────
    cat = dff.groupby('category')['converted'].mean() * 100
    cat = cat.sort_values(ascending=False)
    category_fig = go.Figure(go.Bar(
        x=cat.index, y=cat.values,
        marker=dict(color=COLORS['chart_colors'][:len(cat)], line=dict(width=0)),
        text=[f'{v:.1f}%' for v in cat.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=9)
    ))
    category_fig.update_layout(**chart_layout('CVR BY CATEGORY', 280))

    # ── Country ───────────────────────────────────────
    ctry = dff.groupby('country')['converted'].mean() * 100
    ctry = ctry.sort_values(ascending=True)
    country_fig = go.Figure(go.Bar(
        x=ctry.values, y=ctry.index,
        orientation='h',
        marker=dict(color=COLORS['blue'], line=dict(width=0),
                    opacity=[0.5 + 0.5*(v/ctry.max()) for v in ctry.values]),
        text=[f'{v:.1f}%' for v in ctry.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=10)
    ))
    country_fig.update_layout(**chart_layout('CVR BY COUNTRY', 320))

    # ── Monthly trend ─────────────────────────────────
    month_names = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']
    monthly = dff.groupby('month').agg(
        users=('user_id','count'), conversions=('converted','sum')
    )
    monthly['cvr'] = monthly['conversions'] / monthly['users'] * 100
    monthly['rev'] = dff[dff['converted']==1].groupby('month')['order_value'].sum()
    monthly = monthly.reindex(range(1,13), fill_value=0)

    monthly_fig = go.Figure()
    monthly_fig.add_trace(go.Scatter(
        x=[month_names[m-1] for m in monthly.index],
        y=monthly['cvr'],
        name='CVR %',
        line=dict(color=COLORS['blue'], width=2.5),
        fill='tozeroy',
        fillcolor='rgba(79,195,247,0.08)',
        mode='lines+markers',
        marker=dict(color=COLORS['blue'], size=6)
    ))
    monthly_fig.add_trace(go.Bar(
        x=[month_names[m-1] for m in monthly.index],
        y=monthly['users'],
        name='Users',
        marker=dict(color=COLORS['muted'], opacity=0.3, line=dict(width=0)),
        yaxis='y2'
    ))
    monthly_layout = chart_layout('MONTHLY TREND — CVR & VOLUME', 320)
    monthly_layout['legend'] = dict(
        bgcolor='rgba(0,0,0,0)', orientation='h',
        y=1.1, font=dict(size=9)
    )
    monthly_layout['yaxis2'] = dict(
        overlaying='y', side='right', showgrid=False,
        tickfont=dict(size=9, color=COLORS['muted'])
    )
    monthly_fig.update_layout(**monthly_layout)

    # ── Revenue by category ───────────────────────────
    rev_cat = dff[dff['converted']==1].groupby('category')['order_value'].sum()
    rev_cat = rev_cat.sort_values(ascending=False)
    rev_cat_fig = go.Figure(go.Bar(
        x=rev_cat.index, y=rev_cat.values,
        marker=dict(color=COLORS['chart_colors'][:len(rev_cat)], line=dict(width=0)),
        text=[f'${v/1000:.0f}K' for v in rev_cat.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=9)
    ))
    rev_cat_fig.update_layout(**chart_layout('REVENUE BY CATEGORY', 280))

    # ── Revenue per user by source ────────────────────
    rpu = {}
    for s in dff['traffic_source'].unique():
        sub = dff[dff['traffic_source']==s]
        rev_s = sub[sub['converted']==1]['order_value'].sum()
        rpu[s.replace('_',' ').title()] = rev_s / len(sub) if len(sub) > 0 else 0
    rpu_s = pd.Series(rpu).sort_values(ascending=True)
    rev_src_fig = go.Figure(go.Bar(
        x=rpu_s.values, y=rpu_s.index,
        orientation='h',
        marker=dict(color=COLORS['orange'], line=dict(width=0),
                    opacity=[0.5 + 0.5*(v/rpu_s.max()) for v in rpu_s.values]),
        text=[f'${v:.2f}' for v in rpu_s.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=10)
    ))
    rev_src_fig.update_layout(**chart_layout('REVENUE PER USER BY SOURCE', 280))

    # ── Day of week ───────────────────────────────────
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_cvr = dff.groupby('day_of_week')['converted'].mean() * 100
    day_cvr = day_cvr.reindex(day_order, fill_value=0)
    day_colors = [COLORS['purple'] if d in ['Saturday','Sunday'] else COLORS['blue']
                  for d in day_order]
    day_fig = go.Figure(go.Bar(
        x=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        y=day_cvr.values,
        marker=dict(color=day_colors, line=dict(width=0)),
        text=[f'{v:.1f}%' for v in day_cvr.values],
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=9)
    ))
    day_fig.update_layout(**chart_layout('CVR BY DAY OF WEEK', 280))

    return (kpis, funnel_fig, dropoff_fig, device_fig, source_fig,
            category_fig, country_fig, monthly_fig,
            rev_cat_fig, rev_src_fig, day_fig)

# ── Dropdown styles via CSS ────────────────────────────
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
* { box-sizing: border-box; }
body { margin: 0; background: #07080f; scrollbar-width: thin; scrollbar-color: #1e2d3d #07080f; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #07080f; }
::-webkit-scrollbar-thumb { background: #1e2d3d; border-radius: 2px; }

/* Dropdown fixes */
.Select-control {
  background: #0d1018 !important;
  border: 1px solid #1e2d3d !important;
  border-radius: 3px !important;
  color: #e8f4f8 !important;
}

/* Selected value styling - UPDATED */
.Select-value-label,
.Select-value-label span,
.Select--single > .Select-control .Select-value .Select-value-label {
  color: #e8f4f8 !important;
  font-family: "Share Tech Mono", monospace !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.05em !important;
}

/* Placeholder styling */
.Select-placeholder,
.Select-placeholder span {
  color: #6b8fa3 !important;
  font-family: "Share Tech Mono", monospace !important;
  font-size: 0.8rem !important;
}

/* Input styling */
.Select-input input {
  color: #e8f4f8 !important;
  font-family: "Share Tech Mono", monospace !important;
}

/* Arrow styling */
.Select-arrow { 
  border-top-color: #4fc3f7 !important; 
}

/* Dropdown menu */
.Select-menu-outer {
  background: #0d1018 !important;
  border: 1px solid #1e2d3d !important;
  z-index: 999 !important;
}

/* Options styling */
.Select-option {
  background: #0d1018 !important;
  color: #e8f4f8 !important;
  font-family: "Share Tech Mono", monospace !important;
  font-size: 0.75rem !important;
  padding: 8px 12px !important;
}

.Select-option:hover,
.Select-option.is-focused {
  background: #1e2d3d !important;
  color: #4fc3f7 !important;
}

.Select-option.is-selected {
  background: #1e2d3d !important;
  color: #00e5ff !important;
  font-weight: 600 !important;
}

/* Open state */
.dash-dropdown .Select.is-open .Select-control {
  background: #0d1018 !important;
  border-color: #4fc3f7 !important;
}

/* Ensure contrast */
.dash-dropdown {
  font-family: "Share Tech Mono", monospace !important;
}
</style>
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
'''

if __name__ == '__main__':
    app.run(debug=True, port=8050)