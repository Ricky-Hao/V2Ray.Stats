import re
import subprocess
from traceback import format_exc


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
            process = subprocess.run(["v2ctl", "api", '--server={0}'.format(self.server), method, request],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as err:
            error = '{0}\n{1}\n{2}'.format(format_exc(), locals(), err.stderr.decode())
            raise Exception(error)

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
        email_m = re.compile('user>>>(.*)>>>traffic>>>(downlink|uplink)')
        for key, value in result:
            [(email, bound)] = email_m.findall(key)
            temp_dict = {
                'email': email,
                'bound': bound,
                'value': value
            }
            result_list.append(temp_dict)

        return result_list
