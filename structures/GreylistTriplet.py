from Structure import *

class GreylistTriplet(Structure):

	def __init__(self, env):
		r"""
		Initialize a GreylistTriplet object.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'Network': fp(
				title='Network',
				dbName='Network',
				dbPrimaryKey=True,
				maxlength=11,
			),
			'FromAddress': fp(
				title='From Address',
				dbName='FromAddress',
				dbPrimaryKey=True,
				maxlength=444,
			),
			'ToAddress': fp(
				title='To Address',
				dbName='ToAddress',
				dbPrimaryKey=True,
				maxlength=444,
			),
			'AcceptTime': fp(
				type='date',
				title='Accept Time',
				dbName='AcceptTime',
			),
			'ExpireTime': fp(
				type='date',
				title='Expire Time',
				dbName='ExpireTime',
			),
		}

		self.fieldOrder = (
			'Network',
			'FromAddress',
			'ToAddress',
			'AcceptTime',
			'ExpireTime',
		)

		Structure.__init__(self,
		                   'Greylist',
		                   'GreylistTriplet',
		                   'Greylist Triplet',
		                   'Greylist Triplets')

		if env != None and env.configGreylistTriplet:
			env.configGreylistTriplet(self)

		self.buildFields()

	def CheckGreylist(env, relayAddress, fromAddress, toAddress):
		r"""
		Check a triplet against the database.

		This method checks a triplet against the database. If it is
		already in the database, the @c AcceptTime is checked. If the
		current time is past the @c AcceptTime, this function will
		return true. Otherwise, this function will return false. Also,
		a greylist entry will be created with the @c AcceptTime set in
		the future.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param network     The IP address of the relay which is
		                   attempting to send the message.
		@param fromAddress The SMTP envelope sender address.
		@param toAddress   The SMTP recipient address.

		@return A boolean indicating if the message should be allowed
		        through.
		"""

		sql = 'EXECUTE "CheckGreylist" ?, ?, ?'
		args = [relayAddress, fromAddress, toAddress]

		cur = env.con.cursor()
		util.CursorWrapper.CursorWrapper.execute(cur, sql, args)

		row = cur.fetchone()
		cur.close()
		if row[0]:
			return True
		else:
			return False
	CheckGreylist = staticmethod(CheckGreylist)
