from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from settings import config

class BaseTable(Model):
    class Meta:
        host = "http://localhost:8000" ## hardcoded for dev purposes

class UrlMapping(BaseTable):
    class Meta:
        table_name = "urlMapping"

    ## hash_key is the primary key
    s_url = UnicodeAttribute(hash_key=True)
    l_url = UnicodeAttribute()
    
