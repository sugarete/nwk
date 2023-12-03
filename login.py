import pandas as pd

def getUserPass(request):
    # getting elements in between using split() and join()
    username = ''.join(request.split("username=")[1].split("&")[0])
    password = ''.join(request.split("password=")[1].split("\n")[0])
    # printing result
    # print('username : ' + username) 
    # print('password : ' + password)
    return username, password

def getPassStatusIndex(username, content):
    username_index = content[content['username'] == username].index.tolist()
    # print('username index : ', username_index)
    return username_index

def checkLogin(request):
    content =  pd.read_csv('usr.csv',header=0,sep=',')
    username,password = getUserPass(request)
    index = getPassStatusIndex(username, content)   
    if (content['username'].isin([username]).any() == False):
        #Username is not found
        return 2
    else:
        hold_password = content.loc[index, 'password']
        # print('hold : ', hold_password.values[0])
        if (hold_password.values[0] != password):
            #Password is incorrect
            return 1
        else:
            return 0




