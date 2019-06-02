import json
import time
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")

sys.path.append("pytavia_modules/access")
from access import authentication

sys.path.append("pytavia_modules/forum")
from forum import thread

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_stdlib  import idgen 


##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
app.secret_key  = config.G_FLASK_SECRET

########################## CALLBACK API ###################################

#==================================================
#Landing
#==================================================
@app.route("/", methods=["GET"])
def index_get():
	return "<center>Hello world</center>"
#end

#==================================================
#Authentication
#==================================================
@app.route("/register", methods=["POST"])
def register_post():
	#prepare data
	params		= {
					"name"			: request.form.get('name'),
					"username"		: request.form.get('username'),
					"password"		: request.form.get('password')
				  }

	#run & return
	result		= authentication.authentication({}).register(params)
	return json.dumps(result)
#end

@app.route("/login", methods=["POST"])
def login_post():
	#prepare data
	params		= {
					"username"		: request.form.get('username'),
					"password"		: request.form.get('password')
				  }

	#run & return
	result		= authentication.authentication({}).login(params)
	return json.dumps(result)
#end

@app.route("/logout", methods=["POST"])
def logout_post():
	#prepare data
	params		= {
					"session"		: request.form.get('session')
				  }

	#run & return
	result		= authentication.authentication({}).logout(params)
	return json.dumps(result)
#end

#==================================================
#Thread
#==================================================
@app.route("/threads", methods=["POST"])
def thread_post():
	#prepare data
	params		= {
					"title"			: request.form.get('title'),
					"content"		: request.form.get('content'),
					"session"		: request.form.get('session')
				  }

	#run & return
	result		= thread.thread({}).thread_add(params)
	return json.dumps(result)
#end

@app.route("/threads/<id_thread>", methods=["GET", "PUT", "DELETE"])
def thread_all(id_thread):
	#short by method
	if request.method == 'GET':
		#prepare data
		params		= {
						"method"		: "get",
						"id_thread"		: id_thread
					  }

		result		= thread.thread({}).thread_view(params)
	elif request.method == 'PUT':
		#prepare data
		params		= {
						"method"		: "put",
						"id_thread"		: id_thread,
						"title"			: request.form.get('title'),
						"content"		: request.form.get('content'),
						"session"		: request.form.get('session')
					  }
		
		result		= thread.thread({}).thread_edit(params)
	elif request.method == 'DELETE':
		#prepare data
		params		= {
						"method"		: "delete",
						"id_thread"		: id_thread,
						"session"		: request.form.get('session')
					  }
		
		result		= thread.thread({}).thread_delete(params)
	#endif

	#return
	return json.dumps(result)
#end