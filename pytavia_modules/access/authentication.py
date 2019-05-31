import sys
import json
import hashlib, random, string, datetime
import pymongo

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")

from pytavia_core import database
from pytavia_core import config
from bson import json_util, ObjectId


class authentication:

	#set connection to mongo
	dbsample	= database.get_db_conn(config.mainDB)


	#construct
	def __init__(self, params):
		pass
	#end


	#==================================================
	#Public Function
	#==================================================
	def register(self, params):
		#additional params
		params['salt']	= self._generate_salt()

		#checking user
		info_user		= self._get_user_by_username(params['username'])

		if (info_user is not None):
			return {"status" : 0, "message" : 'username already taken'}
		#endif
		
		#save data user
		user_add 		= database.new(self.dbsample, "t_user")
		user_add.put("name", params['name'])
		user_add.put("username", params['username'])
		user_add.put("salt", params['salt'])
		user_add.put("password", self._generate_password(params['salt'], params['password']))
		user_add.insert()

		return {"status" : 1, "message" : 'username successfully inserted'}
	#end

	def login(self, params):
		#checking user
		info_user		= self._get_user_by_username(params['username'])
		# return info_user['pkey']
		
		if (info_user is None):
			return {"status" : 0, "message" : 'you shall not pass'}
		#endif

		if (info_user['password'] != self._generate_password(info_user['salt'], params['password'])):
			return {"status" : 0, "message" : 'you shall not pass'}
		#endif
		
		#prepare data
		session			= self._generate_session()
		query			= {"username": params['username']}
		new_values		= {"$set": { "session": session }}
		
		#update data user
		myclient		= pymongo.MongoClient("mongodb://localhost:27017/")
		mydb			= myclient["dbsample"]
		mycol			= mydb["t_user"]
		mycol.update_one(query, new_values)

		return {"status" : 1, "message" : 'the floor is yours', 'session' : session}
	#end

	
	#==================================================
	#Private Function
	#==================================================
	def _get_user_by_username(self, username):
		info_user		= self.dbsample.t_user.find_one({"username": username})
		info_user		= json.loads(json_util.dumps(info_user))
		return info_user
	#end

	def _generate_salt(self):
		letters			= string.ascii_letters + string.digits + string.punctuation
		return ''.join(random.choice(letters) for i in range(5))
	#end

	def _generate_password(self, salt, password):
		return hashlib.sha256(str(password + salt + password).encode('utf-8')).hexdigest()
	#end

	def _generate_session(self):
		return hashlib.sha256(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
	#end