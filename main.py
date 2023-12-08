import getpass
import pwinput
import http.client
import json
import os
import shutil
import ssl
import sys
import time
import datetime


import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def login():
    global gstat
    gstat = "não autenticado"
    global conn
    conn = http.client.HTTPSConnection(
        <url>, context=ssl._create_unverified_context())
    tipe = input("Digite o tipo de login(LDAP ou RADIUS): ")
    logonURI = "/PasswordVault/API/auth/"+tipe.upper()+"/Logon/"
    os.system('cls')
    print("-----------------------------------------")
    if tipe.upper() == "LDAP" or "RADIUS":
        username = input("Digite seu usuário: ")
        password = pwinput.pwinput(prompt="Digite sua senha (LDAP) ou Token (RADIUS): ",mask="*")
        print("-----------------------------------------")
        os.system('cls')
        
    else:
        os.system('cls')
        print("Tipo de login inválido!")
        time.sleep(3.0)
        os.system('cls')
        return 0
    os.system('cls')
    logonPayload = json.dumps({
        "username": username,
        "password": password,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", logonURI, logonPayload, headers)
    except:
        print("Conexão falhou, você não está logado!")
        time.sleep(3.0)
        os.system('cls')
    logonResult = conn.getresponse()
    authToken = logonResult.read()
    if "ErrorCode" in authToken.decode("utf-8"):
        print(authToken.decode("utf-8"))
        print("Erro ao logar")
        time.sleep(3.0)
        os.system('cls')
        gstat = "não autenticado"
    else:
        gstat = "Autenticado"
        os.system("cls")
    global loginresult
    loginresult = {
        'Authorization': authToken.decode("utf-8").strip('"'),
        'Content-Type': 'application/json'
    }

def logoff():
    url = "/PasswordVault/API/Auth/Logoff"
    try:
        conn.request("post", url, "", loginresult)
    except:
        os.system("cls")
        print("Você está logado?")
        time.sleep(3.0)
        os.system('cls')
    result = conn.getresponse()
    resultt = result.read()
    if "ErrorCode" in resultt.decode("utf-8"):
        os.system("cls")
        print(resultt.decode("utf-8"))
        print("Erro ao tentar deslogar! Saindo da aplicação")
        time.sleep(3.0)
        os.system('cls')
        sys.exit()
    else:
        os.system("cls")
        print("deslogado com susseso!")
        time.sleep(3.0)
        os.system('cls')
        sys.exit()

def listSafes():
    url = "https://<url>/PasswordVault/WebServices/PIMServices.svc/Safes"
    try:
        response = requests.get(url, headers=loginresult, verify=False)
    except:
        os.system('cls')
        print("Problema ao listar Safes... você está logado?")
        time.sleep(3.0)
        os.system('cls')
        return 0
    data = response.json()
    with open("C:\\Users\\Public\\SAFES.json", "w") as text_file:
        json.dump(data, text_file, indent=4)
    os.system('cls')
    print("Arquivo de com todas os safes criado com sucesso!")
    time.sleep(3.0)
    os.system('cls')

def infoPlat():
    os.system('cls')
    name = input(
        "Digite o nome da plataforma que você que ver as informações: ")
    url = "https://<url>/PasswordVault/API/Platforms/"+name
    try:
        response = requests.get(url, headers=loginresult, verify=False)
    except:
        os.system('cls')
        print("Problema ao retornar a plataforma.")
        time.sleep(3.0)
        os.system('cls')
        return 0
    data = response.json()
    with open("C:\\Users\\Public\\"+name+".json", "w") as text_file:
        json.dump(data, text_file, indent=4)
    os.system('cls')
    print("O arquivo de informações foi criado com sucesso!")
    time.sleep(3.0)
    os.system('cls')

def exportPlat():

    os.system('cls')
    id = input("Digite o nome da plataforma que você que ver as informações: ")
    url = "https://<url>/PasswordVault/API/Platforms/"+id+"/Export"
    try:
        response = requests.post(
            url, headers=loginresult, stream=True, verify=False)
    except:
        os.system('cls')
        print("Problema ao retornar a plataforma.")
        time.sleep(3.0)
        os.system('cls')
        return 0

    oi = response.headers["Content-Disposition"].split("=")[1]
    with open("C:\\Users\\Public\\"+oi, "wb") as text_file:
        shutil.copyfileobj(response.raw, text_file)

    os.system('cls')
    print("O arquivo da plataforma foi exportado com sucesso!")
    time.sleep(3.0)
    os.system('cls')

def arrumadata():
    data0 = json.loads(open("C:\\Users\\Public\\Accounts0.json", 'r').read())
    data1 = json.loads(open("C:\\Users\\Public\\Accounts1.json", 'r').read())
    data2 = json.loads(open("C:\\Users\\Public\\Accounts2.json", 'r').read())
    data=[data0,data1,data2]
    for x in data:
        if "ErrorCode" not in x:
            for i in x["value"]:
                unixToDatetime = datetime.datetime.fromtimestamp(i['createdTime'])
                i['createdTime'] = unixToDatetime
    return 0

def listAccount():
    j = 0
    pont = "."
    url = [
        "https://<url>/PasswordVault/api/accounts?offset=0&limit=1000",
        "https://<url>/PasswordVault/api/accounts?offset=1000&limit=1000",
        "https://<url>/PasswordVault/api/accounts?offset=2000&limit=1000"]
    for i in url:
        response = requests.get(i, headers=loginresult, verify=False)
        os.system('cls')
        print("Atualizando dados"+pont)
        data = response.json()
        with open("C:\\Users\\Public\\Accounts"+str(j)+".json", "w") as text_file:
            json.dump(data, text_file, indent=4)
            
        j = j+1
        pont = pont+"."
    os.system('cls')
    print("Os arquivos de contas foram exportados com sucesso!")
    time.sleep(2.0)
    os.system('cls')
    print("arrumando formato das datas...")
    arrumadata()
    os.system('cls')
    print("Tudo pronto!")
    time.sleep(2.0)
    os.system('cls')

def createAccount():

    os.system('cls')
    platformID = input("Digite o nome da plataforma: ")
    accountAddress = input("Digite o endereço da conta: ")
    accountUsername = input("Digite o usuário da conta: ")
    description = input('Digite uma descrição')
    safeName = input("Digite o nome do safe: ")
    addAccountURI = "/PasswordVault/api/Accounts"
    accountName = "Operating System-"+platformID + \
        "-"+accountAddress+"-"+accountUsername
        
    addAccountBody = json.dumps({
        "name": accountName,
        "address": accountAddress,
        "userName": accountUsername,
        "platformId": platformID,
        "safeName": safeName,
        "secretType": "password",
        "secret": ".",
        "platformAccountProperties": {
            "Custodio_1": ".",
            "Custodio_2": ".",
            "OwnerName": ".",
            "ConnectAs": "...",
            "Description": description,
        },
    })
    try:
        # issue the connection request
        conn.request("POST", addAccountURI, addAccountBody, loginresult)
        addAccountResult = conn.getresponse()
        addAccount = addAccountResult.read()
    except:
        print("Você não está logado!")
        sys.exit()
    if "ErrorCode" in addAccount.decode("utf-8"):
        print(addAccount.decode("utf-8"))
        print("Exiting function")
        return 0
    else:
        print("Account adicionada com sucesso!")

    # return the result in the form of addAccount
    return addAccount

def searchAccountByID():
    id = input("Digite o id da Account: ")
    url = "https://<url>/PasswordVault/api/Accounts/"+id
    response = requests.get(url, headers=loginresult, verify=False)
    os.system('cls')
    data = response.json()
    data1 = json.dumps(data, indent=4)
    print(data1)
    input("aperte enter para continuar")
    os.system('cls')
    return 0

def searchAccountID():
    valu=[]
    listAccount()
    name = input("Digite o nome da Account: ")
    data0 = json.loads(open("C:\\Users\\Public\\Accounts0.json", 'r').read())
    data1 = json.loads(open("C:\\Users\\Public\\Accounts1.json", 'r').read())
    data2 = json.loads(open("C:\\Users\\Public\\Accounts2.json", 'r').read())
    data = [data0, data1,data2]
    for x in data:
        for i in x["value"]:
            if i['userName'] == name:
                print("O ID da Account "+name+" é: "+i["id"])
                input("aperte enter para continuar")
                os.system('cls')
                valu.append(i["id"])

    if valu == []:
        print("Usuário não encontrado!")
        input("aperte enter para continuar")
        os.system('cls')
        return 0
    else:
        return valu[0], 0

def searchAccountByName():
    flag = 0
    name = input("Digite o nome da Account: ")
    data0 = json.loads(open("C:\\Users\\Public\\Accounts0.json", 'r').read())
    data1 = json.loads(open("C:\\Users\\Public\\Accounts1.json", 'r').read())
    data2 = json.loads(open("C:\\Users\\Public\\Accounts2.json", 'r').read())
    data=[data0,data1,data2]
    for x in data:
        if "ErrorCode" not in x:
            for i in x["value"]:
                if i['userName'] == name:
                    cont = json.dumps(i, indent=4)
                    print(cont)
                    flag = 1
                    input("aperte enter para continuar")
                    os.system('cls')

    if flag == 0:
        print("conta não encontrada")
        input("aperte enter para continuar")
        os.system('cls')

def quebraCust():
    accountId = searchAccountID()
    if (accountId == 0):
        return 0
    else:

        motive = input("Digite o motivo da quebra: ")
        ticket = input("Digite o ticket da quebra: ")
        uri = "/PasswordVault/api/Accounts/" + \
            str(accountId)+"/Password/Retrieve"
        payload = json.dumps({
            "reason": motive,
            "TicketingSystemName": ".",
            "TicketId": ticket,
            "ActionType": "show",
            "isUse": "false"
        })
        try:
            conn.request("POST", uri, payload, loginresult)
        except:
            print("você não está logado")
            return 0

        resp = conn.getresponse()
        respq = resp.read()
        senha = json.loads(respq)
        os.system('cls')
        print("quebra de custódia realizada com sucesso!")
        print("A senha é: "+senha)
        time.sleep(3.0)
        os.system('cls')

def autocreateServerAccountLX():
    os.system('cls')
    
    addAccountURI = "/PasswordVault/api/Accounts"
    
    platformID = "."
    accountUsername = ".."
    safeName = "."
    accountAddress = input("Digite o endereço da conta: ")
    accountName = "Operating System-"+platformID + \
        "-"+accountAddress+"-"+accountUsername
    
    platformID1 = "."
    accountUsername1 = "."
    safeName1 = "."
    accountAddress1 = input("Digite o endereço da conta: ")
    accountName1 = "Operating System-"+platformID + \
        "-"+accountAddress+"-"+accountUsername    

    # Define Body
    addAccountBody = json.dumps({
        "name": accountName,
        "address": accountAddress,
        "userName": accountUsername,
        "platformId": platformID,
        "safeName": safeName,
        "secretType": "password",
        "platformAccountProperties": {},
    })
    addAccountBody1 = json.dumps({
        "name": accountName1,
        "address": accountAddress1,
        "userName": accountUsername1,
        "platformId": platformID1,
        "safeName": safeName1,
        "secretType": "password",
        "platformAccountProperties": {},
    })
    try:
        # issue the connection request
        conn.request("POST", addAccountURI, addAccountBody, loginresult)
        addAccountResult = conn.getresponse()
        addAccount = addAccountResult.read()
    except:
        print("Você não está logado!")
        sys.exit()

    try:
        conn.request("POST", addAccountURI, addAccountBody1, loginresult)
        addAccountResult1 =conn.getresponse()
        addAccount1 = addAccountResult1.read
    except:
        print("Você não está logado!")
        sys.exit()
        
    if "ErrorCode" in addAccount.decode("utf-8"):
        print(addAccount.decode("utf-8"))
        print("Exiting function")
        return 0
        time.sleep()
    else:
        print("Account adicionada com sucesso!")

    return addAccount,addAccount1

def autocreateServerAccountWS():
    os.system('cls')
    
    addAccountURI = "/PasswordVault/api/Accounts"
    
    platformID = "."
    accountUsername = "."
    safeName = "."
    accountAddress = input("Digite o endereço da conta: ")
    accountName = "Operating System-"+platformID + \
        "-"+accountAddress+"-"+accountUsername

    addAccountBody = json.dumps({
        "name": accountName,
        "address": accountAddress,
        "userName": accountUsername,
        "platformId": platformID,
        "safeName": safeName,
        "secretType": "password",
        "platformAccountProperties": {},
    })
    
    try:
        # issue the connection request
        conn.request("POST", addAccountURI, addAccountBody, loginresult)
        addAccountResult = conn.getresponse()
        addAccount = addAccountResult.read()
    except:
        print("Você não está logado!")
        sys.exit()
        
    if "ErrorCode" in addAccount.decode("utf-8"):
        print(addAccount.decode("utf-8"))
        print("Exiting function")
        return 0
        time.sleep()
    else:
        print("Account adicionada com sucesso!")

    return addAccount,addAccount1

def createServerAccounts():
    i = int(input("Quantos servidores são .?"))
    j = int(input("Quantos servidores são .?"))
    if i>0:
        while i>0:
            ti+=autocreateServerAccountLX()
            i-1
    if j>0:
        while j>0:
            tj+=autocreateServerAccountWS()
            j-1
    
    return ti, tj 
    
login()
menu = {}
menu['status:'] = gstat
menu['1'] = "- Logar"
menu['2'] = "- Listar Safes"
menu['3'] = "- Listar Accounts"
menu['4'] = "- Criar Account"
menu['5'] = "- Procurar Account por Nome"
menu['6'] = "- Procurar Account por ID"
menu['7'] = "- Quebrar Custódia"
menu['8'] = " - Gerar accounts de servidores"
menu['0'] = "- Deslogar"
while True:
    options = menu.keys()
    for entry in options:
        print(entry, menu[entry])

    selection = input("Selecione uma opção: ")
    if selection == '1':
        login()
    elif selection == '2':
        listSafes()
    elif selection == '3':
        listAccount()
    elif selection == '4':
        createAccount()
    elif selection == '5':
        searchAccountByName()
    elif selection == '6':
        searchAccountByID()
    elif selection == '7':
        quebraCust()
    elif selection == '8':
        createServerAccounts()
    elif selection == '0':
        logoff()
    else:
        os.system('cls')
        print("opção escolhida é inválida!")
        time.sleep(1.0)
        os.system('cls')
