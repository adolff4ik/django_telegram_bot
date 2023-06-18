import requests


def get_articles(api_url,params):
    api_key = "api_key"

    url = api_url + api_key

    request = requests.get(url, params=params)
    
    req_json = request.json()

    print(request.url)

    return req_json
