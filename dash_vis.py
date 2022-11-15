# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#1a1c23',
    'text': '#7FDBFF'
}
datat = pd.read_excel("C:\\Users\\BaoBao\\Downloads\\demo\\country.xlsx")
df = pd.read_excel("C:\\Users\BaoBao\\Downloads\\demo\\data.xlsx")
home = df.groupby(['Year', 'Home Team'])['Home Team.1'].sum()
away = df.groupby(['Year', 'Away Team.1'])['Away Team'].sum()
goals = pd.concat([home, away], axis=1)
goals.fillna(0, inplace=True)
goals['Goals'] = goals['Home Team.1'] + goals['Away Team']
goals = goals.reset_index()
goals.drop(['Home Team.1', 'Away Team'], axis=1)
goals = goals[['Year', 'level_1', 'Goals']]
goals = goals.rename(columns={"level_1": "Team"})
goals = goals.sort_values(by=['Year', 'Goals'], ascending=[True, False])


def chart_score_goal_ever_year():
    line_graph = px.line(goals, x='Year', y='Goals', color='Team',
                      title='Tổng điểm của từng đội qua các kỳ WC', log_y=True)

    line_graph.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return line_graph


def Top5_Teams_with_most_Goals():

    top5 = goals.groupby('Year').head()
    top5.head(10)
    data = []
    for team in top5['Team'].drop_duplicates().values:
        year = top5[top5['Team'] == team]['Year']
        goal = top5[top5['Team'] == team]['Goals']

        data.append(go.Bar(x=year, y=goal, name=team))
    layout = go.Layout(
        barmode='stack', title='Top 5 đội có số bàn thắng nhiều nhất', showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )

    return fig


def map_City_WC():

    wc = pd.read_csv(r'C:\\Users\\BaoBao\\Downloads\\demo\\World_Cities_Location_table_MS-EXCEL.csv') 
    lst = list(df["City"])
    lst = list(set(lst))
    wc = wc[wc.city.isin(lst)]
    fig = px.choropleth(locationmode='country names', locations=wc.Country,color_continuous_scale="magenta",
                    color=wc.Country # size of markers, "pop" is one of the columns of gapminder
                    )
    fig1 = go.Figure(data=go.Scattergeo(
            lon = wc['x'],
            lat = wc['y'],
            text = wc['city'] ,
            mode = 'markers',
            marker=dict(
                color='white',
                size=3
            )
    #         marker_color ="purple"
            ))

    fig.add_trace(fig1.data[0])
    fig.update_layout(title = 'BIỂU ĐỒ THỂ HIỆN CÁC THÀNH PHỐ DIỄN RA WORLD CUP 1930 - 2014', title_y=0.95)
    fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
    )
    return fig
def total_attendance_with_year():
    df_att = df.groupby(by='Year')['Attendance'].apply(sum)
    fig1 = px.line(df_att, title='Số lượng khán giả qua các kì WC')
    fig1.update_layout(xaxis_title='Year', yaxis_title='Số lượng khán giá')
    fig1.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig1


def sum_goals_of_year():
    df['Goals'] = df['Home Team.1'] + df['Away Team']
    box_plot = px.box(df, x="Year", y="Goals", color='Year', points='outliers',title="Tổng số bàn thắng ghi được từ năm 1930-2014")
    box_plot.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return box_plot
def champion_in_year():
    fig2 = px.bar(datat, x = datat['Country'], y = datat['Champion'], color = 'Country',title="Các đội vô địch từ năm 1930")
    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig2
def total_match_in_year():
    dataset = df.groupby(by=['Year'])['Stage'].count()
    fig3=px.scatter(data_frame=dataset,y='Stage',trendline='lowess')
    fig3.update_layout(title='Số trận đấu qua các năm',xaxis_title='Năm',yaxis_title='Tổng số trận')
    fig3.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig3

def build_header():
    return html.Div(
        className="col-xl-12 col-md-12 col-xs-12 col-lg-12",
        children=[
            html.H1(
                className="text-center",
                children=[
                    "Bảng tổng hợp các thành tích trong lịch sử qua các kỳ WC"
                ]
            )
        ]
    )


def build_body():
    return html.Div(
        className="col-xl-12 col-md-12 col-xs-12 col-lg-12",
        children=[
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                        children=[
                            dcc.Graph(
                                id="chart-score-goal",
                                figure=total_attendance_with_year()
                            )
                        ],
                        style={
                            "max-width": "100%",
                            "background-color": "#30333d"
                        }
                    ),
                    html.Div(
                        className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                        children=[
                            dcc.Graph(
                                id="top-5-team-with-goals",
                                figure=Top5_Teams_with_most_Goals()
                            )
                        ],
                        style={
                            "background-color": "#30333d"
                        }
                    )
                ],
                style={
                    "margin-top": "10px"
                }
            ),
            html.Div(
                className="row ",
                children=[
                    html.Div(
                        className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                        children=[
                            dcc.Graph(
                                id="map-City",
                                figure=map_City_WC()
                            )
                        ],
                        style={
                            "background-color": "#30333d"
                        }
                    ),
                    html.Div(
                        className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                        children=[
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="col-xl-12 col-md-12 col-xs-12 col-lg-12",
                                        children=[
                                            dcc.Graph(
                                                id="sum-goals",
                                                figure=sum_goals_of_year()
                                            )
                                        ],
                                        style={
                                                    "background-color": "#30333d"
                                                }
                                        )
                                ]
                            )
                        ]
                    )
                ],
                style={
                    "margin-top": "10px"
                }
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                        children=[
                            dcc.Graph(
                                id="champion-in-yeaer",
                                figure=champion_in_year()
                            )
                        ]
                    ),
                    html.Div(
                                className="col-xl-6 col-md-12 col-xs-12 col-lg-6",
                                children=[
                                    dcc.Graph(
                                        id="match-in-year",
                                        figure=total_match_in_year()
                                    )
                                ]
                            )
                ],
                style={
                    "margin-top": "10px"
                }
            )
        ]
    )

app.layout=html.Div(
    className= "container-fluid",
    children = [
        html.Div(
            className="row shadow",
            children=[
                build_header()
            ]
        ),
        html.Div(
            className="row ",
            children=[
                build_body()
            ],
            style={
                "background-color": "#30333d"
            }
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug = True)
