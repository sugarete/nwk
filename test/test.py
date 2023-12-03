str = """POST / HTTP/1.1
Host: 192.168.1.6:8080
Connection: keep-alive
Content-Length: 29
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://192.168.1.6:8080
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.1.6:8080/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
dnt: 1
sec-gpc: 1

username=admin&password=admin"""

print(str.splitlines()[-1])

# GET / HTTP/1.1
# Host: 192.168.1.4:8080
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9
# dnt: 1
# sec-gpc: 1