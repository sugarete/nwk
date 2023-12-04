import csv
from urllib.parse import parse_qs

def is_username_registered(username):
    with open('usr.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)               
        for row in reader:
            if row and row[0] == username:
                return 1
    return 0

def register_handle(request):
    content_length = int(request.split('Content-Length: ')[1].split('\n')[0])
    form_data = parse_qs(request.split('\r\n\r\n')[1][:content_length].encode('utf-8'))
    # print('day la register')
    # print( form_data)
    username = form_data.get(b'username',[b''])[0].decode('utf-8')
    # print('Username:', username)
    password = form_data.get(b'password',[b''])[0].decode('utf-8')
    # print('here')
    # check username
    if len(password)<4:
        return 1 #qua yeu 
    else:
        if is_username_registered(username):
            return 2
        else:
            with open('usr.csv', 'a', newline='') as csvfile:
                fieldnames = ['username', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
                if csvfile.tell() == 0:
                    writer.writeheader()
                
                writer.writerow({'username': username , 'password': password})
            return 0
        
def check_olduser(username, oldpassword):   
    with open('usr.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[0] == username and row[1] == oldpassword:
                return True
    return False

def change_pwd(request):
    content_length = int(request.split('Content-Length: ')[1].split('\n')[0])
    form_data = parse_qs(request.split('\r\n\r\n')[1][:content_length].encode('utf-8'))  

    username = form_data.get(b'username',[b''])[0].decode('utf-8')
    oldpassword = form_data.get(b'oldpassword',[b''])[0].decode('utf-8')
    password=form_data.get(b'password',[b''])[0].decode('utf-8')

    if check_olduser(username, oldpassword): #check user cu co khop khong     
        if len(password)<4 :
            return 1 # mk không đủ độ dài 
        else:
            with open('usr.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

    
            index_to_update = None
            for i, row in enumerate(rows):
                if row and row[0] == username:
                    index_to_update = i
                    break
            if index_to_update is not None:       
                rows[index_to_update][1] = password
       
                with open('usr.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)
                return 0 #doi mk thanh cong
    else :
        return 2 # user khong khop 