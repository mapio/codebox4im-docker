from hashlib import sha256
from hmac import new as mac
from json import loads, dumps
from logging import StreamHandler, FileHandler, Formatter, INFO, getLogger
from os import environ
from subprocess import check_output, CalledProcessError
from sys import argv

from flask import Flask, abort, redirect, request

app = Flask( __name__ )

EVENTS_LOG = getLogger( 'EVENTS_LOG' )
EVENTS_LOG.setLevel( INFO )
fh = FileHandler( './var/bootstrap.events' )
fh.setLevel( INFO )
f = Formatter( '%(asctime)s: %(message)s', '%Y-%m-%d %H:%M:%S' )
fh.setFormatter( f )
EVENTS_LOG.addHandler( fh )
EVENTS_LOG.info( 'Start' )

if not 'ARBITER_SECRET' in environ:
	exit( 'No ARBITER_SECRET found in environment' )
ARBITER_SECRET = environ[ 'ARBITER_SECRET' ]

if not 'ARBITER_IP' in environ:
	exit( 'No ARBITER_IP found in environment' )
REDIRECT_URL = 'http://' + environ[ 'ARBITER_IP' ] + ':{port}/?email={uid}&token={signature}'

def _sign( uid ):
	return '{0}:{1}'.format( uid, mac( ARBITER_SECRET, uid, sha256 ).hexdigest() )

@app.route( '/' )
def index():
	uid = request.remote_addr
	return _sign( uid ), 200, { 'Content-Type': 'text/plain;charset=UTF-8' }

@app.route( '/favicon.ico' )
def favicon():
	abort( 404 )

@app.route( '/<uid_signature>' )
def spinup( uid_signature = None ):
	try:
		uid, signature = uid_signature.split( ':' )
	except ValueError:
		EVENTS_LOG.warn( 'cannot split uid_signature "{}"'.format( uid_signature ) )
		abort( 404 )
	if not uid_signature == _sign( uid ):
		EVENTS_LOG.error( 'wrong signature "{}" for uid {}"'.format( signature, uid ) )
		abort( 404 )
	try:
		output = check_output( [ './bin/rundocker', uid_signature ] )
	except CalledProcessError, e:
		EVENTS_LOG.error( 'rundocker: exit code {}'.format( e.returncode ) )
		abort( 404 )
	try:
		data = loads( output )
	except ValueError:
		EVENTS_LOG.error( 'rundocker: unparseable json "{}"'.format( output ) )
		abort( 404 )
	if not data[ 'status' ] == 'ok':
		EVENTS_LOG.error( 'rundocker: status "{}"'.format( data[ 'status' ] ) )
		abort( 404 )
	EVENTS_LOG.info( 'started container for uid "{}"'.format( uid ) )
	return redirect( REDIRECT_URL.format( port = data[ 'port' ], uid = uid, signature = signature ) )

if __name__ == "__main__":
	app.run( debug = True )
