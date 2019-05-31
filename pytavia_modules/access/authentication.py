import sys
import hashlib
import random, string

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" )

from pytavia_core import database
from pytavia_core import config

class authentication:

	#set connection to mongo
	dbsample	= database.get_db_conn(config.mainDB)


	#construct
	def __init__(self, params):
		pass
	#end


	#public
	def register(self, params):
		#additional params
		params['salt']	= self._generate_salt()

		#checking user
		if (self._is_username_exist(params) is 0):
			user_add = database.new(self.dbsample, "t_user")
			user_add.put("name", params['name'])
			user_add.put("username", params['username'])
			user_add.put("salt", params['salt'])
			user_add.put("password", self._encode_password(params['salt'], params['password']))
			user_add.insert()

			result		= {
							"status"		: 1,
							"message"		: 'username successfully inserted'
						  }
		else:
			result		= {
							"status"		: 0,
							"message"		: 'username already taken'
						  }
		#endif

		#return
		return result
	#end


	#private
	def _is_username_exist(self, params):
		#get user
		count_user	= self.dbsample.t_user.find({"username": params['username']}).count()
		if (count_user > 0):
			return 1
		else:
			return 0
		#endif
	#end

	def _generate_salt(self):
		letters		= string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(5))
	#end

	def _encode_password(self, salt, password):
		return hashlib.sha256(str(password+salt+password).encode('utf-8')).hexdigest()
	#end