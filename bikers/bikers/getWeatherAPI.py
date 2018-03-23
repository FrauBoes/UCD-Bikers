import urllib.request,urllib.parse,json

def weatherbroadcast():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.description from weather.forecast where woeid=560743"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&u=c&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    res=data['query']['results']['channel']['item']['description'].replace("<![CDATA[","").replace("]]>","").replace("\n","")
    return res