import re
import subprocess
from traceback import format_exc

from v2ray_stats.utils import V2RayLogger


class V2Ctl(object):
    def __init__(self, server: str):
        """
        Init V2Ctl class.
        :param server: api server address.
        """
        self.server = server

    def _call_api(self, method: str, request: str) -> str:
        """
        Call v2ctl api and return parsed dict result.
        :param method: One of LoggerService.RestartLogger, StatsService.GetStats, StatsService.QueryStats
        :param request: Invalid request string
        :return: Result String
        """
        if method not in ("LoggerService.RestartLogger", "StatsService.GetStats", "StatsService.QueryStats"):
            raise Exception("Invalid method: {0}".format(method))

        assert isinstance(request, str)

        try:
            V2RayLogger.debug(["v2ctl", "api", '--server={0}'.format(self.server), method, request])
            process = subprocess.run(["v2ctl", "api", '--server={0}'.format(self.server), method, request],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as err:
            error = '{0}\n{1}\n{2}'.format(format_exc(), locals(), err.stderr.decode())
            raise Exception(error)

        V2RayLogger.debug(process.stdout.decode())
        return process.stdout.decode()

    def query_stats(self, pattern: str = "", reset: bool = False) -> list:
        """
        V2ctl StatsService.QueryStats
        :param pattern: Default is "", query pattern
        :param reset: If reset data after query, default is False
        :return: Result list
        """
        assert isinstance(pattern, str)
        assert isinstance(reset, bool)

        request = 'pattern: "{pattern}" reset: {reset}'.format(pattern=pattern, reset='true' if bool else 'false')

        output = self._call_api(method='StatsService.QueryStats', request=request)
        m = re.compile('stat: <\n {2}name: "(.*)"\n {2}value: (.*)\n>')
        result = m.findall(output)

        result_list = []
        user_m = re.compile('user>>>(.*)>>>traffic>>>(downlink|uplink)')
        system_m = re.compile('inbound>>>(.*)>>>traffic>>>(downlink|uplink)')
        for key, value in result:
            temp = user_m.findall(key)
            if temp != []:
                [(email, bound)] = temp
                temp_dict = {
                    'type': 'user',
                    'name': email,
                    'bound': bound,
                    'value': value
                }
                result_list.append(temp_dict)
                continue

            temp = system_m.findall(key)
            if temp != []:
                [(tag, bound)] = temp
                temp_dict = {
                    'type': 'system',
                    'name': tag,
                    'bound': bound,
                    'value': value
                }
                result_list.append(temp_dict)


        return result_list
