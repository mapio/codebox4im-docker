from hashlib import sha256
from hmac import new as mac
from json import loads, dumps
from logging import StreamHandler, FileHandler, Formatter, INFO, getLogger
from subprocess import check_output, CalledProcessError
from sys import argv

from flask import Flask, abort, redirect, request

app = Flask( __name__ )
try:
	app.config.from_envvar( 'TM_SETTINGS' )
except:
	exit( 'Error loading TM_SETTINGS, is such variable defined?' )

EVENTS_LOG = getLogger( 'EVENTS_LOG' )
EVENTS_LOG.setLevel( INFO )
fh = FileHandler( './var/bootstrap.events' )
fh.setLevel( INFO )
f = Formatter( '%(asctime)s: %(message)s', '%Y-%m-%d %H:%M:%S' )
fh.setFormatter( f )
EVENTS_LOG.addHandler( fh )
EVENTS_LOG.info( 'Start' )

if not 'SECRET_KEY' in app.config:
	exit( 'No SECRET_KEY found in TM_SETTINGS file' )

if not 'REDIRECT_URL' in app.config:
	exit( 'No REDIRECT_URL found in TM_SETTINGS file' )

def _sign( uid ):
	return '{0}:{1}'.format( uid, mac( app.config[ 'SECRET_KEY' ], uid, sha256 ).hexdigest() )

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
	return redirect( app.config[ 'REDIRECT_URL' ].format( port = data[ 'port' ], uid = uid, signature = signature ) )

if __name__ == "__main__":
	app.run( debug = True )
