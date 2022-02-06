import sys
import json
import pandas as pd
import numpy as np
import difflib

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

    
    if 'test' in targets:
        tx = pd.read_csv('tx_50.csv')
        tx = tx[tx['vehicle_make'].notna()]
        tx['make_model'] = tx['vehicle_year'].astype(str) + ' ' + tx['vehicle_make'].astype(str) + ' ' + tx['vehicle_model'].astype(str)
        tx['age'] = (tx['vehicle_year'] - 2022) *-1
        tx = tx[tx['age']>= 0] 
        tx = tx[tx['age'] <=30]
        
        kbb = pd.read_csv('https://raw.githubusercontent.com/Tai-Pach/kbb/gh-pages/KBB_used_final_3.csv')
        
        cars_join = pd.DataFrame()
        cars_join['car'] = kbb['year'].astype(str) + ' ' +  kbb['make_model']
        cars_join['price'] = kbb['price']
        
        def shorten(car):
            l = car.split()
            l[1] = l[1][:3]
            l[2] = l[2][:3]
            return ' '.join(l[:3])
        cars_join['car'] = cars_join['car'].astype(str).apply(shorten)
        cars_join = cars_join.set_index('car')
        
        tx_kbb = {'KIA':'Kia', 'VOLK': 'Volkswagen', 'CADI':'Cadillac','CHEV':'Chevorlet', 'MAZD': 'Mazda', 'FIAT':'FIAT',
                  'HYUN':'Hyundai', 'PONT':'Pontiac', 'GMC':'GMC', 'NISS':'Nissan', 'TOY':'Toyota', 'HOND':'Honda',
                  'JEEP':'Jeep', 'FORD':'Ford', 'HUMM':'HUMMER', 'MINI':'MINI','LINC':'Lincoln', 'SUBA':'Subaru',
                  'JAG':'Jaguar', 'MERZ':'Mercedes-Benz', 'ISUZ':'Isuzu', 'MITS':'Mitsubishi', 'DODG':'Dodge',
                  'ACUR':'Acura', 'CHRY':'Chrysler', 'BMW':'BMW', 'MERC':'Mercury', 'SATU':'Saturn', 'OLDS':'Oldsmobile',
                  'BUIC':'Buick', 'LEXU':'Lexus', 'AUDI':'Audi', 'VOLV':'Volvo', 'INFI':'INFINITI', 'SCIO':'Scion',
                  'PORS': 'Porsche', 'PLYM':'Plymouth', 'RAM':'RAM', 'SAAB':'Saab', 'BENT':'Bentley', 'TESL':'Tesla',
                  'SUZU':'Suzuki', 'GEO':'Geo', 'FERR':'Ferrari'}
        make_model_price = dict({})
        
        for i in cars_join.index.to_list():
            matches = difflib.get_close_matches(i, tx['make_model'].unique())
            if len(matches) > 0:
                make_model = difflib.get_close_matches(i, tx['make_model'].unique())[0]
                make_model_price[make_model] = cars_join.loc[i]['price'].mean()
        
        make_model_price_df = pd.DataFrame.from_dict(make_model_price, orient='index')
        make_model_price_df = make_model_price_df.reset_index()
        make_model_price_df.columns = ['make_model', 'price']
        make_model_price_df['make_model']= make_model_price_df['make_model'].astype(str)
        
        tx['make_model'] = tx['make_model'].astype(str)
        tx = tx.merge(make_model_price_df, on='make_model')
        
        tx.to_csv('test.csv')
    
    return


if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)