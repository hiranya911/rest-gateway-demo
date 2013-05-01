#!/usr/bin/python

from optparse import OptionParser
import sys
import httplib

def report_error(msg):
    print msg
    exit(1)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--format', dest='format', help='Output content type')
    parser.add_option('-s', '--server', dest='host', help='Server name/IP of the REST endpoint')
    parser.add_option('-p', '--port', dest='port', help='Port number of the REST endpoint')

    (options, args) = parser.parse_args(sys.argv)
    format = 'application/atom+xml'
    host = '127.0.0.1'
    port = 8281
    if options.format:
        format = options.format
    if options.host:
        host = options.host
    if options.port:
        port = int(options.port)

    conn = httplib.HTTPConnection(host + ':' + str(port))
    conn.set_debuglevel(1)
    headers = { 'Accept' : format }
    conn.request('GET', '/orders', headers=headers)
    response = conn.getresponse()
    output = response.read()
    print 'response:', output
    print
    if response.status == 200:
        print 'Order list retrieved successfully...'
    else:
        print 'Failed to obtain the order list'
    conn.close()
