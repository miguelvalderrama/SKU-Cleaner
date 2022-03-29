import pandas as pd
import datetime


DROGS = ['Drolanca', 'Dismeven', 'Vitalclinic']


def dismeven(days):
    try:
        df = pd.read_csv('Dismeven.csv', usecols=['Unnamed: 1','Unnamed: 2', 'Unnamed: 3', 'Unnamed: 9'])
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
        df.to_csv('modified.csv', index=False)
    except:
        return False
    return True

def drolanca(days):
    try:
        df = pd.read_excel('Drolanca.xlsx' , usecols=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 6', 'Unnamed: 10', 'Unnamed: 11'])
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
        df.to_csv('drolanca.csv', index=False)
    except:
        return False
    return True

def vitalclinic(tasa, days):
    try:
        df = pd.read_excel('Vitalclinic.xlsx', usecols=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 6', 'Unnamed: 9'])
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
        df.to_csv('vitalclinic.csv', index=False)
    except:
        return False
    return True

def Merge_Drogs(method=False):
    tasa = float(input('Ingrese la tasa de cambio: '))

    #Input credits days for each drog
    #days = int(input('Ingrese los dias de credito: '))
    
    #Call dismeven
    if not dismeven(14):
        print('Dismeven failed')
    #Call drolanca
    if not drolanca(7):
        print('Drolanca failed')
    #Call vitalclinic
    if not vitalclinic(tasa, 21):
        print('Vitalclinic failed')

    #Read the files
    df1 = pd.read_csv('drolanca.csv')
    df2 = pd.read_csv('modified.csv')
    df3 = pd.read_csv('vitalclinic.csv')
   
    #Concatenate the dataframes and sort by cod. bar
    df = pd.concat([df1, df2, df3])
    df = df.sort_values(by=['Cod. Bar'])
    
    #Dictionary with cod. bar as key
    dic = {}

    #Selected price
    if method == 'price':
        for index, row in df.iterrows():
            if row['Cod. Bar'] > 1000:
                #if the cod. bar is not in the dictionary, add it
                if row['Cod. Bar'] not in dic:
                    dic[row['Cod. Bar']] = {
                        'Product': row['Product'],
                        'F.Price': row['F.Price'],
                        'Qty': row['Qty'],
                        'Drog': row['Drog'],
                        'Date': row['Date']
                    }
                #if the cod. bar is in the dictionary and the price is lower, update the price
                elif row['F.Price'] < dic[row['Cod. Bar']]['F.Price']:
                    dic[row['Cod. Bar']]['F.Price'] = row['F.Price']
                    dic[row['Cod. Bar']]['Drog'] = row['Drog']
                    dic[row['Cod. Bar']]['Date'] = row['Date']
    elif method == 'credit':
        for index, row in df.iterrows():
            if row['Cod. Bar'] > 1000:
                #if the cod. bar is not in the dictionary, add it
                if row['Cod. Bar'] not in dic:
                    dic[row['Cod. Bar']] = {
                        'Product': row['Product'],
                        'F.Price': row['F.Price'],
                        'Qty': row['Qty'],
                        'Drog': row['Drog'],
                        'Date': row['Date']
                    }
                #if the cod. bar is in the dictionary and the date is older, update the date
                elif row['Date'] > dic[row['Cod. Bar']]['Date']:
                    dic[row['Cod. Bar']]['F.Price'] = row['F.Price']
                    dic[row['Cod. Bar']]['Drog'] = row['Drog']
                    dic[row['Cod. Bar']]['Date'] = row['Date']
                
                elif row['Date'] == dic[row['Cod. Bar']]['Date']:
                    #Check the price
                    if row['F.Price'] < dic[row['Cod. Bar']]['F.Price']:
                        dic[row['Cod. Bar']]['F.Price'] = row['F.Price']
                        dic[row['Cod. Bar']]['Drog'] = row['Drog']
                        dic[row['Cod. Bar']]['Date'] = row['Date']
                    
    #Create a new dataframe with the correct format
    dfd = pd.DataFrame.from_dict(dic, orient='index')
    dfd = dfd.reset_index()
    dfd.rename(columns={'index': 'Cod. Bar'}, inplace=True)

    #Add cod. bar from df less than 1000
    for index, row in df.iterrows():
        if row['Cod. Bar'] < 1000:
            dfd.loc[index, 'Cod. Bar'] = row['Cod. Bar']
            dfd.loc[index, 'Product'] = row['Product']
            dfd.loc[index, 'F.Price'] = row['F.Price']
            dfd.loc[index, 'Qty'] = row['Qty']
            dfd.loc[index, 'Drog'] = row['Drog']

    #Save the dataframe
    dfd.sort_values(by=['Cod. Bar'], inplace=True)  #Sort by cod. bar
    dfd.to_csv('final.csv', index=False)
    
    print('Done')

def Unmerge_Drogs():

    #Read the file
    df = pd.read_csv('final.csv')

