def hello_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [bytes('\r\n'.join(environ['QUERY_STRING'].split('&')), encoding="utf8")]

#def hello_app(environ, start_response):
#    body = [bytes(i + '\n', 'ascii') for i in environ['QUERY_STRING'].split('&')]
#    response_string = [('Content-type', 'text/plain')]
#    start_response('200 OK', response_string)
#    return body

#def hello_app(environ, start_response):
#    q_string = environ.get('QUERY_STRING')
#    pairs_list = q_string.split("&")
#    body = ""
#    for pair in pairs_list:
#        body += pair + "\n"
#    response_string = [('Content-type', 'text/plain')]
#    start_response('200 OK', response_string)
#    return [body.strip()]