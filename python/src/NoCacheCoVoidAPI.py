import typing

from python.src.base.BaseClassCoVoid import BaseClassCoVoid

try:
    import ujson as json
except ImportError:
    import json


class NoCacheCoVoidAPI(BaseClassCoVoid):


    async def get_all_data(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
         get full data
        :return:
        """
        async with self.session.get(url=self.all_data_url) as response:
            return await response.json()

    async def get_endpoint_data(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        get endpoint data
        :return:
        """
        async with self.session.get(url=self.endpoint_data_url) as response:
            return await response.json()

    async def get_full_data(self) -> typing.Tuple[
        typing.List[typing.Dict[str, typing.Any]], typing.List[typing.Dict[str, typing.Any]]]:
        """
        return tuple with full and enpoint daata
        :return:
        """
        response_all = await self.get_all_data()
        response_endpoint = await self.get_endpoint_data()

        return response_all, response_endpoint

    async def get_data_country(self, name: str) -> typing.Optional[typing.Dict[str, typing.Any]]:
        response: typing.List[typing.Dict[str, typing.Any]] = await self.get_endpoint_data()
        for i in response:
            if i["country"] == name:
                return i
        else:
            return None


