import pandas as pd
import datetime


def dismeven(days):
    try:
        df = pd.read_excel('raw_data\Dismeven.xlsx', usecols=['Unnamed: 1','Unnamed: 2', 'Unnamed: 3', 'Unnamed: 9'])
        df = df.iloc[9:]
        names = {
            'Unnamed: 1': 'Qty',
            'Unnamed: 2': 'Product',
            'Unnamed: 3': 'F.Price',
            'Unnamed: 9': 'Cod. Bar'
            }
        df.rename(columns=names, inplace=True)
        mf = df['Product'].dropna()
        df = df.iloc[:len(mf)]
        #Fix the cod. bar
        df['Cod. Bar'] = df['Cod. Bar'].replace('NO APLICA', 0)
        df['Cod. Bar'] = df['Cod. Bar'].fillna(0)
        #Fix F.price
        df['F.Price'] = df['F.Price'].astype(float)
        #Get today's date and sum the days of credit
        today = datetime.datetime.today() + datetime.timedelta(days=days)
        df['Date'] = today.strftime('%d/%m/%Y')
        #Add the drog name
        df['Drog'] = 'Dismeven'
        #Save the dataframe
        df.to_csv('csv\dismeven.csv', index=False)
    except:
        raise Exception('Error en Dismeven')

def drolanca(days):
    try:
        df = pd.read_excel('raw_data\Drolanca.xlsx' , usecols=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 6', 'Unnamed: 10', 'Unnamed: 11'])
        df = df.iloc[6:]
        names = {
            'Unnamed: 1': 'Cod. Bar',
            'Unnamed: 2': 'Product',
            'Unnamed: 6': 'Bs',
            'Unnamed: 10': 'F.Price',
            'Unnamed: 11': 'Qty',
            }
        df.rename(columns=names, inplace=True)
        #Check promo price
        df['F.Price'] = df['F.Price'].fillna(df['Bs'])
        #Fix the cod. bar
        df['Cod. Bar'] = df['Cod. Bar'].fillna(0)
        #Drop the Bs column
        df.drop(['Bs'], axis=1, inplace=True)
        #Get today's date and sum the days of credit
        today = datetime.datetime.today() + datetime.timedelta(days=days)
        df['Date'] = today.strftime('%d/%m/%Y')
        #Add the drog name
        df['Drog'] = 'Drolanca'
        #Save the dataframe
        df.to_csv('csv\drolanca.csv', index=False)
    except:
        raise Exception('Error en Drolanca')

def vitalclinic(tasa, days):
    try:
        df = pd.read_excel('raw_data\Vitalclinic.xlsx', usecols=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 6', 'Unnamed: 9'])
        df = df.iloc[10:]
        names = {
            'Unnamed: 1': 'Cod. Bar',
            'Unnamed: 3': 'Product',
            'Unnamed: 6': '$',
            'Unnamed: 9': 'Qty',
            }
        df.rename(columns=names, inplace=True)
        mf = df['Product'].dropna()
        df = df.iloc[:len(mf)]
        df['F.Price'] = df['$'] * float(tasa)
        df.drop(['$'], axis=1, inplace=True)
        #Fix the cod. bar
        df['Cod. Bar'] = df['Cod. Bar'].replace(to_replace='[^0-9]', value='', regex=True)
        df['Cod. Bar'] = df['Cod. Bar'].fillna(0)
        #Fix F.price
        df['F.Price'] = df['F.Price'].astype(float)
        #Get today's date and sum the days of credit
        today = datetime.datetime.today() + datetime.timedelta(days=days)
        df['Date'] = today.strftime('%d/%m/%Y')
        #Add the drog name
        df['Drog'] = 'Vitalclinic'
        #Save the dataframe
        df.to_csv('csv\italclinic.csv', index=False)
    except:
        raise Exception('Error en Vitalclinic')

def cobeca():
    try:
        df = pd.read_excel('raw_data\Cobeca.xlsx', sheet_name='MEDICINAS', usecols=['Unnamed: 1', 'Unnamed: 5', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'])
        df = df.iloc[8:]
        names = {
            'Unnamed: 1': 'Product',
            'Unnamed: 5': 'Cod. Bar',
            'Unnamed: 11': 'F.Price',
            'Unnamed: 12': 'Date',
            'Unnamed: 13': 'Qty',
            }
        df.rename(columns=names, inplace=True)
        #Eliminate the F.Price with NaN values
        df = df[df['F.Price'].notnull()]
        #Get today's date and sum the values of Date for each product
        today = datetime.datetime.today()
        df['Date'] = df['Date'].astype(int)
        df['Date'] = df['Date'].apply(lambda x: today + datetime.timedelta(days=x)).dt.strftime('%d/%m/%Y')
        #Add the drog name
        df['Drog'] = 'Cobeca'
        #Save the dataframe
        df.to_csv('csv\cobeca.csv', index=False)
    except:
        raise Exception('Error en Cobeca')
