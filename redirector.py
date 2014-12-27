from json import loads, dumps
from subprocess import check_output

from flask import Flask, abort, redirect

REDIRECT_IP = '192.168.59.103'

app = Flask( __name__ )

@app.route( '/<user_key>' )
def spinup( user_key ):
	try:
		user, key = user_key.split( ':' )
		data = loads( check_output( [ './run', user_key ] ) )
	except ValueError:
		abort( 404 )
	return redirect( 'http://{}:{}/?email={}&token={}'.format( REDIRECT_IP, data[ 'port' ], user, key ) )

if __name__ == "__main__":
	app.run( debug = True )
