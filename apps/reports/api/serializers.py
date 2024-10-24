import requests
import pandas as pd
import os
import unicodedata

class ReportPUC():
    
    def puc_function(self, data):
        try:
            if not data.get('status'):
                return {'message': data.get('error')}, False

            file_url = data.get('data', {}).get('file_url')
            if not file_url:
                return {'message': 'URL del archivo no disponible'}, False

            file_response = requests.get(file_url)
            if file_response.status_code != 200:
                return {'message': 'Error al descargar el archivo'}, False
            
            temp_file_path = 'temp_file.xlsx'
            with open(temp_file_path, 'wb') as f:
                f.write(file_response.content)
            
            
            df = pd.read_excel('temp_file.xlsx', engine='openpyxl', header=4) 
            
            filtered_df  = df.iloc[:-2] 
            selected_df  = filtered_df [['Transaccional', 'Código cuenta contable', 'Nombre Cuenta contable']]
            selected_df  = selected_df .applymap(lambda x: x.strip() if isinstance(x, str) else x)
            
            code = ""
            accountingAccount = ""
            type_list = []
            subtype_list = []
            subtype_two_list = []
            subtype_three_list = []
            puc_list = []

            type_dictionary = {}
            subtype_dictionary = {}
            subtype_two_dictionary = {}
            subtype_three_dictionary = {}
            puc_dictionary = {}
            puc_more_dictionary = {}
            
            for index, row in selected_df .iterrows():
                
                if self.contains_dig(row['Código cuenta contable']) == 1:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code)
                    accountingAccount = row['Nombre Cuenta contable']
                    type_list.append(accountingAccount)
                    type_dictionary[code] = accountingAccount
                    
                if self.contains_dig(row['Código cuenta contable']) == 2:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code)
                    accountingAccount = row['Nombre Cuenta contable']
                    subtype_list.append(accountingAccount)
                    subtype_dictionary[code] = accountingAccount
                    
                if self.contains_dig(row['Código cuenta contable']) == 4:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code)
                    accountingAccount = row['Nombre Cuenta contable']
                    subtype_two_list.append(accountingAccount)
                    subtype_two_dictionary[code] = accountingAccount
                    
                if self.contains_dig(row['Código cuenta contable']) == 6:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code) 
                    accountingAccount = row['Nombre Cuenta contable']
                    subtype_three_list.append(accountingAccount)
                    subtype_three_dictionary[code] = accountingAccount
                    
                if self.contains_dig(row['Código cuenta contable']) == 8:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code)
                    accountingAccount = row['Nombre Cuenta contable']
                    puc_list.append(accountingAccount)
                    puc_dictionary[code] = accountingAccount    
                    
                if self.contains_dig(row['Código cuenta contable']) == 10:
                    code = row['Código cuenta contable'] 
                    code = int(code)
                    code = str(code)
                    accountingAccount = row['Nombre Cuenta contable']
                    puc_list.append(accountingAccount)
                    puc_more_dictionary[code] = accountingAccount    
                    
            data_list = []
            
            for code_five, valor_cinco in puc_dictionary.items():
                code_four = code_five[:6]
                code_three = code_five[:4]
                code_two = code_five[:2]
                code_puc = code_five[:1]    
                 
                if (code_four in subtype_three_dictionary and 
                    code_three in subtype_two_dictionary and 
                    code_two in subtype_dictionary and 
                    code_puc in type_dictionary):
                    
                    value_four = subtype_three_dictionary[code_four]
                    value_three = subtype_two_dictionary[code_three]
                    value_two = subtype_dictionary[code_two]
                    value = type_dictionary[code_puc]
                    
                    datae = {
                        'Codigo': code_five,
                        'Cuenta Contable': valor_cinco,
                        'Clase': value,
                        'Grupo': value_two,
                        'Tipo': value_three,
                        'Subtipo': value_four
                    }
                    
                    data_list.append(datae)

            dataframe_final = pd.DataFrame(data_list)                    
          
            data_list = dataframe_final.to_dict(orient='records')
            data = {"data": data_list}
            os.remove('temp_file.xlsx')
            
            return data, True
        
        except Exception as e:
            return {'message': str(e)}, False
        
    @staticmethod
    def contains_dig(number):
        return len(str(abs(int(number))))


    def Data(self, Code='n/a', AccountingAccount='n/a', Type='n/a', Subtype='n/a', SubtypeTwo='n/a', SubtypeThree='n/a'):
        self.Code = Code
        self.AccountingAccount = AccountingAccount
        self.Type = Type
        self.Subtype = Subtype
        self.SubtypeTwo = SubtypeTwo
        self.SubtypeThree = SubtypeThree
        return self
    
    @staticmethod
    def contains(cadena, subcadena): 
        return subcadena in cadena
    
    
class Balance():
    
    def balance_function_terceros(self,data):
        
        try:
            if not data.get('status'):
                return {'message': data.get('error')}, False

            file_url = data.get('data', {}).get('file_url')
            if not file_url:
                return {'message': 'URL del archivo no disponible'}, False

            file_response = requests.get(file_url)
            if file_response.status_code != 200:
                return {'message': 'Error al descargar el archivo'}, False
            
            temp_file_path = 'temp_file.xlsx'
            with open(temp_file_path, 'wb') as f:
                f.write(file_response.content)
            
            df = pd.read_excel('temp_file.xlsx', engine='openpyxl', header=4)
            df.columns = df.columns.str.replace(' ', '_')
            
            if 'Sucursal' in df.columns:
                df = df.drop(columns=['Sucursal'])
            df_filtered = df[df["Transaccional"] == "Sí"]
            df_filtered = df_filtered.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df_filtered = df_filtered.where(pd.notnull(df_filtered), None)
            data_list = df_filtered.to_dict(orient='records')
            data = {"data": data_list}
            os.remove('temp_file.xlsx')
            
            return data, True   
        
        except Exception as e:
            return {'message': str(e)}, False
        
    def balance_function_general(self,data):
        
        try:
            if not data.get('status'):
                return {'message': data.get('error')}, False

            file_url = data.get('data', {}).get('file_url')
            if not file_url:
                return {'message': 'URL del archivo no disponible'}, False

            file_response = requests.get(file_url)
            if file_response.status_code != 200:
                return {'message': 'Error al descargar el archivo'}, False
            
            temp_file_path = 'temp_file.xlsx'
            with open(temp_file_path, 'wb') as f:
                f.write(file_response.content)
            
            df = pd.read_excel('temp_file.xlsx', engine='openpyxl', header=4)
            df = df.iloc[:-2]
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = [''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn') for col in df.columns] 
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.where(pd.notnull(df), None)
            data_list = df.to_dict(orient='records')
            data = {"data": data_list}
            os.remove('temp_file.xlsx')
            
            return data, True   
        
        except Exception as e:
            return {'message': str(e)}, False
        

    
   