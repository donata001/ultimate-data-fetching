import facebook
from urllib2 import urlopen
from json import load

#FACEBOOK_APP-ID="683906191632398"
#FACEBOOK_APP_SECRET="7368db893aa15767f66f94921473387d"


query_list=[
"bananarepublic",
"coach",
"gap",
"burberry"
"jcrew"
]
datastore={}
base_url = 'https://graph.facebook.com/'

for query in query_list:
    url=base_url+query
    response=urlopen(url)
    js=load(response)
    name=js['name']
    likes=js['likes']
    TAC=js['talking_about_count']
    
    datastore[query]={'name':name,'likes':likes,'TAC':TAC}
data=datastore.values()
print data


