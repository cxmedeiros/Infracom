#---------------------------------------------------------------------

#AQUI CRIAMOS CLASSES E FUNCOES PARA GERENCIAR DIFERENTES TIPOS DE MSG
#PADRONIZAR FORMATOS DE MENSAGEM PARA COMUNICAO ENTRE SERVER E CLIENTE

#---------------------------------------------------------------------

import json  #Vamos usar o formato JSON como formato padrao

class Message:
    def __init__(self, message_type, data): #message_type -> "MENU_REQUEST", "PLACE_ORDER"...
        self.message_type = message_type
        self.data = data

class CustomerInfo(Message):                # Condiciao incial p/ receber nome e mesa do cliente
    def __init(self, table_number, customer_name):
        data = {
            "table_number": table_number,
            "customer_name": customer_name
        }
        super().__init__("CUSTOMER_INFO", data)

class MenuRequest(Message):           #nao precisa de nenhum argumento para pegar carpadio
    def __init__(self):
        super().__init__("MENU_REQUEST", None)

class PlaceOrder(Message): 
    def __init__(self,table_number, customer_name, order_items):
        data = {
            "table_number" : table_number,
            "customer_name": customer_name,
            "order_items": order_items
        }
        super().__init__("PLACE_ORDER", data)

class PayBill(Message):
    def __init__(self, table_number, customer_name, amount_paid):
        data = {
            "table_number": table_number,
            "customer_name": customer_name,
            "amount_paid": amount_paid
        }
        super().__init__("PAY_BILL", data)


# ------------- EXEMPLO EM client.py --------------------------------
#      from message import MenuRequest
#      from message_utils import encode_message
#      
#      menu_request = MenuRequest()
#      message_str = encode_message(menu_request)

# mandar message_str usando RDT_sender
#---------------------------------------------------------------------


# ------------- EXEMPLO EM server.py --------------------------------
#    from message_utils import decode_message
#
#    # receber a message_str usando RDT_receiver
#    message = decode_message(message_str)
# ---------------------------------------------------------------------