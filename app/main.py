from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError

from app.data import RedisWrapper, load_results_data

app = FastAPI()

class StringRequest(BaseModel):
    """
    schema for incoming requests.
    Unexpected fields will be ignored.
    """
    searchString: str = None

def featurize_request(search_string):
    """
    logic for featurizing query
    """
    #featurize logic here
    return search_string

def lookup_results(featurized, results_data):
    """
    performs results lookup.
    """
    msg = ("performing lookup for key: search_key={search_key}".
                    format(search_key=featurized))

    results = results_data.get(featurized, default='[]')
    #parse string result
    results = eval(results)
    msg = ("{n_results} found for key {search_key}".
                    format(n_results=len(results), search_key=featurized))
    return results

def structure_results(results):
    """
    logic to structure response
    """
    #posproc logic here

    return results

__featurizer = Featurizer()
__searchStringKey = "searchString"
__results_data = load_results_data()

@app.post("/ml_search")
async def get_reponse(request: StringRequest):
    """
    Handles request for results.
    Input request (StringRequest): ref to json body.
    output output (string): json-encoded response.
    """
    request_dict = request.dict()
    search_string = request_dict[__searchStringKey]
    if search_string is None:
        raise HTTPException(400, 'Missing required field: searchString')

    featurized = featurize_request(search_string)
    results = lookup_results(featurized, __results_data)
    results = structure_results(results)

    output = jsonable_encoder({
        'search_key': featurized,
        'results': str(results)
    })

    return output

@app.get("/healthcheck")
async def healthcheck():
    """
    Test to see if server is responive.
    Returns code 200, {'status':'ok'}
    """
    return jsonable_encoder({
        'status': 'ok'
    })
