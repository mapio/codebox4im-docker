from hashlib import sha256
from hmac import new as mac
from json import loads, dumps
from logging import StreamHandler, FileHandler, Formatter, INFO, DEBUG, getLogger
from os import environ
from subprocess import Popen, PIPE
from sys import argv

from flask import Flask, abort, redirect, request

app = Flask( __name__ )

EVENTS_LOG = getLogger( 'EVENTS_LOG' )
EVENTS_LOG.setLevel( DEBUG )
fh = FileHandler( './var/bootstrap.events' )
fh.setLevel( DEBUG )
f = Formatter( '%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S' )
fh.setFormatter( f )
EVENTS_LOG.addHandler( fh )
EVENTS_LOG.info( 'Start' )

if not 'ARBITER_SECRET' in environ:
	exit( 'No ARBITER_SECRET found in environment' )
ARBITER_SECRET = environ[ 'ARBITER_SECRET' ]

if not 'ARBITER_ADDRESS' in environ:
	exit( 'No ARBITER_ADDRESS found in environment' )
REDIRECT_URL = 'http://' + environ[ 'ARBITER_ADDRESS' ] + ':{port}/?email={uid}&token={signature}'

def _sign( uid ):
	return '{0}:{1}'.format( uid, mac( ARBITER_SECRET, uid, sha256 ).hexdigest() )

@app.route( '/', methods = [ 'GET', 'POST' ] )
def index():
	if 'uid' in request.form:
		uid = request.form[ 'uid' ]
	else:
		uid = request.remote_addr
	EVENTS_LOG.info( 'Returning signed pair to uid "{}"'.format( uid ) )
	return _sign( uid ), 200, { 'Content-Type': 'text/plain;charset=UTF-8' }

@app.route( '/favicon.ico' )
def favicon():
	abort( 404 )

@app.route( '/<uid_signature>' )
def spinup( uid_signature = None ):

	try:
		uid, signature = uid_signature.split( ':' )
	except ValueError:
		EVENTS_LOG.warn( 'Cannot split uid_signature "{}"'.format( uid_signature ) )
		abort( 404 )
	if not uid_signature == _sign( uid ):
		EVENTS_LOG.error( 'Wrong signature "{}" for uid "{}"'.format( signature, uid ) )
		abort( 404 )

	popen = Popen( [ './bin/runworker', uid_signature ], stdout = PIPE, stderr = PIPE )
	output, perror = popen.communicate()
	if popen.returncode != 0:
		EVENTS_LOG.error( 'runworker: exit code {}'.format( popen.returncode ) )
		EVENTS_LOG.debug( 'runworker: stdout...\n{}'.format( output ) )
		EVENTS_LOG.debug( 'runworker: stderr...\n{}'.format( perror ) )
		abort( 404 )

	try:
		data = loads( output )
	except ValueError:
		EVENTS_LOG.error( 'runworker: unparseable json "{}"'.format( output ) )
		abort( 404 )
	if not data[ 'status' ] == 'ok':
		EVENTS_LOG.error( 'runworker: status "{}"'.format( data[ 'status' ] ) )
		abort( 404 )
	EVENTS_LOG.info( 'Started container for uid "{}"'.format( uid ) )

	return redirect( REDIRECT_URL.format( port = data[ 'port' ], uid = uid, signature = signature ) )

if __name__ == "__main__":
	app.run( debug = True )
