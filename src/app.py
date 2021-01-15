import dash
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div('5-star Insights ')

if __name__ == '__main__':
    app.run_server(debug=True)