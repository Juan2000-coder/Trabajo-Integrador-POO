import http.client

request_body = b"<?xml version='1.0'?>\n<methodCall>\n<methodName>status</methodName>\n</methodCall>\n"
#request_body = b"<?xml version='1.0'?>\n<methodCall>\n<methodName>list</methodName>\n<params>\n<param>\n<value><int>55</int></value>\n</param>\n</params>\n</methodCall>\n"

connection = http.client.HTTPConnection('localhost:8891')
connection.putrequest('POST', '/')
connection.putheader('Content-Type', 'text/xml')
#connection.putheader('User-Agent', 'Python-xmlrpc/3.9') # si se coloca debe ser exacto
connection.putheader("Content-Length", str(len(request_body)))
connection.endheaders(request_body)
    
print(connection.getresponse().read())

