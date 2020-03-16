import aiohttp
import typing
import asyncio

try:
    import ujson as json
except ImportError:
    import json


class CoVoidAPI:
    cache_list: typing.List[typing.Dict[str, str]]

    cache_mode: bool

    loop: asyncio.AbstractEventLoop

    all_data_url: str = "https://coronavirus-19-api.herokuapp.com/all"

    endpoint_data_url: str = "https://coronavirus-19-api.herokuapp.com/countries"

    cache_dict: typing.Dict

    def __init__(self, session: typing.Optional[aiohttp.ClientSession] = None, cache: bool = True,
                 loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> None:
        """

        :param session:
        :param cache:
        """
        self.cache_mode = cache
        if self.cache_mode:
            self.cache_list = list()
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.new_event_loop()
        if session:
            self.session = session
        else:
            self.loop.run_until_complete(self.create_session())

    def __str__(self) -> str:
        """

        :return:
        """
        return f"{self.__class__.__name__}(cache: {hash(self.cache_mode)})"

    def __hash__(self) -> int:
        """

        :return:
        """
        return hash(self.cache_mode) ^ hash(self.loop) and hash(self.session)

    def __del__(self):
        """

        :return:
        """
        self.loop.run_until_complete(self.session.close())

    def close(self) -> bool:
        """

        :return:
        """
        self.__del__()
        try:
            self.cache_list.clear()
        except AttributeError:
            pass
        return True

    class NoCacheModeError(Exception):
        pass

    async def create_session(self) -> None:
        self.session = aiohttp.ClientSession()

    async def get_all_data(self) -> typing.Dict[str, typing.Any]:
        """

        :return:
        """
        async with self.session.get(url=self.all_data_url) as response:
            js = await response.json()
            if self.cache_mode:
                self.cache_list.append(js)
            return js

    async def get_endpoint_data(self) -> typing.Dict[str, typing.Any]:
        """

        :return:
        """
        async with self.session.get(url=self.endpoint_data_url) as response:
            js = await response.json()
            if self.cache_mode:
                self.cache_list.append(js)
                self.cache_dict = js
            return js

    async def get_full_data(self) -> typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, typing.Any]]:
        """

        :return:
        """
        response_all = await self.get_all_data()
        response_endpoint = await self.get_endpoint_data()

        return response_all, response_endpoint

    async def read_json(self, all_data: bool = False, endpoint_data: bool = False,
                        js: typing.Optional[typing.Dict] = None, indent: int = 4):
        """

        :param all_data:
        :param endpoint_data:
        :param js:
        :param indent:
        :return:
        """
        if js and all_data and endpoint_data:
            return json.dumps({
                "response": js,
                "all": await self.get_all_data(),
                "endpoint": await self.get_endpoint_data()
            }, ensure_ascii=False, indent=indent)

        if js:
            return json.dumps(js, ensure_ascii=False, indent=indent)
        if all_data and endpoint_data:
            return json.dumps({
                "all": await self.get_all_data(),
                "endpoint": await self.get_endpoint_data()
            }, ensure_ascii=False, indent=indent)
        if all_data:
            return json.dumps(await self.get_all_data(), ensure_ascii=False, indent=indent)
        if endpoint_data:
            return json.dumps(await self.get_endpoint_data(), ensure_ascii=False, indent=indent)

    def get_data_country(self, name: str, use_cache: bool = False):
        if not use_cache:
            async def get_data(self):
                response = await self.get_endpoint_data()
                return response[name]

            return self.loop.run_until_complete(get_data(self))
        if self.cache_mode:
            for i in self.cache_dict:
                if i["country"] == name:
                    return i
            else:
                    raise NameError("this name not in list")
        raise self.NoCacheModeError("to use cache include it in init")


