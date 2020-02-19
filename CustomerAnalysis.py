
import pandas as pd



df = pd.read_csv('enq2.csv', encoding='latin-1')
df_cus = pd.read_csv('customers.csv', encoding='latin-1')
df_cus.rename(columns={df_cus.columns[0]:'Destination'}, inplace=True)
df.rename(columns={df.columns[39]:'PGID'}, inplace=True)
df.rename(columns={df.columns[35]:'NF Received'}, inplace=True)



df1 = df

df1.loc[(df1.PGID != '?'), 'UnidadesProcessadas'] = df1['Qty']
df1.loc[(df1.PGID == '?'), 'UnidadesProcessadas'] = 0

df1['UnidadesPendentes'] = df1['Qty'] - df1['UnidadesProcessadas'] 

df1["Destination"] = [(lambda x: x.strip('0') if isinstance(x,str) and len(x) != 1 else x)(x) for x in df1["Destination"]]

df1 = pd.merge(df1, df_cus[['Destination','Name 1']], on='Destination', how='right')

df1.rename(columns={"Name 1": "Customer"}, inplace=True)

df2 = df1.groupby(['Customer','Order No']).sum()
df2.reset_index(inplace=True)
df2 = df2.groupby('Customer').sum()
df2.reset_index(inplace=True)

dfqtyorders = df1.groupby(['Customer', 'Order No']).count()
dfqtyorders.reset_index(inplace=True)
dfqtyorders = dfqtyorders.groupby('Customer').count()
dfqtyorders.reset_index(inplace=True)

dfqtyorders.rename(columns={"Order No": "Qty_Ordens"}, inplace=True)

dftotalcustomer = df2[['Customer', 'Qty', 'UnidadesProcessadas', 'UnidadesPendentes']]

dftotalcustomer = pd.merge(dftotalcustomer, dfqtyorders[['Customer','Qty_Ordens']], on='Customer', how='right')

dftotalcustomer['Perfil DN'] = (dftotalcustomer['Qty'] / dftotalcustomer['Qty_Ordens']).round(2)

dftotalcustomer_cutt = df1.groupby(['Customer', 'Cut Off Date']).sum()
dftotalcustomer_cutt.reset_index(inplace=True)

dftotalcustomer_cutt = dftotalcustomer_cutt[['Customer', 'Cut Off Date', 'Qty','UnidadesProcessadas', 'UnidadesPendentes']]



dftotalcustomer_cutt2 = df1.groupby(['Customer','Cut Off Date', 'Order No']).sum()
dftotalcustomer_cutt2.reset_index(inplace=True)
dftotalcustomer_cutt2 = dftotalcustomer_cutt2.groupby(['Customer', 'Cut Off Date']).count()
dftotalcustomer_cutt2.reset_index(inplace=True)
dftotalcustomer_cutt2 = dftotalcustomer_cutt2.groupby(['Customer', 'Cut Off Date']).sum()
dftotalcustomer_cutt2.reset_index(inplace=True)

dftotalcustomer_cutt2 = dftotalcustomer_cutt2[['Customer','Cut Off Date','Order No']]


dftotalcustomer_cutt['Qty_Ordens'] = dftotalcustomer_cutt2['Order No']
dftotalcustomer_cutt['Perfil'] = (dftotalcustomer_cutt['Qty'] / dftotalcustomer_cutt['Qty_Ordens']).round(2)


dfdetail = df1[['Order No', 'Order Type', 'Destination', 'Customer', 'Cut Off Date', 'Received', 'Processed', 'PGID', 'NF Received', 'Qty', 'Pick No', 'Status']]

