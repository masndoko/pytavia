import sys
import json
import datetime
import pymongo

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")

from pytavia_core import database
from pytavia_core import config
from bson import json_util, ObjectId


class thread:

	#set connection to mongo
	dbsample	= database.get_db_conn(config.mainDB)


	#construct
	def __init__(self, params):
		pass
	#end


	#==================================================
	#Public Function
	#==================================================
	def thread_add(self, params):
		#validation
		required_param	= ['title', 'content', 'session']
		validation		= self._validation_params(required_param, params)
		if (validation is not None):
			return {'status' : False, 'message' : validation['message']}
		#end

		try:
			#get info user
			info_user		= self._get_user_by_session(params['session'])
			if (info_user is None):
				return {'status' : False, 'message' : 'You shall not pass'}
			#endif
			
			#save data thread
			thread_add 		= database.new(self.dbsample, 't_thread')
			thread_add.put('title', params['title'])
			thread_add.put('content', params['content'])
			thread_add.put('creator', info_user['pkey'])
			thread_add.insert()
			
			#return
			return {'status' : True, 'message' : 'Thread successfully created'}
		
		except:
			return {'status' : False, 'message' : 'Something went wrong, be hold...'}
		#endtry
	#end

	def thread_view(self, params):
		#validation
		required_param	= ['id_thread']
		validation		= self._validation_params(required_param, params)
		if (validation is not None):
			return {'status' : False, 'message' : validation['message']}
		#end

		try:
			#get info thread
			info_thread		= self._get_thread_by_id(params['id_thread'])
			if (info_thread is None):
				return {'status' : False, 'message' : 'You seek the wrong thread'}
			#endif
			
			#return
			return {'status' : True, 'message' : 'Thread successfully created', 'data' : info_thread}
		
		except:
			return {'status' : False, 'message' : 'Something went wrong, be hold...'}
		#endtry
	#end

	def thread_edit(self, params):
		#validation
		required_param	= ['id_thread', 'session']
		validation		= self._validation_params(required_param, params)
		if (validation is not None):
			return {'status' : False, 'message' : validation['message']}
		#end

		try:
			#get info user
			info_user		= self._get_user_by_session(params['session'])
			if (info_user is None):
				return {'status' : False, 'message' : 'You shall not pass'}
			#endif

			#get info thread
			info_thread		= self._get_thread_by_id(params['id_thread'])
			if (info_thread is None):
				return {'status' : False, 'message' : 'You seek the wrong thread'}
			#endif

			#is thread creator?
			if (info_user['pkey'] != info_thread['creator']):
				return {'status' : False, 'message' : 'Only creator can modify thread'}
			#endif

			#update data user
			title			= info_thread['title'] if (len(params['title']) == 0) else params['title']
			content			= info_thread['content'] if (len(params['content']) == 0) else	params['content']

			query			= {'_id': ObjectId(params['id_thread'])}
			new_values		= {'$set': {'title': title, 'content': content}}
			
			myclient		= pymongo.MongoClient('mongodb://localhost:27017/')
			mydb			= myclient['dbsample']
			mycol			= mydb['t_thread']
			mycol.update_one(query, new_values)

			#return
			return {'status' : True, 'message' : 'Thread successfully updated'}
		
		except:
			return {'status' : False, 'message' : 'Something went wrong, be hold...'}
		#endtry
	#end

	def thread_delete(self, params):
		#validation
		required_param	= ['id_thread', 'session']
		validation		= self._validation_params(required_param, params)
		if (validation is not None):
			return {'status' : False, 'message' : validation['message']}
		#end

		try:
			#get info user
			info_user		= self._get_user_by_session(params['session'])
			if (info_user is None):
				return {'status' : False, 'message' : 'You shall not pass'}
			#endif

			#get info thread
			info_thread		= self._get_thread_by_id(params['id_thread'])
			if (info_thread is None):
				return {'status' : False, 'message' : 'You seek the wrong thread'}
			#endif

			#delete data thread
			thread_delete 	= database.new(self.dbsample, 't_thread')
			thread_delete.delete({'_id': ObjectId(params['id_thread'])})
			
			#return
			return {'status' : True, 'message' : 'Thread successfully deleted'}
		
		except:
			return {'status' : False, 'message' : 'Something went wrong, be hold...'}
		#endtry
	#end

	
	#==================================================
	#Private Function
	#==================================================
	def _validation_params(self, required_param, params):
		#checking required_param
		for field in required_param:
			if (len(params[field]) == 0):
				return {'status' : False, 'message' : 'Field [' + field + '] is required'}
			#endif
		#endfor
	#end

	def _get_user_by_session(self, session):
		info_user		= self.dbsample.t_user.find_one({'session': session})
		info_user		= json.loads(json_util.dumps(info_user))
		return info_user
	#end

	def _get_thread_by_id(self, id_thread):
		info_thread		= self.dbsample.t_thread.find_one({'_id': ObjectId(id_thread)})
		info_thread		= json.loads(json_util.dumps(info_thread))
		return info_thread
	#end