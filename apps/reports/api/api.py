import json
import os
import requests
import warnings
import pandas as pd
from collections import defaultdict
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.reports.auth_siigo.auth import execute_request
from apps.reports.api.serializers import ReportPUC, Balance
from accounting_success.mixins import UserRoleMixin
from datetime import datetime
from calendar import monthrange

warnings.filterwarnings("ignore")
year = datetime.now().year

# 1.PUC (plan único de cuentas) y Balance general
class ReportPUCDuo(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report', values=payload_json, type='post', request=request)
                       
            report_puc = ReportPUC()
            data, success = report_puc.puc_function(response)
            
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(1) # 1.PUC (plan único de cuentas).
            
            
            if  permission:
                if success:
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class Balance_general(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report', values=payload_json, type='post', request=request)
            
            report_third = Balance()
            data, success = report_third.balance_function_general(response)
            
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(1) # 1. PUC Y BALANCE GENERAL
             
            if permission:
                if success:
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Balance_general_excel(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report', values=payload_json, type='post', request=request)
        
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(1) # 1. PUC Y BALANCE GENERAL
            
            if  permission:
                if response['status'] == False:
                    return Response({'message': response['error']}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(response['data'], status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
# 2.Movimiento contable por terceros.    
class Third_parties(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report-by-thirdparty', values=payload_json, type='post', request=request)
        
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(2) # 2.Movimiento contable por terceros.
            
            if  permission:
                if response['status'] == False:
                    return Response({'message': response['error']}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(response['data'], status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 # 2.Movimiento contable por terceros.    
class ThirdsDuo(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report-by-thirdparty', values=payload_json, type='post', request=request)
            
            report_third = Balance()
            data, success = report_third.balance_function_terceros(response)
            
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(2) # 2.Movimiento contable por terceros.
             
            if permission:
                if success:
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 3. Reporte de ventas por cliente por producto. 
class SalesPerProduct(APIView):
    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page_size=100'
            all_sales = []
            page = 1
            while sales_url:
                response_sales = execute_request(sales_url, values={}, type='get', request=request)
                if not response_sales['status']:
                    return Response({'message': 'Error en la obtención de ventas'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_sales.extend(response_sales['data']['results'])
                
                total_results = response_sales['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page={page}&page_size={page_size}'
                else:
                    sales_url = None

            customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
            all_customers = []
            page = 1
            while customers_url:
                response_customers = execute_request(customers_url, values={}, type='get', request=request)
                if not response_customers['status']:
                    return Response({'message': 'Error en la obtención de clientes'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_customers.extend(response_customers['data']['results'])

                total_results = response_customers['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
                else:
                    customers_url = None

            product_url = 'https://api.siigo.com/v1/products?page_size=100'
            all_products = []
            page = 1
            while product_url:
                response_product = execute_request(product_url, values={}, type='get', request=request)
                if not response_product['status']:
                    return Response({'message': 'Error en la obtención de productos'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_products.extend(response_product['data']['results'])

                total_results = response_product['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    product_url = f'https://api.siigo.com/v1/products?page={page}&page_size={page_size}'
                else:
                    product_url = None

            customer_dict = {customer['identification']: customer['name'] for customer in all_customers}
            product_dict = {product['code']: product['name'] for product in all_products}
            grupo_dict = {grupo['code']: grupo['account_group']['name'] for grupo in all_products}
            
            sales_data = []
            for sale in all_sales:
                for item in sale['items']:
                    customer_id = sale['customer']['identification']
                    fecha_venta = sale['date']
                    customer_name = customer_dict.get(customer_id, 'Desconocido')
                    quantity = item['quantity']
                    product_code = item['code']
                    product_name = product_dict.get(product_code, 'Desconocido')
                    grupo_code = grupo_dict.get(product_code, 'Desconocido')
                    product_total = item['total']

                    retention_tax = product_total * 0.11
                    cargo_tax = product_total * 0.19
                    total_tax = retention_tax + cargo_tax

                    sales_data.append({
                        'id_cliente': customer_id,
                        'nombre_cliente': customer_name,
                        'codigo_producto': product_code,
                        'nombre_producto': product_name,
                        'grupo_inventario': grupo_code,
                        'cantidad_vendida': quantity,
                        'fecha_venta': fecha_venta,
                        'subtotal': product_total - total_tax,
                        'impuesto_retencion': retention_tax,
                        'impuesto_cargo': cargo_tax,
                        'total': product_total,
                    })

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(3) # 3. Ventas.
             
            if permission:
                return Response(sales_data, status=status.HTTP_200_OK)
            else:
                return Response(sales_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SalesPerCustomer(APIView):
    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

            sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page_size=100'
            all_sales = []
            page = 1
            while sales_url:
                response_sales = execute_request(sales_url, values={}, type='get', request=request)
                if not response_sales['status']:
                    return Response({'message': 'Error en la obtención de ventas'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_sales.extend(response_sales['data']['results'])
                total_results = response_sales['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page={page}&page_size={page_size}'
                else:
                    sales_url = None

            customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
            all_customers = []
            page = 1
            while customers_url:
                response_customers = execute_request(customers_url, values={}, type='get', request=request)
                if not response_customers['status']:
                    return Response({'message': 'Error en la obtención de clientes'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_customers.extend(response_customers['data']['results'])
                total_results = response_customers['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
                else:
                    customers_url = None

            customer_dict = {customer['identification']: customer['name'] for customer in all_customers}

            sales_by_customer = {}
            for sale in all_sales:
                customer_id = sale['customer']['identification']
                customer_name = customer_dict.get(customer_id, 'Desconocido')
                sale_total = sale['total']
                
                retention_tax = sale_total * 0.11
                cargo_tax = sale_total * 0.19
                total_tax = retention_tax + cargo_tax
                net_total = sale_total - total_tax

                if customer_id not in sales_by_customer:
                    sales_by_customer[customer_id] = {
                        'id_cliente': customer_id,
                        'nombre_cliente': customer_name,
                        'subtotal': net_total,
                        'impuesto_retencion': retention_tax,
                        'impuesto_cargo': cargo_tax,
                        'total': sale_total
                    }

            sales_data = list(sales_by_customer.values())

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(3) # 3. Ventas.
             
            if permission:
                return Response(sales_data, status=status.HTTP_200_OK)
            else:
                return Response(sales_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SalesDuo(APIView):
    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

            url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}'
            response_sales = execute_request(url, values={}, type='get', request=request)

            if not response_sales['status']:
                return Response({'message': 'Error al obtener las ventas.'}, status=status.HTTP_400_BAD_REQUEST)

            customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
            all_customers = []
            page = 1
            while customers_url:
                response_customers = execute_request(customers_url, values={}, type='get', request=request)
                if not response_customers['status']:
                    return Response({'message': 'Error al obtener clientes.'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_customers.extend(response_customers['data']['results'])

                total_results = response_customers['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
                else:
                    customers_url = None
            
            customer_dict = {customer['identification']: customer['name'] for customer in all_customers}

            flattened_results = []

            for result in response_sales['data']['results']:
                flattened_result = {
                    'id': result['id'],
                    'document_id': result['document']['id'],
                    'prefix': result['prefix'],
                    'number': result['number'],
                    'name': result['name'],
                    'date': result['date'],
                    'customer_id': result['customer']['id'],
                    'customer_identification': result['customer']['identification'],
                    'customer_branch_office': result['customer']['branch_office'],
                    'customer_name': customer_dict.get(result['customer']['identification'], 'Unknown'),
                    'seller': result['seller'],
                    'total': result['total'],
                    'balance': result['balance'],
                    'product_name': result['items'][0]['description'],
                    'quantity': result['items'][0]['quantity'],
                    'price': result['items'][0]['price'],
                    'observations': result['observations'],
                    'payment_id': result['payments'][0]['id'] if result['payments'] else None,
                    'payment_name': result['payments'][0]['name'] if result['payments'] else None,
                    'payment_value': result['payments'][0]['value'] if result['payments'] else None,
                    'payment_due_date': result['payments'][0]['due_date'] if result['payments'] else None,
                    'stamp_status': result['stamp']['status'],
                    'cufe': result['stamp']['cufe'],
                    'mail_status': result['mail']['status'],
                    'mail_observations': result['mail']['observations'],
                    'created': result['metadata']['created'],
                    'public_url': result['public_url']
                }

                for i, tax in enumerate(result['items'][0]['taxes']):
                    flattened_result[f'tax_{i+1}_id'] = tax['id']
                    flattened_result[f'tax_{i+1}_name'] = tax['name']
                    flattened_result[f'tax_{i+1}_type'] = tax['type']
                    flattened_result[f'tax_{i+1}_percentage'] = tax['percentage']
                    flattened_result[f'tax_{i+1}_value'] = tax['value']
                
                flattened_results.append(flattened_result)

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(3) # 3. Ventas.
             
            if permission:
                return Response(flattened_results, status=status.HTTP_200_OK)
            else:
                return Response(flattened_results, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
# ------ Menester ----------------------------------------    
class Taxes(APIView):
    def get(self, request):
        response = execute_request('https://api.siigo.com/v1/credit-notes', values={}, type='get', request=request)
        if response['status'] == False:
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response['data'], status=status.HTTP_200_OK)
        
# ---- Menester ----------------------------------------
class Vouchers(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_accounts_payable = []
        accounts_payable_url = 'https://api.siigo.com/v1/vouchers?page_size=100'
        page = 1

        while accounts_payable_url:
            response = execute_request(accounts_payable_url, values={}, type='get', request=request)
            
            if not response['status']:
                return Response({'message': 'Error en la obtención de cuentas por pagar'}, status=status.HTTP_400_BAD_REQUEST)

            all_accounts_payable.extend(response['data']['results'])

            total_results = response['data']['pagination']['total_results']
            page_size = 100
            if (page_size * page) < total_results:
                page += 1
                accounts_payable_url = f'https://api.siigo.com/v1/accounts-payable?page={page}&page_size={page_size}'
            else:
                accounts_payable_url = None

        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(5)  # Rol 5 es Cuentas por pagar

        if permission:
            return Response(all_accounts_payable, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene permisos para ver esta información'}, status=status.HTTP_403_FORBIDDEN)

# ---- Menester ----------------------------------------   
class Purchases(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_accounts_payable = []
        purchases_url = 'https://api.siigo.com/v1/purchases?page_size=100'
        page = 1

        while purchases_url:
            response = execute_request(purchases_url, values={}, type='get', request=request)

            if not response['status']:
                return Response({'message': 'Error en la obtención de cuentas por pagar'}, status=status.HTTP_400_BAD_REQUEST)

            for purchase in response['data']['results']:
                filtered_data = {
                    'name': purchase['name'],
                    'date': purchase['date'],
                    'items': [
                        {
                            'description': item['description'],
                            'price': item['price'],
                            'total': item['total'],
                            'iva': next((tax['value'] for tax in item.get('taxes', []) if tax['type'] == 'IVA'), 0)  # Solo IVA
                        } for item in purchase['items']
                    ]
                }
                all_accounts_payable.append(filtered_data)

            total_results = response['data']['pagination']['total_results']
            page_size = 100
            if (page_size * page) < total_results:
                page += 1
                purchases_url = f'https://api.siigo.com/v1/purchases?page={page}&page_size={page_size}'
            else:
                purchases_url = None

        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(5)  # Rol 5 es Cuentas por pagar

        if permission:
            return Response(all_accounts_payable, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene permisos para ver esta información'}, status=status.HTTP_403_FORBIDDEN)

# 4.Cartera general detallada por cliente.
class Tessera(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = {
            "year": year,
            "month_start": 1,
            "month_end": 13,
            "includes_tax_difference": False
        }
        payload_json = json.dumps(payload)
        try:
            response = execute_request('https://api.siigo.com/v1/test-balance-report-by-thirdparty', values=payload_json, type='post', request=request)
            
            report_third = Balance()
            data, success = report_third.balance_function_terceros(response)
            
            if isinstance(data, str):
                data = json.loads(data)
           
            records = data.get('data', []) 
            filtered_data = [item for item in records if item.get("Nombre_Cuenta_contable") == "Contables y tributarios"]
            
            result = [
                {
                    "Nombre_cliente": item.get("Nombre_tercero"),
                    "Identificación": item.get("Identificación"),
                    "saldo_final_deuda": item.get("Saldo_final")
                }
                for item in filtered_data
            ]
            
            if success:
                mixin = UserRoleMixin(request)
                permission = mixin.check_permissions(3) # 3. Ventas.
             
                if permission:
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TesseraDuo(APIView):
    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page_size=100'
            all_sales = []
            page = 1
            while sales_url:
                response_sales = execute_request(sales_url, values={}, type='get', request=request)
                if not response_sales['status']:
                    return Response({'message': 'Error en la obtención de ventas'}, status=status.HTTP_400_BAD_REQUEST)

                all_sales.extend(response_sales['data']['results'])

                total_results = response_sales['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    sales_url = f'https://api.siigo.com/v1/invoices?created_start={start_date}&created_end={end_date}&page={page}&page_size={page_size}'
                else:
                    sales_url = None

            customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
            all_customers = []
            page = 1
            while customers_url:
                response_customers = execute_request(customers_url, values={}, type='get', request=request)
                if not response_customers['status']:
                    return Response({'message': 'Error en la obtención de clientes'}, status=status.HTTP_400_BAD_REQUEST)
                
                all_customers.extend(response_customers['data']['results'])

                total_results = response_customers['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
                else:
                    customers_url = None

            customer_dict = {customer['identification']: customer['name'] for customer in all_customers}
            
            sales_data = []
            for sale in all_sales:
                sale_id = sale['name']
                cantidad_cuotas = 1
                deuda_por_cobrar = sale['total']
                sale_date = datetime.strptime(sale['date'], "%Y-%m-%d")
                dias_vencidos = (datetime.now() - sale_date).days
                customer_id = sale['customer']['identification']
                customer_name = customer_dict.get(customer_id, 'Desconocido')

                sales_data.append({
                    'id_venta': sale_id,
                    'cuotas': cantidad_cuotas,
                    'deuda_por_cobrar': deuda_por_cobrar,
                    'valor_a_favor': 0,
                    'dias_vencidos': dias_vencidos,
                    'id_cliente': customer_id,
                    'nombre_cliente': customer_name
                })

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(3) # 3. Ventas.
             
            if permission:
                return Response(sales_data, status=status.HTTP_200_OK)
            else:
                return Response(sales_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
# 5. Cuentas por pagar detallada por proveedor.        
class AccountsPayable(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, option):
        all_accounts_payable = []
        accounts_payable_url = 'https://api.siigo.com/v1/accounts-payable?page_size=100'
        page = 1

        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            while accounts_payable_url:
                response = execute_request(accounts_payable_url, values={}, type='get', request=request)
                
                if not response['status']:
                    return Response({'message': 'Error en la obtención de cuentas por pagar'}, status=status.HTTP_400_BAD_REQUEST)

                for account in response['data']['results']:
                    due_date = account['due']['date']
                    if start_date <= due_date <= end_date:
                        account_info = {
                            'idenficación': account['provider']['identification'],
                            'nombre_cliente': account['provider']['name'],
                            'deuda_total': account['due']['balance']
                        }
                        all_accounts_payable.append(account_info)

                total_results = response['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    accounts_payable_url = f'https://api.siigo.com/v1/accounts-payable?page={page}&page_size={page_size}'
                else:
                    accounts_payable_url = None

            grouped_accounts = defaultdict(lambda: {'deuda_por_pagar': 0, 'valor_anticipos': 0})

            for account in all_accounts_payable:
                if account['deuda_total'] > 0:
                    grouped_accounts[account['idenficación']]['deuda_por_pagar'] += account['deuda_total']
                else:
                    grouped_accounts[account['idenficación']]['valor_anticipos'] += account['deuda_total']

            result = []
            for client_id, values in grouped_accounts.items():
                result.append({
                    'idenficación': client_id,
                    'nombre_proveedor': next(account['nombre_cliente'] for account in all_accounts_payable if account['idenficación'] == client_id),
                    'deuda_por_pagar': values['deuda_por_pagar'],
                    'valor_anticipos': values['valor_anticipos'],
                    'saldo_proveedor': values['deuda_por_pagar'] + values['valor_anticipos'],
                    'valor_vencido': values['deuda_por_pagar']
                })

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(5)  # Rol 5 es Cuentas por pagar

            if permission:
                if result == []:
                    return Response({'message': 'No hay cuentas por pagar en el mes actual, consulte con la opcion 2 o 3 para encontrar datos'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(result, status=status.HTTP_200_OK)
               
            else:
                return Response({'message': 'No tiene permisos para ver esta información'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AccountsPayableDuo(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            response = execute_request('https://api.siigo.com/v1/accounts-payable', values={}, type='get', request=request)

            if not response['status']:
                return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

            flattened_results = []

            for result in response['data']['results']:
                due_date = result['due']['date']
                if start_date <= due_date <= end_date:
                    flattened_result = {
                        'due_prefix': result['due']['prefix'],
                        'due_consecutive': result['due']['consecutive'],
                        'due_quote': result['due']['quote'],
                        'due_date': result['due']['date'],
                        'due_balance': result['due']['balance'],
                        'provider_id': result['provider']['id'],
                        'provider_identification': result['provider']['identification'],
                        'provider_name': result['provider']['name']
                    }
                    flattened_results.append(flattened_result)

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(6)  #rol 6 tiene acceso a cuentas por pagar
            
            if not permission:
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if flattened_results == []:
                    return Response({'message': 'No hay cuentas por pagar en el mes actual, consulte con la opcion 2 o 3 para encontrar datos'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(flattened_results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AccountsPayableTris(APIView):
    permission_classes = [IsAuthenticated]

    def options(self, request, *args, **kwargs):
        url = 'https://api.siigo.com/v1/test-balance-report'
        
        try:
            response = requests.options(url)
            if response.status_code == 200:
                return Response(response.json(), status=200)
            else:
                return Response({'error': 'No se pudo obtener la información de la API.'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)
        
# 6. ******* Reporte de comprobantes detallados. *************
class Journals(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self, request, option):
        url = 'https://api.siigo.com/v1/journals'
        
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            response = execute_request(url, values={}, type='get', request=request)
            if not response['status']:
                return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
            
            customer_dict = GetCustomer.get_customers(request)
            if customer_dict is None:
                return Response({'message': 'Error en la obtención de clientes'}, status=status.HTTP_400_BAD_REQUEST)
            
            journal_data = response['data']['results']
            formatted_results = []

            for journal in journal_data:
                journal_date = datetime.strptime(journal['date'], '%Y-%m-%d')
                
                if start_date <= journal_date.strftime('%Y-%m-%d') <= end_date:
                    for item in journal['items']:
                        formatted_results.append({
                            'fecha': journal['date'],
                            'codigo_cuenta': item['account']['code'],
                            'movimiento': item['account']['movement'],
                            'id_cliente': item['customer']['identification'],
                            'nombre_cliente': customer_dict.get(item['customer']['identification'], 'Unknown'),
                            'descripcion': item['description'],
                            'valor': item['value']
                        })
            
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(6)  # Rol 6 es Reporte de comprobantes
            
            if not permission:
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(formatted_results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# 6. ***** Reporte de comprobantes detallados. *************
class JournalsDuo(APIView, UserRoleMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            response = execute_request('https://api.siigo.com/v1/journals', values={}, type='get', request=request)

            if not response['status']:
                return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                mixin = UserRoleMixin(request)
                permission = mixin.check_permissions(6)  # Rol 6 es Reporte de comprobantes

                if not permission:
                    return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

                flattened_results = []
                for result in response['data']['results']:
                    result_date = datetime.strptime(result['date'], '%Y-%m-%d')
                    
                    if start_date <= result_date.strftime('%Y-%m-%d') <= end_date:
                        for item in result['items']:
                            flattened_result = {
                                "id": result["id"],
                                "document_id": result["document"]["id"],
                                "number": result["number"],
                                "name": result["name"],
                                "date": result["date"],
                                "account_code": item["account"]["code"],
                                "account_movement": item["account"]["movement"],
                                "customer_id": item["customer"]["id"],
                                "customer_identification": item["customer"]["identification"],
                                "branch_office": item["customer"]["branch_office"],
                                "cost_center": item.get("cost_center", None),
                                "description": item["description"],
                                "value": item["value"],
                                "created": result["metadata"]["created"]
                            }
                            flattened_results.append(flattened_result)

                return Response(flattened_results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

      
        
# 7. ******** Clientes totales (Provedores y clientes) **************
class Customers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
        all_customers = []
        page = 1

        while customers_url:
            response_customers = execute_request(customers_url, values={}, type='get', request=request)
            if not response_customers['status']:
                return None

            for customer in response_customers['data']['results']:
                contacts = customer.get('contacts', [])
                contact = contacts[0] if len(contacts) > 0 else {}

                cliente_planificado = {
                    'id': customer.get('id'),
                    'tipo': customer.get('type'),
                    'tipo_persona': customer.get('person_type'),
                    'codigo_tipo_id': customer.get('id_type', {}).get('code'),
                    'nombre_tipo_id': customer.get('id_type', {}).get('name'),
                    'identificacion': customer.get('identification'),
                    'sucursal': customer.get('branch_office'),
                    'digito_verificacion': customer.get('check_digit'),
                    'nombre': customer.get('name', [])[0] if customer.get('name') else '',
                    'activo': customer.get('active'),
                    'responsable_iva': customer.get('vat_responsible'),
                    'codigo_responsabilidad_fiscal': customer.get('fiscal_responsibilities', [{}])[0].get('code'),
                    'nombre_responsabilidad_fiscal': customer.get('fiscal_responsibilities', [{}])[0].get('name'),
                    'direccion': customer.get('address', {}).get('address'),
                    'codigo_pais': customer.get('address', {}).get('city', {}).get('country_code'),
                    'nombre_pais': customer.get('address', {}).get('city', {}).get('country_name'),
                    'codigo_estado': customer.get('address', {}).get('city', {}).get('state_code'),
                    'nombre_estado': customer.get('address', {}).get('city', {}).get('state_name'),
                    'codigo_ciudad': customer.get('address', {}).get('city', {}).get('city_code'),
                    'nombre_ciudad': customer.get('address', {}).get('city', {}).get('city_name'),
                    'indicativo_telefono': customer.get('phones', [{}])[0].get('indicative'),
                    'numero_telefono': customer.get('phones', [{}])[0].get('number'),
                    'extension_telefono': customer.get('phones', [{}])[0].get('extension'),
                    'nombre_contacto': contact.get('first_name'),
                    'apellido_contacto': contact.get('last_name'),
                    'email_contacto': contact.get('email'),
                    'indicativo_telefono_contacto': contact.get('phone', {}).get('indicative'),
                    'numero_telefono_contacto': contact.get('phone', {}).get('number'),
                    'fecha_creacion_metadata': customer.get('metadata', {}).get('created')
                    }
                all_customers.append(cliente_planificado)


            total_results = response_customers['data']['pagination']['total_results']
            page_size = 100
            if (page_size * page) < total_results:
                page += 1
                customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
            else:
                customers_url = None
            
        
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(7)  # Rol 6 es Reporte de clientes
        
            if not permission:
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(all_customers, status=status.HTTP_200_OK)

class CustomersBI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, option):
        try:
            try:
                start_date, end_date = DateRangeCalculator.get_date_range(option)
            except ValueError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
            all_customers = []
            page = 1

            while customers_url:
                response_customers = execute_request(customers_url, values={}, type='get', request=request)
                if not response_customers['status']:
                    return Response({'message': 'Error retrieving customers'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                for customer in response_customers['data']['results']:
                    fecha_creacion = customer.get('metadata', {}).get('created')

                    if fecha_creacion:
                        fecha_creacion = fecha_creacion.split('.')[0]
                        fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%dT%H:%M:%S')

                        if start_date <= fecha_creacion.strftime('%Y-%m-%d') <= end_date:
                            cliente_nuevo = {
                                'identificacion': customer.get('identification'),
                                'nombre': customer.get('name', [])[0] if customer.get('name') else '',
                                'año_creacion': fecha_creacion.strftime('%Y'),
                                'mes_creacion': fecha_creacion.strftime('%B')
                            }
                            all_customers.append(cliente_nuevo)

                total_results = response_customers['data']['pagination']['total_results']
                page_size = 100
                if (page_size * page) < total_results:
                    page += 1
                    customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
                else:
                    customers_url = None

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(7)

            if not permission:
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    'cantidad_clientes_nuevos': len(all_customers),
                    'clientes_nuevos': all_customers
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
# 8. ********** Productos totales *******************
class Products(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products_url = 'https://api.siigo.com/v1/products?page_size=100'
        all_products = []
        page = 1

        while products_url:
            response_products = execute_request(products_url, values={}, type='get', request=request)
            if not response_products['status']:
                return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

            for product in response_products['data']['results']:
                flat_product = {
                    'id': product.get('id'),
                    'code': product.get('code'),
                    'name': product.get('name'),
                    'type': product.get('type'),
                    'description': product.get('description', ''),
                    'unit_code': product.get('unit', {}).get('code'),
                    'unit_name': product.get('unit', {}).get('name'),
                    'unit_label': product.get('unit_label', ''),
                    'stock_control': product.get('stock_control'),
                    'available_quantity': product.get('available_quantity'),
                    'account_group_id': product.get('account_group', {}).get('id'),
                    'account_group_name': product.get('account_group', {}).get('name'),
                    'tax_classification': product.get('tax_classification'),
                    'tax_included': product.get('tax_included'),
                    'tax_consumption_value': product.get('tax_consumption_value'),
                    'active': product.get('active'),
                    'metadata_created': product.get('metadata', {}).get('created'),
                    'metadata_last_updated': product.get('metadata', {}).get('last_updated')
                }

                taxes = product.get('taxes', [])
                for i, tax in enumerate(taxes):
                    flat_product[f'tax_{i+1}_name'] = tax.get('name')
                    flat_product[f'tax_{i+1}_type'] = tax.get('type')
                    flat_product[f'tax_{i+1}_percentage'] = tax.get('percentage')

                warehouses = product.get('warehouses', [])
                for i, warehouse in enumerate(warehouses):
                    flat_product[f'warehouse_{i+1}_id'] = warehouse.get('id')
                    flat_product[f'warehouse_{i+1}_name'] = warehouse.get('name')
                    flat_product[f'warehouse_{i+1}_quantity'] = warehouse.get('quantity')

                all_products.append(flat_product)

            total_results = response_products['data']['pagination']['total_results']
            page_size = 100
            if (page_size * page) < total_results:
                page += 1
                products_url = f'https://api.siigo.com/v1/products?page={page}&page_size={page_size}'
            else:
                products_url = None

            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(7)  # Rol 6 es Reporte de clientes
        
            if not permission:
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(all_products, status=status.HTTP_200_OK)


class DateRangeCalculator:
    @staticmethod
    def get_date_range(option):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Este es para el mes
        if option == 1:
            start_date = f"{current_year}-{current_month:02d}-01"
            end_date = f"{current_year}-{current_month:02d}-{monthrange(current_year, current_month)[1]}"

        # Este es para el trimestre
        elif option == 2:
            if current_month in [1, 2, 3]:
                start_month, end_month = 1, 3
            elif current_month in [4, 5, 6]:
                start_month, end_month = 4, 6
            elif current_month in [7, 8, 9]:
                start_month, end_month = 7, 9
            else:
                start_month, end_month = 10, 12

            start_date = f"{current_year}-{start_month:02d}-01"
            end_date = f"{current_year}-{end_month:02d}-{monthrange(current_year, end_month)[1]}"

        # Este es para el semestre
        elif option == 3:
            if current_month <= 6:
                start_month, end_month = 1, 6
            else:
                start_month, end_month = 7, 12

            start_date = f"{current_year}-{start_month:02d}-01"
            end_date = f"{current_year}-{end_month:02d}-{monthrange(current_year, end_month)[1]}"

        else:
            raise ValueError("Opción inválida. Elija entre 1 (mes), 2 (trimestre) o 3 (semestre).")

        return start_date, end_date
    
class GetCustomer:
    @staticmethod
    def get_customers(request):
        customers_url = 'https://api.siigo.com/v1/customers?page_size=100'
        all_customers = []
        page = 1
        
        while customers_url:
            response_customers = execute_request(customers_url, values={}, type='get', request=request)
            if not response_customers['status']:
                return None
            
            all_customers.extend(response_customers['data']['results'])
            
            total_results = response_customers['data']['pagination']['total_results']
            page_size = 100
            if (page_size * page) < total_results:
                page += 1
                customers_url = f'https://api.siigo.com/v1/customers?page={page}&page_size={page_size}'
            else:
                customers_url = None
        
        return {customer['identification']: customer['name'] for customer in all_customers}