import typing

from python.src.base.BaseClassCoVoid import BaseClassCoVoid


class WithCacheCoVoidApi(BaseClassCoVoid):

    cache_list: typing.List[typing.Dict[str, typing.Any]] = list()

    async def get_all_data(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        get full data
        :return:
        """
        async with self.session.get(url=self.all_data_url) as response:
            js = await response.json()
            self.cache_list.append(js)
            return js

    async def get_endpoint_data(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        get endpoint data
        :return:
        """
        async with self.session.get(url=self.endpoint_data_url) as response:
            js = await response.json()
            self.cache_list.append(js)
            return js

    async def get_full_data(self) -> typing.Tuple[
        typing.List[typing.Dict[str, typing.Any]], typing.List[typing.Dict[str, typing.Any]]]:
        """
        return tuple with full and enpoint daata
        :return:
        """
        response_all = await self.get_all_data()
        response_endpoint = await self.get_endpoint_data()

        return response_all, response_endpoint

    def get_data_country(self, name: str) -> typing.Optional[typing.Dict[str, typing.Any]]:
        response: typing.List[typing.Dict[str, typing.Any]] = self.cache_list[-1]
        for i in response:
            if i["country"] == name:
                return i
        else:
            return None

    async def close(self) -> bool:
        """

        :return:
        """
        await self.session.close()
        try:
            self.cache_list.clear()
        except AttributeError:
            pass
        return True


