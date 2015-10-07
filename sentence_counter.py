import rethinkdb as r 
from pprint import pprint

conn = r.connect("104.130.21.31")

for _ in xrange(5):
	pprint(r.db('ycsb').table('usertable').map( r.row["field0"].split(".").count() ).sum().run(conn, profile=True)['profile'][0]['duration(ms)'])
 

