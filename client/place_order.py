#!/usr/bin/python

from optparse import OptionParser
import sys
import httplib

def report_error(msg):
    print msg
    exit(1)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--drink', dest='drink', help='Name of the drink to order')
    parser.add_option('-a', '--additions', dest='additions', help='Any additions to be included in the drink')
    parser.add_option('-s', '--server', dest='host', help='Server name/IP of the REST endpoint')
    parser.add_option('-p', '--port', dest='port', help='Port number of the REST endpoint')

    (options, args) = parser.parse_args(sys.argv)
    drink = None
    additions = None
    host = '127.0.0.1'
    port = 8281
    if not options.drink:
        report_error('Please specify the name of the drink to order')
    drink = options.drink
    if options.additions:
        additions = options.additions
    if options.host:
        host = options.host
    if options.port:
        port = int(options.port)

    conn = httplib.HTTPConnection(host + ':' + str(port))
    conn.set_debuglevel(1)
    drink_payload = '<drink>{0}</drink>'.format(drink)
    additions_payload = ''
    if additions is not None and additions != '':
        additions_payload = '<additions>{0}</additions>'.format(additions)
    payload = '<order xmlns="http://starbucks.example.org">{0}{1}</order>'.format(drink_payload, additions_payload)
    headers = { 'Content-type' : 'application/xml' }
    conn.request('POST', '/order', payload, headers)
    response = conn.getresponse()
    output = response.read()
    print 'response:', output
    print
    if response.status == 201:
        print 'Order submitted successfully...'
        response_headers = {}
        for header in response.getheaders():
            response_headers[header[0]] = header[1]
        print 'Your order can be reviewed at: ', response_headers['location']
    else:
        print 'Failed to submit the order'
    conn.close()
