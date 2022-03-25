import pandas as pd
import plistlib
import pandas_read_xml as pdx


def out_color_text(text, color):
    match color:
        case 'red':
            return f"\033[31m{text}\033[0m"
        case 'yellow':
            return f"\033[33m{text}\033[0m"
        case 'green':
            return f"\033[32m{text}\033[0m"
        case _:
            return text


def get_data_file(file_name):
    data = None
    if '.xlsx' in file_name:
        excel_data = pd.read_excel('DominiGames Test  Sheet.xlsx')
        df = pd.DataFrame(excel_data)
        return df
    elif '.plist' in file_name:
        with open(file_name, 'rb') as f:
            plist_data = plistlib.load(f)
            df = pd.DataFrame(plist_data)
            return df
    elif '.xml' in file_name:
        df = pdx.read_xml(file_name, ['config', 'shop_items', 'item']).T
        df['data'] = df
        data_normilized = pd.json_normalize(df.data)
        return data_normilized


data_instance_xlsx = get_data_file('DominiGames Test  Sheet.xlsx')
data_plist = get_data_file('Info.plist')
data_xml = get_data_file('DominiIAP.xml')

instance_for_xml = data_instance_xlsx.purchase.dropna()
check_value_xml = data_xml.ProductID.dropna()

instance_for_plist = data_instance_xlsx.plist_UniversalF2P.dropna()
check_value_plist = [key for key in data_plist]


def validate_key(check_value, instance):
    print('Validation...')
    for elem in check_value:
        if elem in list(instance):
            print(out_color_text(f'{elem} - key is correct', 'green'))
        else:
            hint = [el for el in list(instance) if el[0] == elem[0]]
            if hint:
                print(out_color_text(f'{elem} - key is incorrect, maybe you mean {hint}', 'yellow'))
            else:
                print(out_color_text(f'{elem} - key is incorrect, key not recognized', 'red'))
    print('Validation completed.')
                
validate_key(check_value_plist, instance_for_plist)  # validation plist
print()
validate_key(check_value_xml, instance_for_xml)  # validation xml
