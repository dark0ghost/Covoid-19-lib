# Covoid-19-lib
__lib implementing__ [app](https://coronavirus-19-api.herokuapp.com/) __api__
# python
[implement](https://github.com/dark0ghost/Covoid-19-lib/tree/master/python/src)
# python use
```python
from python.src import NoCacheCoVoidAPI
# or 
from python.src import WithCacheCoVoidApi

async def main():
   session = aiohttp.ClientSession() # optional
   co_void19_ncov_2 = NoCacheCoVoidAPI(session)
   #or 
    co_void19_ncov_2  =  WithCacheCoVoidAPI(session)
    print(awit co_void19_ncov_2.get_full_data())
    # print tuple with all data
    print(awit co_void19_ncov_2.get_data_country())
    # printed data for need country
    
```
# python dep
aiohttp>=3.6
python>=3.7
