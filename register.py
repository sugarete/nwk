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
    if is_username_registered(username):
        return 1
    else:
        with open('usr.csv', 'a', newline='') as csvfile:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerow({'username': username , 'password': password})
        return 0
        

        
# def handle_http_request(addr, request):
#     """Handles HTTP requests."""
#     request_line = request.split('\n')
#     method, uri = request_line[0].split()[:2]
#     print("client addr ", addr, "with request: ", method, uri)
#     if method == "GET":
#         if uri == "/login" or uri == "/":
#             return create_response(read_html("app/templates/login.html"))
#         elif uri == "/register":
#             return create_response(read_html("app/templates/register.html"))
#     elif method == "POST":
    
#         if uri == "/":
#             if "username=admin&password=admin" in request:
#                 return create_response(read_html("app/templates/home.html"))
#             else:
#                 return create_response(read_html("app/templates/login.html"))
#         elif uri == "/register":
#             # THAY CHO NAY 
#             if register(request):
#                 return create_response(read_html("app/templates/login.html"))
#             else :
#                 return create_response(read_html("app/templates/register.html"))
            
#         elif uri == "/submit-url":
#             return createVideoResponse(youtubeProcessing(request))
#     else:
#         return create_response(read_html("404.html"))
