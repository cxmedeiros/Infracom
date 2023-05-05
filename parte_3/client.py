import socket
from rdtSender import RdtSender
from rdtReceiver import RdtReceiver
from Utils import IP_ADDRESS, PORT_NO, BUFFER_SIZE
from message import CustomerInfo, MenuRequest, PlaceOrder, PayBill
from message_utils import encode_message, decode_message

def main():
    sender = RdtSender(IP_ADDRESS, PORT_NO) #inicia Sender

    print("Chame o CINtofome para iniciar")
    input()
    print("Digite sua mesa")
    num_mesa = int(input("Número da mesa: "))  # inicio da interação
    nome_cliente = input("Seu nome: ")

#------------------- enviando info para servidor ------------------------------
    message = CustomerInfo(num_mesa, nome_cliente)
    encoded_message = encode_message(message)
    response = sender.send_message(encoded_message) 
    decoded_response = decode_message(response)

    if decoded_response.message_type == "CUSTOMER_INFO_ACK": #IMPLEMENTAR ISSO NO SERVER.PY
        print("Bem-vindo, {}! Sua mesa é {}." .format(nome_cliente, num_mesa))
    else:
        print("Erro no sistema[ACK]. Tente novamente")
        return
#-------------------------------------------------------------------------------

    while True:
        print("\nFaça sua escolha:")
        print("1 - Ver Cardápio")
        print("2 - Fazer pedido")
        print("3 - Pagar a conta")
        
        escolha = int(input("Digite o número: "))

        if escolha == 1:
            message = MenuRequest()

            encoded_message = encode_message(message) # Codificar e mandar
            response = sender.send_message(encoded_message)
            decoded_response = decode_message(response)

            if decoded_response.message_type == "MENU":
                print("Cardapio: ")
                print(decoded_response.data) #Printa o cardapio
        
        elif escolha == 2:
            pedidos = input("Digite qual primeiro item que gostaria(número): ")
            while(input("Gostaria de mais algum item? [s/n]") == "s"):
                

            

    # IMPLEMENTAR RESTO DAS OPCOES..

if __name__ == "__main__":
    client = Client()
    client.run()

    # ATUALIZAR SERVER.PY PARA GERENCIAR 'MESSAGE' E GUARDAR DADOS DOS CLIENTES
    