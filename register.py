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
    if len(password)<5:
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
        

        
