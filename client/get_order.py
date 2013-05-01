#!/usr/bin/python

from optparse import OptionParser
import sys
import httplib

def report_error(msg):
    print msg
    exit(1)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-o', '--order', dest='order', help='ID of the order to retreive')
    parser.add_option('-s', '--server', dest='host', help='Server name/IP of the REST endpoint')
    parser.add_option('-p', '--port', dest='port', help='Port number of the REST endpoint')

    (options, args) = parser.parse_args(sys.argv)
    order = None
    host = '127.0.0.1'
    port = 8281
    if not options.order:
        report_error('Please specify the ID of the order to retrieve')
    order = options.order
    if options.host:
        host = options.host
    if options.port:
        port = int(options.port)

    conn = httplib.HTTPConnection(host + ':' + str(port))
    conn.set_debuglevel(1)
    conn.request('GET', '/order/' + order)
    response = conn.getresponse()
    output = response.read()
    print 'response:', output
    print
    if response.status == 200:
        print 'Order retrieved successfully...'
    else:
        print 'Failed to obtain the specified order'
    conn.close()
