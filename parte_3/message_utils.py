
#---------------------------------------------------------
# Modulo para funcoes de encoding e decoding no formato JSON

# Serve para converter instancias da classe Message e suas subclasses
# em um formato padrao p/ ser transmitido entre cliente e servidor
#----------------------------------------------------------


import json
from message import Message, MenuRequest, PlaceOrder, PayBill, CustomerInfo


def encode_message(message):                   # pega Message ou subclasses e converte para JSON.
    message_dict = {                           # mensage_type e data sao dicionarios que correspondem
        "message_type": message.message_type,  # aos atributos do objeto
        "data": message.data
    }
    return json.dumps(message_dict)            #Converte o dicionario para uma string JSON ser transmitida

def decode_message(message_str):               #Faz o contrario, convertendo JSON de volta ao objeto `Message`
    message_dict = json.loads(message_str)
    message_type = message_dict["message_type"]
    data = message_dict["data"]

    if message_type == "CUSTOMER_INFO":
        return CustomerInfo(data["table_number"], data["customer_name"])
    if message_type == "MENU_REQUEST":
        return MenuRequest()
    elif message_type == "PLACE_ORDER":
        return PlaceOrder(data["table_number"], data["customer_name"], data["order_items"])
    elif message_type == "PAY_BILL":
        return PayBill(data["table_number"], data["customer_name"], data["amount_paid"])
    else:  
        return Message(message_type, data)    #Caso nao seja nenhuma das mensagem, retorna generico
