import pandas as pd
# Open the file
file = open('usr.csv', 'r+', encoding='utf-8')

# Read the content
content =  pd.read_csv('usr.csv',header=0,sep=',')

def getUserPass(request):
    # getting elements in between using split() and join()
    username = ''.join(request.split("username=")[1].split("&")[0])
    password = ''.join(request.split("password=")[1].split("\n")[0])
    # printing result
    print('username : ' + username) 
    print('password : ' + password)
    return username, password

def getPassStatusIndex(username):
    username_index = content[content['username'] == username].index.tolist()
    print('username index : ', username_index)
    return username_index
    

def checkLogin(request):
    username,password = getUserPass(request)
    index = getPassStatusIndex(username)   
    if (content['username'].isin([username]).any() == False):
        #Username is not found
        return 2
    else:
        hold_password = content.loc[index, 'password']
        print('hold : ', hold_password[0])
        if (hold_password[0] != password):
            #Password is incorrect
            return 1
        else:
            #Correct Password, check status
            hold_status = content.loc[index, 'status']
            if hold_status[0] == 1:
                #Already logged in
                return 3
            else:
                #Login success
                replaceStatus(index, 1)
                return 0

def replaceStatus(index, new_status):
    if index:  # If the list is not empty
        # Replace the status
        content.loc[index, 'status'] = new_status
    content.to_csv('usr.csv', index=False)

file.close()
