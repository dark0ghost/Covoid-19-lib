import asyncio
import typing

import aiohttp

try:
    import ujson as json
except ImportError:
    import json


class BaseInterfaceCoVoid:
    all_data_url: str = "https://coronavirus-19-api.herokuapp.com/all"
    endpoint_data_url: str = "https://coronavirus-19-api.herokuapp.com/countries"

    def __init__(self, session: typing.Optional[aiohttp.ClientSession] = None,
                 loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> None:
        """
        :param session:
        """

        self.cache_list = list()
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.new_event_loop()
        if session:
            self.session = session
        else:
            self.session = aiohttp.ClientSession()

    def __str__(self) -> str:
        """
        :return:
        """
        return f"{self.__class__.__name__}(cache: {hash(self.cache)})"

    def __hash__(self) -> int:
        """

        :return:
        """
        return hash(self.cache) ^ hash(self.loop) and hash(self.session)

    def __del__(self) -> None:
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

    async def get_all_data(self) -> typing.Dict[str, typing.Any]:
        pass

    async def get_endpoint_data(self) -> typing.Dict[str, typing.Any]:
        pass

    async def get_full_data(self) -> typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, typing.Any]]:
        pass

    async def get_data_country(self, name: str):
        pass

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
