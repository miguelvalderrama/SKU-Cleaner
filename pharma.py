import pandas as pd
from drogs import *

#DROGS = ['dismeven', 'drolanca', 'italclinic', 'cobeca']

def Merge_Drogs(method=False, dismeven_d=False, drolanca_d=False, italclinic_d=False, cobeca_d=False):
    #Input tasa de cambio
    tasa = 5.1
    #Input credits days for each drog
    #for i in range(len(DROGS)):
    
    #Call dismeven
    dismeven(14)
    #Call drolanca
    drolanca(7)
    #Call vitalclinic
    vitalclinic(tasa, 21)
    #Call cobeca
    cobeca()

    #Read the files
    df1 = pd.read_csv('csv\drolanca.csv')
    df2 = pd.read_csv('csv\dismeven.csv')
    df3 = pd.read_csv('csv\italclinic.csv')
    df4 = pd.read_csv('csv\cobeca.csv')
   
    #Concatenate the dataframes and sort by cod. bar
    df = pd.concat([df1, df2, df3, df4])
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
    '''
    #Add cod. bar from df less than 1000
    for index, row in df.iterrows():
        if row['Cod. Bar'] < 1000:
            dfd.loc[index, 'Cod. Bar'] = row['Cod. Bar']
            dfd.loc[index, 'Product'] = row['Product']
            dfd.loc[index, 'F.Price'] = row['F.Price']
            dfd.loc[index, 'Qty'] = row['Qty']
            dfd.loc[index, 'Drog'] = row['Drog']
    '''
    #Save the dataframe
    dfd.sort_values(by=['Cod. Bar'], inplace=True)  #Sort by cod. bar
    dfd.to_csv('final.csv', index=False)
    
    print('Done')

def Unmerge_Drogs():

    #Read the file
    df = pd.read_csv('final.csv')

    #Read the files
    df1 = pd.read_excel('raw_data\dismeven.xlsx')
    df2 = pd.read_excel('raw_data\drolanca.xlsx')
    df3 = pd.read_excel('raw_data\Vitalclinic.xlsx')
    df4 = pd.read_excel('raw_data\cobeca.xlsx', sheet_name='MEDICINAS')
    
    #If qty is over 0, add it to the correct drog
    for index, row in df.iterrows():
        if row['Qty'] > 0:
            if row['Cod. Bar'] > 1000:
                if row['Drog'] == 'dismeven':
                    df1.loc[index, 'Cod. Bar'] = row['Cod. Bar']
                    df1.loc[index, 'Product'] = row['Product']
                elif row['Drog'] == 'drolanca':
                    df2.loc[index, 'Qty'] = row['Qty']
                elif row['Drog'] == 'italclinic':
                    df3.loc[index, 'Qty'] = row['Qty']
                elif row['Drog'] == 'cobeca':
                    df4.loc[index, 'Qty'] = row['Qty']

    #Save the files
    df1.to_csv('process_data\dismeven.csv', index=False)
    df2.to_csv('process_data\drolanca.csv', index=False)
    df3.to_csv('process_data\italclinic.csv', index=False)
    df4.to_csv('process_data\cobeca.csv', index=False)




Unmerge_Drogs()