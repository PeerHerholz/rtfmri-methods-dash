# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import json

# Styling
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
tabs_styles = {
    'height': '50px',
    'marginLeft': '5%',
    'maxWidth': '90%',
    'fontSize': '20px',
    'fontFamily': 'Trebuchet MS',
    'verticalAlign': 'middle',

}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#586F7C',
    'color': 'white',
    'padding': '10px'
}



# Get data
filename = 'assets/rtfMRI_methods_review_included_studies_procsteps_DEFAULTS.txt'
df_studies = pd.read_csv(filename, sep='\t', lineterminator='\r')
df_studies = df_studies.dropna(axis='columns')
df_plot = df_studies.copy()

colnames = {
    'author':'Author',
    'vendor': 'Vendor',
    'magnet': 'Field strength',
    'software': 'Software',
    'stc': 'Slice time correction',
    'mc': '3D volume realignment',
    'ss': 'Spatial smoothing',
    'dr': 'Drift removal',
    'hmp': 'Realignment parameter regression',
    'ts': 'Temporal smoothing',
    'ff': 'Frequency filtering',
    'or': 'Outlier removal',
    'droi': 'Differential ROI',
    'resp': 'Respiratory noise removal',
    'doi': 'Article DOI'
}

plotnames = [
    {'label': 'Vendor', 'value': 'vendor'},
    {'label': 'Field strength', 'value': 'magnet'},
    {'label': 'Software', 'value': 'software'},
    {'label': 'Slice time correction', 'value': 'stc'},
    {'label': '3D volume realignment', 'value': 'mc'},
    {'label': 'Spatial smoothing', 'value': 'ss'},
    {'label': 'Drift removal', 'value': 'dr'},
    {'label': 'Realignment parameter regression', 'value': 'hmp'},
    {'label': 'Temporal smoothing', 'value': 'ts'},
    {'label': 'Frequency filtering', 'value': 'ff'},
    {'label': 'Outlier removal', 'value': 'or'},
    {'label': 'Differential ROI', 'value': 'droi'},
    {'label': 'Respiratory noise removal', 'value': 'resp'},
]

srs = df_plot['vendor'].value_counts()
xx = srs.index.to_list()
yy = srs.values

dataframe = df_plot.loc[df_plot['vendor'] == 'Siemens']
srs2 = dataframe['magnet'].value_counts()
xx2 = srs2.index.to_list()
yy2 = srs2.values


# Replace 'doi' column values with markdown link to actual doi
for index, row in df_studies.iterrows():
    doi = row['doi']
    doi_link = '[' + doi + ']' + '(https://doi.org/' + doi + ')'
    row['doi'] = doi_link

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])
server = app.server

# make a reuseable navitem for the different examples
nav_item1 = dbc.NavItem(dbc.NavLink("Browse", href="#"))
nav_item2 = dbc.NavItem(dbc.NavLink("Visualize", href="#"))
nav_item3 = dbc.NavItem(dbc.NavLink("Submit", href="#"))

app.layout = html.Div(children=[

    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/logo_jsheunis_3.jpeg', height="30px", className="avatar")),
                            dbc.Col(dbc.NavbarBrand("rtfMRI Methods", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://rtfmri-methods.herokuapp.com/",
                ),
                dbc.NavbarToggler(id="navbar-toggler2"),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item1, nav_item2, nav_item3], className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="mb-5",
    ),


    html.H1(
        children='Real-time fMRI Neurofeedback',
        style={
            'textAlign': 'center',
        }
    ),

    html.H2(children='Browse through literature to find and visualize studies and their methods',
             style={
        'textAlign': 'center',
    }),

    html.Br([]),

    dcc.Tabs([
        dcc.Tab(label='Browse', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                html.H3('Search'),
                dcc.Input(id='my-id', value='', type='text',
                    style={
                        'marginBottom': 0,
                        'marginTop': 0,
                    }
                )],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'textAlign': 'left'
                }
            ),

            dash_table.DataTable(
                id='table',
                columns=[{"name": colnames[i], "id": i, "presentation": "markdown"} for i in df_studies.columns],
                data=df_studies.to_dict('records'),
                style_table={
                    # 'overflowX': 'scroll',
                             'marginLeft': '5%',
                             'maxWidth': '90%',},
                fixed_columns={ 'headers': True, 'data': 0 },
                style_header={
                    'textAlign': 'center',
                    'backgroundColor': '#EBEDEF',
                    'fontWeight': 'bold',
                    # 'textAlign': 'right',
                },
                style_cell={
                    'height': 'auto',
                    # 'minWidth': '0px', 'maxWidth': '150px',
                    'whiteSpace': 'normal',
                    'padding': '4px',
                    'fontSize': '12px',
                    'textAlign': 'left',
                    'fontFamily': 'Trebuchet MS',

                    # all three widths are needed
                    'minWidth': '70px', 'width': '70px', 'maxWidth': '70px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'author'},
                     'minWidth': '130px', 'width': '130px', 'maxWidth': '130px'},
                    {'if': {'column_id': 'doi'},
                     'minWidth': '130px', 'width': '130px', 'maxWidth': '130px' },
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                # css= [{'selector': 'table', 'rule': 'table-layout: fixed;'}]
            )
        ]),
        dcc.Tab(label='Visualize', value='tab-2', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                html.H3('Select study feature(s):'),
                ],
                style={
                    'marginBottom': 10,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'textAlign': 'left'
                }
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Dropdown(
                                id='drop-1',
                                options=plotnames,
                                value='vendor',
                                style={
                                    'marginBottom': 20,
                                    'marginTop': 0,
                                    'width': '60%',
                                },
                            ),),
                            dbc.Col(dcc.Dropdown(
                                id='drop-2',
                                options=plotnames,
                                value='vendor',
                                style={
                                    'marginBottom': 20,
                                    'marginTop': 0,
                                    'width': '60%',
                                },
                            )
                            ),
                        ],
                        justify="end"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.H6(
                                id='graph-1-title',
                                children='Vendor (hover to show options of second feature; click to display studies)',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            ),
                            dbc.Col(html.H6(
                                id='graph-2-title',
                                children='Field strength options when Vendor = Siemens',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                dcc.Graph(
                                    id='graph-1',
                                    figure={
                                        'data': [
                                            {'x': xx, 'y': yy, 'type': 'bar', 'name': 'Vendors', 'marker': {'color': '#9EBC9F'}},
                                        ],
                                    }
                                ),
                            )),
                            dbc.Col(html.Div(
                               dcc.Graph(
                                id='graph-2',
                                    figure={
                                        'data': [
                                            {'x': xx2, 'y': yy2, 'type': 'bar', 'name': 'Field strength', 'marker': {'color': '#D3B88C'}},
                                        ],
                                    }
                                ),
                            )),
                        ]
                    ),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            # html.Table([
            #     html.Tbody([
            #         html.Tr([
            #             html.Td(
            #                 dcc.Graph(
            #                     id='graph-1',
            #                     figure={
            #                         'data': [
            #                             {'x': xx, 'y': yy, 'type': 'bar', 'name': 'Vendors', 'marker': {'color': '#9EBC9F'}},
            #                         ],
            #                         'layout': {
            #                             'title': 'Vendor\n*hover to show options of second feature\n*click to display studies)'
            #                         }
            #                     }
            #                 ),
            #             ),
            #             html.Td(
            #                 dcc.Graph(
            #                     id='graph-2',
            #                     figure={
            #                         'data': [
            #                             {'x': xx2, 'y': yy2, 'type': 'bar', 'name': 'Field strength', 'marker': {'color': '#D3B88C'}},
            #                         ],
            #                         'layout': {
            #                             'title': 'Field strength options when Vendor = Siemens'
            #                         }
            #                     }
            #                 ),
            #             )
            #         ]),
            #     ]),
            #     ],
            #     style={
            #         'marginBottom': 25,
            #         'marginTop': 25,
            #         'marginLeft': '5%',
            #         'maxWidth': '90%',
            #     }),

            html.Div(
                id='table-1',
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }),
        ]),
    ], style=tabs_styles),


],
# style={
#     'marginLeft': '5%',
#     'maxWidth': '90%',
# }
)



###########################
# CALLBACKS AND FUNCTIONS #
###########################

# Callback for table search function
@app.callback(
    Output('table', 'data'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):

    mask = np.column_stack([df_studies[col].str.contains(input_value, case=False, regex=False, na=False) for col in df_studies])
    df = df_studies.loc[mask.any(axis=1)]
    data = df.to_dict('records')

    return data


# Callback for updating graph 1
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-1-title', 'children')],
    [Input('drop-1','value')]
)
def update_graph(feature):

    srs = df_plot[feature].value_counts()
    xx = srs.index.to_list()
    yy = srs.values
    txt = colnames[feature]

    fig={
        'data': [
            {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#9EBC9F'}},
        ],
    }

    title = txt + ' (hover to show options of second feature; click to display studies)'


    return [fig, title]

# Callback for updating dropdown2 based on dropdown1 value
@app.callback(
    [Output('drop-2', 'options'),
     Output('drop-2', 'value')],
    [Input('drop-1','value')]
)
def reset_dropdown2_opts(value):
    plotnames_2 = [x for x in plotnames if x['value'] != value]
    value_2 = plotnames_2[0]['value']
    return plotnames_2, value_2


# Callback for updating graph 2 based on graph1 hoverData and dropdowns
@app.callback(
    [Output('graph-2', 'figure'),
     Output('graph-2-title', 'children')],
    [Input('graph-1', 'hoverData'),
     Input('drop-1','value'),
     Input('drop-2','value')]
)
def update_graph(hoverData, feature1, feature2):
    if hoverData is None or feature1 is None or feature2 is None:
        raise PreventUpdate
    else:
        x = hoverData['points'][0]['x']
        dataframe = df_plot.loc[df_plot[feature1] == x]
        srs = dataframe[feature2].value_counts()
        xx = srs.index.to_list()
        yy = srs.values
        txt = colnames[feature2] + ' options when ' + colnames[feature1] + ' = ' + x

        fig={
            'data': [
                {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#D3B88C'}},
            ],
        }

        title = txt

        return [fig, title]


# Callback for showing table 1 after filtering on feature 1
@app.callback(
    Output('table-1', 'children'),
    [Input('graph-1', 'clickData'),
     Input('drop-1','value')])
def generate_table(clickData, feature, max_rows=20):

    if clickData is None:
        raise PreventUpdate
    else:
        x = clickData['points'][0]['x']

        dataframe = df_plot.loc[df_plot[feature] == x]
        table=html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in list(colnames.values())])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(writeElement(i, col, dataframe)) for col in dataframe.columns],
                ) for i in range(min(len(dataframe), max_rows))
            ]),
            ],
            className='qcsummary',
        )

        # class="table-row" data-href="http://tutorialsplane.com"

        heading=html.H4('Showing studies where ' + colnames[feature] + ' = ' + x,
                        style={'textAlign': 'center',})

        # table = dbc.Table.from_dataframe(dataframe,
        #                                  striped=True,
        #                                  bordered=True,
        #                                  hover=True,
        #                                  responsive=True,
        #                                  className='qcsummary'
        #                                  )

        return [heading, table]


# # Callback for showing table after filtering on feature 2
# @app.callback(
#     Output('table-1', 'children'),
#     [Input('graph-1', 'clickData'),
#      Input('graph-1', 'hoverData'),
#      Input('graph-2', 'clickData'),
#      Input('drop-1','value'),
#      Input('drop-2','value')])
# def generate_table2(clickData1, hoverData, clidkData2, feature1, feature2, max_rows=20):
#
#     if clickData1 is None:
#         raise PreventUpdate
#     else:
#         x_hover = hoverData['points'][0]['x']
#         x_click = clickData['points'][0]['x']
#
#         df = df_plot.loc[df_plot[feature1] == x_hover]
#         dataframe = df.loc[df[feature2] == x_click]
#
#         table=html.Table([
#             html.Thead(
#                 html.Tr([html.Th(col) for col in list(colnames.values())])
#             ),
#             html.Tbody([
#                 html.Tr([
#                     html.Td(writeElement(i, col, dataframe)) for col in dataframe.columns]
#                 ) for i in range(min(len(dataframe), max_rows))
#             ]),
#             ],
#             className='qcsummary',
#         )
#         return table




def writeElement(i, col, dataframe):
    if col == 'doi':
        hrf = 'https://doi.org/'+dataframe.iloc[i][col]
        return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    else:
        return dataframe.iloc[i][col]



# the same function (toggle_navbar_collapse) is used in all three callbacks
@app.callback(
    Output("navbar-collapse2", "is_open"),
    [Input("navbar-toggler2", "n_clicks")],
    [State("navbar-collapse2", "is_open")],
)
def toggle_navbar_collapse(n, is_open): # we use a callback to toggle the collapse on small screens
    if n:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run_server(debug=True)