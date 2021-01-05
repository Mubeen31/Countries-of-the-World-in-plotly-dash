import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


world = pd.read_csv('countries of the world.csv')

world['Region'] = world['Region'].str.replace("," , ".").astype('object')
world['Net migration'] = world['Net migration'].str.replace("," , ".").astype('float64')
world['Birthrate'] = world['Birthrate'].str.replace("," , ".").astype('float64')
world['Deathrate'] = world['Deathrate'].str.replace("," , ".").astype('float64')
world['Pop. Density (per sq. mi.)'] = world['Pop. Density (per sq. mi.)'].str.replace("," , ".").astype('float64')
world['Infant mortality (per 1000 births)'] = world['Infant mortality (per 1000 births)'].str.replace("," , ".").astype('float64')

world.fillna(0, inplace=True)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

html.Div([
    html.Div([
       html.Div([
        html.H3('World Countries Information', style={'margin-bottom': '0px', 'color': 'white'}),
    ])
             ], className="create_container1 four columns", id="title"),


        ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),


# drop down list (region)
html.Div([
html.Div([
        html.P('Select Region', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
        dcc.Dropdown(id='select_region',
                     multi=False,
                     clearable=True,
                     disabled=False,
                     style={'display': True},
                     value='EASTERN EUROPE                     ',
                     placeholder='Select Countries',
                     options=[{'label': c, 'value': c}
                              for c in (world['Region'].unique())], className='dcc_compon')

         ], className="create_container1 four columns",  style={'margin-bottom': '8px'}),

    ], className="row flex-display"),




# data table
html.Div([
html.Div([
      dt.DataTable(id='my_datatable',
                   columns=[{'id': c, 'name': c} for c in world.columns.values],
                   # page_action='native',
                   # page_size=20,
                   # editable=False,
                   sort_action="native",
                   sort_mode="multi",
                   # column_selectable="single",
                   # fill_width=False,
                   # style_table={
                   #         "width": "100%",
                   #         "height": "100vh"},
                   virtualization=True,
                   style_cell={'textAlign': 'left',
                               'min-width': '230px',
                               'backgroundColor': '#010915',
                               'color': '#FEFEFE',
                               'border-bottom': '0.01rem solid #313841',
                               },
                   style_as_list_view=True,
                   style_header={
                       'backgroundColor': '#010915',
                       'fontWeight': 'bold',
                       'font': 'Lato, sans-serif',
                       'color': 'orange',
                       'border': '#010915',
                        },
                   style_data={'textOverflow': 'hidden', 'color': 'white'},
                   fixed_rows={'headers': True}
                   )

    ], className='create_container six columns'),

# horizontal bar chart (top countries)
html.Div([
    html.Br(),
    dcc.Graph(id='top_1',
              config={'displayModeBar': 'hover'}),

        ], className='create_container six columns'),

 ], className='row flex-display'),

# combination of bar and line chart (population and area)
html.Div([
html.Div([
    html.Br(),
    dcc.Graph(id='bar_line_1',
              config={'displayModeBar': 'hover'}),

        ], className='create_container six columns'),

# line chart (birth rate vs death rate)
html.Div([
    html.Br(),
    dcc.Graph(id='line_1',
              config={'displayModeBar': 'hover'}),

        ], className='create_container six columns'),

], className='row flex-display'),

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

# data table
@app.callback(
    Output('my_datatable', 'data'),
    [Input('select_region', 'value')])
def display_table(select_region):
    data_table = world[world['Region'] == select_region]
    return data_table.to_dict('records')

# horizontal bar chart (top countries)
@app.callback(Output('top_1', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):
    top_country = world.groupby(['Region', 'Country'])[['Population', 'Area (sq. mi.)']].sum().reset_index()
    top_country_world = top_country[top_country['Region'] == select_region].sort_values(by='Population', ascending=False)


    return {
        'data': [go.Bar(x=top_country_world[top_country_world['Region'] == select_region]['Population'],
                            y=top_country_world[top_country_world['Region'] == select_region]['Country'],
                            text=top_country_world[top_country_world['Region'] == select_region]['Population'],
                            texttemplate='%{text:,.0s}',
                            textposition='auto',
                            marker=dict(color='#04B77A'),
                            orientation='h',
                            hoverinfo='text',
                            hovertext=
                            '<b>Region</b>: ' + top_country_world[top_country_world['Region'] == select_region]['Region'].astype(str) + '<br>' +
                            '<b>Country</b>: ' + top_country_world[top_country_world['Region'] == select_region]['Country'].astype(str) + '<br>' +
                            '<b>Population</b>: ' + [f'{x:,.0f}' for x in top_country_world[top_country_world['Region'] == select_region]['Population']] + '<br>' +
                            '<b>Area (sq. mi.)</b>: ' + [f'{x:,.0f}' for x in top_country_world[top_country_world['Region'] == select_region]['Area (sq. mi.)']] + '<br>'


                           )],

        'layout': go.Layout(
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
             title={
                'text': 'Top Countries :' + (select_region),
                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 15},

             hovermode='closest',
             margin=dict(l=130, b=0, r=0, t=17),

             xaxis=dict(title='<b>Population</b>',

                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b></b>',
                        autorange='reversed',
                        color='white',
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                )

        )
    }

# combination of bar and line chart (population and area)
@app.callback(Output('bar_line_1', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):
    world_pop = world.groupby(['Region', 'Country', 'Pop. Density (per sq. mi.)', 'Net migration', 'Infant mortality (per 1000 births)'])[['Population', 'Area (sq. mi.)']].mean().reset_index()


    return {
        'data':[go.Bar(
                    x=world_pop[world_pop['Region'] == select_region]['Country'],
                    y=world_pop[world_pop['Region'] == select_region]['Population'],
                    name='Population',
                    yaxis='y1',
                    marker=dict(
                          color=world_pop[world_pop['Region'] == select_region]['Population'],
                          colorscale='sunsetdark',
                          showscale=False),

                  hoverinfo='text',
                  hovertext=
                  '<b>Region</b>: ' + world_pop[world_pop['Region'] == select_region]['Region'].astype(str) + '<br>' +
                  '<b>Country</b>: ' + world_pop[world_pop['Region'] == select_region]['Country'].astype(str) + '<br>' +
                  '<b>Population</b>: ' + [f'{x:,.0f}' for x in world_pop[world_pop['Region'] == select_region]['Population']] + '<br>' +
                  '<b>Pop. Density (per sq. mi.)</b>: ' + world_pop[world_pop['Region'] == select_region]['Pop. Density (per sq. mi.)'].astype(str) + '<br>' +
                  '<b>Net migration</b>: ' + world_pop[world_pop['Region'] == select_region]['Net migration'].astype(str) + '<br>' +
                  '<b>Infant mortality (per 1000 births)</b>: ' + world_pop[world_pop['Region'] == select_region]['Infant mortality (per 1000 births)'].astype(str) + '<br>'


              ),

               go.Scatter(
                   x=world_pop[world_pop['Region'] == select_region]['Country'],
                   y=world_pop[world_pop['Region'] == select_region]['Area (sq. mi.)'],
                   name='Area (sq. mi.)',
                   mode='markers+lines',
                   yaxis='y2',
                   marker=dict(color='orange'),
                   hoverinfo='text',
                   hovertext=
                   '<b>Country</b>: ' + world_pop[world_pop['Region'] == select_region]['Country'].astype(str) + '<br>' +
                   '<b>Area (sq. mi.)</b>: ' + [f'{x:,.0f}' for x in world_pop[world_pop['Region'] == select_region]['Area (sq. mi.)']] + '<br>'

            )],


        'layout': go.Layout(
             # width=1030,
             # height=520,
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': 'Region : ' + (select_region),

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'white',
                        'size': 15},

             hovermode='x',
             margin=dict(b=100),

             xaxis=dict(title='<b></b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b>Population</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                ),

             yaxis2=dict(title='<b>Area</b>', overlaying='y', side='right',
                        color='white',
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                        ),

             legend=dict(title='',
                         x=0.3,
                         y=1.2,
                         orientation='h',
                         bgcolor='#010915',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='white')),


                 )

    }

# line chart (birth rate vs death rate)
@app.callback(Output('line_1', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):
    world_pop_1 = world.groupby(['Region', 'Country'])[['Birthrate', 'Deathrate']].mean().reset_index()


    return {
        'data': [go.Scatter(
                   x=world_pop_1[world_pop_1['Region'] == select_region]['Country'],
                   y=world_pop_1[world_pop_1['Region'] == select_region]['Birthrate'],
                   name='Birth Rate',
                   mode='markers+lines',
                   marker=dict(color='green'),
                   hoverinfo='text',
                   hovertext=
                   '<b>Region</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Region'].astype(str) + '<br>' +
                   '<b>Country</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Country'].astype(str) + '<br>' +
                   '<b>Birth Rate</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Birthrate'].astype(str) + '<br>'

            ),

            go.Scatter(
                x=world_pop_1[world_pop_1['Region'] == select_region]['Country'],
                y=world_pop_1[world_pop_1['Region'] == select_region]['Deathrate'],
                name='Death Rate',
                mode='markers+lines',
                marker=dict(color='red'),
                hoverinfo='text',
                hovertext=
                '<b>Death Rate</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Deathrate'].astype(str) + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': 'Region : ' + (select_region),

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'white',
                        'size': 15},

             hovermode='x',
             margin=dict(b=100),

             xaxis=dict(title='<b></b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                        ),

             yaxis=dict(title='<b>Population</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                        ),

             legend=dict(title='',
                         x=0.35,
                         y=1.2,
                         orientation='h',
                         bgcolor='#010915',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='white')),


                 )

    }



if __name__ == '__main__':
    app.run_server(debug=True)