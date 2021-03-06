import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import random
import dash_table_experiments
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash_table_experiments as dash_table
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly_express as px
import plotly.offline as pyo

get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrate e Solte Aqui O Orderlines Descompactado ou ',
            html.A('Clique para selecionar')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
], style={'marginLeft': 50, 'marginRight': 50})


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            
             
            
            df = pd.read_csv(
                io.StringIO(decoded.decode('latin-1')))
            
            
            """fdr4= df.groupby(['Machine', 'Time']).sum()
            fdr4.reset_index(inplace=True)
            
            fig = px.scatter(fdr4, x="Time", y="Units Pruduced", color="Machine", template="plotly_dark")
            fig.update_traces(mode='lines+markers')"""
            
            
            df1 = df
            #df2 = df
            

            df1.rename(columns={"Order Type": "OrderType"}, inplace=True)
            df1.rename(columns={df1.columns[40]:'ProcessFinishTime'}, inplace=True)
            df1.rename(columns={df1.columns[30]:'ProcessStartTime'}, inplace=True)
            df1.rename(columns={df1.columns[12]:'HoraDrop'}, inplace=True)

            dforder = df1.groupby('Order No').sum().round(2)
            dforder = df1.pivot_table(index='Order No', aggfunc='sum').round(2)

            dfmedir = df1[['Order No', 'OrderType','ProcessStartTime','ProcessFinishTime']]
            dfmedir['UnidadesProcessadas'] = 0

            #dfmedir.drop(['index'], axis=1, inplace=True)
            dforder.reset_index(inplace=True)

            # Convertendo tempos

            dfmedir = pd.merge(dfmedir, dforder[['Order No','Qty']], on='Order No', how='left')


            df1.loc[(df1.ProcessFinishTime == '::'), 'ProcessFinishTime'] = 0
            df1.loc[(df1.ProcessStartTime == '::'), 'ProcessStartTime'] = 0
            dfmedir.loc[(dfmedir.ProcessFinishTime == '::'), 'ProcessFinishTime'] = 0
            dfmedir.loc[(dfmedir.ProcessStartTime == '::'), 'ProcessStartTime'] = 0
            dfmedir.loc[(dfmedir.ProcessFinishTime != 0), 'UnidadesProcessadas'] = dfmedir['Qty']




            df1['ProcessFinishTime'] = pd.to_datetime(df1['ProcessFinishTime'])
            df1['ProcessStartTime'] = pd.to_datetime(df1['ProcessStartTime'])
            df1['HoraDrop'] = pd.to_datetime(df1['HoraDrop'])
            df1['TimeOfProcess'] = df1['ProcessFinishTime'] - df1['ProcessStartTime']
            df1['TimeOfProcess'] = pd.to_datetime(df1['TimeOfProcess'])




            df1['ProcessFinishTime'] = pd.to_datetime(df1['ProcessFinishTime'],errors='ignore')
            df1['ProcessStartTime'] = pd.to_datetime(df1['ProcessStartTime'],errors='ignore')
            df1['TimeOfProcess'] = df1['ProcessFinishTime'] - df1['ProcessStartTime']
            df1['TimeOfProcess'] = pd.to_datetime(df1['TimeOfProcess'],errors='ignore')

            dfmedir['ProcessFinishTime'] = pd.to_datetime(dfmedir['ProcessFinishTime'],errors='ignore')
            dfmedir['ProcessStartTime'] = pd.to_datetime(dfmedir['ProcessStartTime'],errors='ignore')




            dfmedir.drop_duplicates('Order No', inplace=True)

            dfmedir['ProcessFinishTime'] = pd.to_datetime(dfmedir['ProcessFinishTime'],errors='ignore')
            dfmedir['ProcessStartTime'] = pd.to_datetime(dfmedir['ProcessStartTime'],errors='ignore')
            dfmedir['TimeOfProcess'] = dfmedir['ProcessFinishTime'] - dfmedir['ProcessStartTime']

            dfmedir['Time Proc Seg'] = (dfmedir['TimeOfProcess'].dt.total_seconds().astype(int))
            dfmedir['Horas Trabalhadas'] = ((dfmedir['Time Proc Seg'] / 3600).round(2))
            #Teste De Processamento

            df1.loc[(df1.Processed != '::'), 'UnidadesProcessadas'] = df1['Qty']
            df1.loc[(df1.Processed == '::'), 'UnidadesProcessadas'] = 0
            #df1.loc[(df1.Processed == '::'), 'UnidadesProcessadas'] = 0
            dfmedir['Unidades Pendentes'] = dfmedir['Qty'] - dfmedir['UnidadesProcessadas']





            dfmedir.loc[(dfmedir.UnidadesProcessadas == 0), 'Time Proc Seg'] = 0
            dfmedir.loc[(dfmedir.UnidadesProcessadas == 0), 'Horas Trabalhadas'] = 0


            dfmedirgrouped = dfmedir

            dfmedirgrouped['Hora'] = dfmedirgrouped['ProcessFinishTime'].apply(lambda x: x.hour)

            dfmedirgrouped = dfmedir.groupby('Order No').sum()
            dfmedirgrouped.reset_index(inplace=True)


            dfmedirgrouped.drop_duplicates('Order No', inplace=True)
            #dfmedirgrouped['UPH'] = dfmedirgrouped['UnidadesProcessadas'] / dfmedirgrouped['Horas Trabalhadas']
            dfmedirgrouped = pd.merge(dfmedirgrouped, dfmedir[['Order No','OrderType']], on='Order No', how='left')
            dfmedirgrouped = pd.merge(dfmedirgrouped, df1[['Order No',' Packout station Number']], on='Order No', how='left')
            dfmedirgrouped = pd.merge(dfmedirgrouped, df1[['Order No','Packout station Operator']], on='Order No', how='left')
            dfmedirgrouped.drop_duplicates('Order No', inplace=True)


            dfoperador = dfmedirgrouped.groupby('Packout station Operator').sum()
            dfoperador.reset_index(inplace=True)
            dfoperador['UPH'] =  (dfoperador['UnidadesProcessadas'] / dfoperador['Horas Trabalhadas']).round(2)

            dfordertype = dfmedirgrouped.groupby('OrderType').sum().round(2)
            dfordertype.reset_index(inplace=True)
            dfordertype['UPH'] =  (dfordertype['UnidadesProcessadas'] / dfordertype['Horas Trabalhadas']).round(2)

            dfstation = dfmedirgrouped.groupby(' Packout station Number').sum()
            dfstation.reset_index(inplace=True)
            dfstation['UPH'] =  (dfstation['UnidadesProcessadas'] / dfstation['Horas Trabalhadas']).round(2)


            
           

            dfmedirgrouped['MM_10'] = dfmedirgrouped['UnidadesProcessadas'].rolling(window=10).mean()
            dfmedirgrouped['MM_20'] = dfmedirgrouped['UnidadesProcessadas'].rolling(window=20).mean()
            dfmedirgrouped['MM_30'] = dfmedirgrouped['UnidadesProcessadas'].rolling(window=30).mean()


            # Agrupamentos


            df2 = df1.groupby('OrderType').sum()

            df3 = df1.groupby(' Packout station Number').sum()
            df4 = df1.groupby('Packout station Operator').sum()
            df5 = df1.groupby('Product Category').sum()
            df1.rename(columns={df1.columns[12]:'Received Time'}, inplace=True)
            df6 = df1.groupby('Received Time').sum()
            df7 = df1.groupby('Cut Off Time').sum()
            df1['HoraDrop'] = df1['Received Time'].apply(lambda x: x.hour)
            dfdrop = df1.groupby(['OrderType', 'HoraDrop']).sum()
            dfdrop.reset_index(inplace=True)
            # Convertendo tempos

            dfmedir['HoraDrop'] = df1['Received Time'].apply(lambda x: x.hour)
            dfdrop2 = dfmedir.groupby(['HoraDrop', 'OrderType']).sum()
            dfdrop2.reset_index(inplace=True)
            
            dfordertype['ETA'] = (dfordertype['Unidades Pendentes'] / dfordertype['UPH']).round(2)


            # Calculando UnidadesProcessadas por hora

            df8 = df1.groupby('OrderType').sum()
            
            #DFYPPH
            dfupph = dfmedirgrouped.groupby(['Packout station Operator','Hora','OrderType']).sum()
            dfupph['UPPH'] = dfupph['UnidadesProcessadas'] / dfupph['Horas Trabalhadas']
            dfupph.reset_index(inplace=True)
            npessoas = dfupph['Packout station Operator'].unique()
            npessoas = len(npessoas)+1
            dfupphcanal = dfupph.groupby(['OrderType', 'Hora']).sum()
            dfupphcanal.reset_index(inplace=True)
            dfupphcanal['UPH'] = (dfupphcanal['UnidadesProcessadas'] / dfupphcanal['Horas Trabalhadas']).round(2)
            dfupphcanal['UPPH'] = (dfupphcanal['UPH'] / npessoas).round(2)
            
            
            
            # Resetando indices

            df2.reset_index(inplace=True)
            df3.reset_index(inplace=True)
            df4.reset_index(inplace=True)
            df5.reset_index(inplace=True)
            df6.reset_index(inplace=True)
            df7.reset_index(inplace=True)

            tabelaordertype = dfordertype
            tabelaordertype.drop(['Order No', 'Time Proc Seg', 'Hora'],axis=1, inplace=True)
            tabelaordertype = tabelaordertype['Horas Trabalhadas'].round(2)
            
            
            df9 = dfmedirgrouped.groupby(['OrderType', 'Hora']).sum()
            df9.reset_index(inplace=True)
            
            
            groups2 = df9.groupby(by='OrderType')

            data2 = []
            colors2=get_colors(50)

            for group2, dataframe2 in groups2:
                dataframe2 = dataframe2.sort_values(by=['Hora'])
                trace2 = go.Scatter(x=dataframe2.Hora.tolist(), 
                                   y=dataframe2.UnidadesProcessadas.tolist(),
                                   marker=dict(color=colors2[len(data2)]),
                                   name=group2)
                data2.append(trace2)

            layout2 =  go.Layout(xaxis={'title': 'Time'},
                                yaxis={'title': 'Produced Units'},
                                margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                hovermode='closest',
                                template='plotly_white')

            figure2 = go.Figure(data=data2, layout=layout2) 
            
            df10 = dfmedirgrouped.groupby([' Packout station Number', 'Hora']).sum()
            df10.reset_index(inplace=True)


            groups3 = df10.groupby(by=' Packout station Number')

            data3 = []
            colors3=get_colors(50)

            for group3, dataframe3 in groups3:
                dataframe3 = dataframe3.sort_values(by=['Hora'])
                trace3 = go.Scatter(x=dataframe3.Hora.tolist(), 
                                    y=dataframe3.UnidadesProcessadas.tolist(),
                                    marker=dict(color=colors3[len(data3)]),
                                    name=group3,
                                   )
                data3.append(trace3)

                layout3 =  go.Layout(xaxis={'title': 'Hora'},
                                    yaxis={'title': 'Unidades Produzidas'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest',
                                    template='plotly_white')

            figure3 = go.Figure(data=data3, layout=layout3)
            
            df11 = dfmedirgrouped.groupby(['Packout station Operator', 'Hora']).sum()
            df11.reset_index(inplace=True)


            groups4 = df11.groupby(by='Packout station Operator')

            data4 = []
            colors4=get_colors(50)

            for group4, dataframe4 in groups4:
                dataframe4 = dataframe4.sort_values(by=['Hora'])
                trace4 = go.Scatter(x=dataframe4.Hora.tolist(), 
                                    y=dataframe4.UnidadesProcessadas.tolist(),
                                    marker=dict(color=colors4[len(data4)]),
                                    name=group4,
                                   )
                data4.append(trace4)

                layout4 =  go.Layout(xaxis={'title': 'Hora'},
                                    yaxis={'title': 'Unidades Produzidas'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest',
                                    template='plotly_white')

            figure4 = go.Figure(data=data4, layout=layout4)
            
            
            dfmm = dfmedirgrouped.groupby('Hora').sum()

            dfmm.reset_index(inplace=True)
            


            dfmm = dfmm.drop(dfmm[dfmm.Hora == 0].index)



            tracemm10 = go.Scatter(x=dfmm.Hora.tolist(), 
                                y=dfmm.MM_10.tolist(),
                                name='MM_10',
                                )

            tracemm20 = go.Scatter(x=dfmm.Hora.tolist(), 
                                y=dfmm.MM_20.tolist(),
                                name='MM_20',
                                )
            tracemm30 = go.Scatter(x=dfmm.Hora.tolist(), 
                                y=dfmm.MM_30.tolist(),
                                name='MM_30',
                                )
            traceunidades = go.Bar(x=dfmm.Hora.tolist(), 
                                y=dfmm.UnidadesProcessadas.tolist(),
                                name='Qty Produzida',
                                marker_color='blue'
                                
                                )


            datamm = (tracemm10, tracemm20,tracemm30, traceunidades)

            layoutmm =  go.Layout(xaxis={'title': 'Hora'},
                                yaxis={'title': 'Unidades Produzidas'},
                                margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                hovermode='closest',
                                template='plotly_white')

            figuremm = go.Figure(data=datamm, layout=layoutmm)
            
            dfmmcanal = dfmedirgrouped.groupby(['Hora', 'OrderType']).sum()
            dfmmcanal.reset_index(inplace=True)
            dfmmcanal = dfmmcanal.drop(dfmmcanal[dfmmcanal.Hora == 0].index)

            groups7 = dfmmcanal.groupby(by='OrderType')

            data7 = []
            colors7=get_colors(50)

            for group7, dataframe7 in groups7:
                dataframe7 = dataframe7.sort_values(by=['Hora'])
                trace7 = go.Scatter(x=dataframe7.Hora.tolist(), 
                                    y=dataframe7.MM_10.tolist(),
                                    marker=dict(color=colors7[len(data7)]),
                                    name=group7,
                                   )


                data7.append(trace7)

                layout7 =  go.Layout(xaxis={'title': 'Hora'},
                                    yaxis={'title': 'Unidades Produzidas'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest',
                                    template='plotly_white',
                                    title='Média Móvel 10 Intervalos Por Canal')
            figure7 = go.Figure(data=data7, layout=layout7)
            
            dfgraphdrop = df1.groupby(['HoraDrop', 'OrderType']).sum()
            dfgraphdrop.reset_index(inplace=True)
            groupsdn = dfgraphdrop.groupby(by='OrderType')

            tracefd = go.Bar(x=dfdrop2.HoraDrop.tolist(), 
                    y=dfdrop2.Qty.tolist(),
                    name='Dropado',
                    )
                    


            tracefd2 = go.Bar(x=dfdrop2.HoraDrop.tolist(), 
                                y=dfdrop2.UnidadesProcessadas.tolist(),
                                name='Processado',
                                )

            traceff = go.Bar(x=dfdrop2.HoraDrop.tolist(), 
                                y=dfdrop2['Unidades Pendentes'].tolist(),
                                name='Pendente',
                               )



            datafd = (tracefd, tracefd2, traceff)

            layoutfd=  go.Layout(xaxis={'title': 'Hora'},
                                yaxis={'title': 'Unidades Produzidas'},
                                margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                hovermode='closest',
                                template='plotly_white',
                                barmode='stack')

            figurefd = go.Figure(data=datafd, layout=layoutfd)
            
            #UPPH
            dfupphcanal = dfupphcanal.drop(dfupphcanal[dfupphcanal.Hora == 0].index)
            groups52 = dfupphcanal.groupby(by='OrderType')


            data52 = []
            colors52=get_colors(50)

            for group52, dataframe52 in groups52:
                dataframe52 = dataframe52.sort_values(by=['Hora'])
                trace52 = go.Scatter(x=dataframe52.Hora.tolist(), 
                                    y=dataframe52.UPPH.tolist(),
                                    marker=dict(color=colors52[len(data52)]),
                                    name=group52,
                                   )


                data52.append(trace52)

                layout52 =  go.Layout(xaxis={'title': 'Hora'},
                                    yaxis={'title': 'Unidades Produzidas'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest',
                                    template='plotly_white',
                                    title={
                                            'text': "Unidades Produzidas Por Pessoas / Hora",
                                            'y':.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'})

            figure52 = go.Figure(data=data52, layout=layout52)
            tabelaupph = dfupphcanal.drop(['Unidades Pendentes','Qty','Order No', 'Time Proc Seg', 'MM_10', 'MM_20', 'MM_30', 'UPH', 'Hora' ], axis=1)
            tabelaupph2 = tabelaupph.groupby('OrderType').sum().round(2)
            tabelaupph2.reset_index(inplace=True)
            
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5('Nome Do Arquivo:'+filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Conteudo Bruto: '),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        }),
        

html.Div([
   html.H2(children = "Tabela De Desempenho Por Canal",
    style = {'textAlign' : 'center',}),
]),    
html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfordertype.columns],
         data=dfordertype.to_dict('records'),
        style_table={'textAlign': 'center'},
         style_as_list_view=True,
        style_cell={'padding': '5px','fontSize': 12, 'textAlign': 'center'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'fontSize': 12},


    ),

        ],style={'textAlign': 'center',
                 'align-items': 'center',
                 'fontSize': 12,
                 'width': '100%',
                 'display': 'flex',
                 'align-items': 'center',
                 'justify-content': 'center'}),       
        

html.Div([ 
html.Div([
   html.H3(children = "Produção Por Hora (Canal)",
    style = {'textAlign' : 'center',}),
], style={'marginBottom': 50, 'marginTop': 25}),


dcc.Graph(
        id = 'GrapGo',
        figure = figure2),
    
html.Div([
   html.H3(children = "Produção Por Hora (Estação)",
    style = {'textAlign' : 'center',}),    

], style={'marginBottom': 50, 'marginTop': 25}),
    
dcc.Graph(
    id = 'GrapGo2',
    figure = figure3),

html.Div([
   html.H3(children = "Produção Por Hora (Operador)",
    style = {'textAlign' : 'center',}),    

], style={'marginBottom': 50, 'marginTop': 25}),    
    
dcc.Graph(
    id = 'GrapGo3',
    figure = figure4), 
 
    
    
html.Div([
   html.H3(children = "Média Moveis (10, 20 e 30 periodos)",
    style = {'textAlign' : 'center',}),    

], style={'marginBottom': 50, 'marginTop': 25}), 
    
dcc.Graph(
    id = 'GrapGo4',
    figure = figuremm),

    
html.Div([
   html.H3(children = "Médias Móveis - 10 Intervalos por canal",
    style = {'textAlign' : 'center',}),    

], style={'marginBottom': 50, 'marginTop': 25}),
    
dcc.Graph(
    id = 'GrapGo4',
    figure = figure7),

    
html.Div([
    html.P(""),
    html.H3(children = "Unidades Recebidas Vs Processadas por Hora",
    style = {'textAlign' : 'center',}),    

], style={'marginBottom': 50, 'marginTop': 25}),

    dcc.Graph(
    id = 'GrapGo4',
    figure = figurefd),

    #Tabela UPPH
    
        html.Div([
           html.H2(children = "Tabela De Desempenho Por Pessoa / Hora",
            style = {'textAlign' : 'center',}),
        ]),    
        html.Div([
            dash_table.DataTable(
                id='tableUPPH',
                columns=[{"name": i, "id": i} for i in tabelaupph2.columns],
                 data=tabelaupph2.to_dict('records'),
                style_table={'textAlign': 'center'},
                 style_as_list_view=True,
                style_cell={'padding': '5px','fontSize': 12},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'fontSize': 12},


            ),

                ],style={'textAlign': 'center',
                         'align-items': 'center',
                         'fontSize': 12,
                         'width': '100%',
                         'display': 'flex',
                         'align-items': 'center',
                         'justify-content': 'center'}),       




], style={'marginBottom': 50, 'marginTop': 25}),

    dcc.Graph(
    id = 'GrapGo4',
    figure = figure52),

], style={'marginLeft': 50, 'marginRight': 50})





@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server()
