from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import tables
import settings
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import Body
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ['*'] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/create")
# def create(long_url: str = Body(..., embed=True)):
async def create(request: Request):

    long_url = await request.json()
    # the long_url is the URL that the user wants to shorten
    # we use md5 hashing to generate a unique hash for the URL
    # we save the hash and the URL in the database
    short_url = hashlib.md5(long_url["longUrl"].encode()).hexdigest()
    # store in db the short_url and long_url as key-value pair
    tables.UrlMapping.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    # take first 7 characters of hash as short_url
    # if it already exists in db, increment by 1 character until unique
    for i in range(7, len(short_url)):
        try:
            tables.UrlMapping.get(short_url[:i])
        except tables.UrlMapping.DoesNotExist:
            short_url = short_url[:i]
            break

    new_mapping = tables.UrlMapping(s_url=short_url, l_url=long_url["longUrl"])
    new_mapping.save()

    return {"shortenedUrl": short_url}


@app.get("/{short_url}")
def retrieve(short_url):
    # query db to find mapping
    try:
        mapping = tables.UrlMapping.get(short_url)
        # redirect to the long_url
        return RedirectResponse(mapping.l_url)
    except tables.UrlMapping.DoesNotExist:
        return {"message": "Resource not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)