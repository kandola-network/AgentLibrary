from newsdataapi import NewsDataApiClient
api = NewsDataApiClient(apikey='pub_63883963ee91860350581787e696120f0f6f9')
response = api.latest_api(q='What?', category='technology')
print(response['results'])

