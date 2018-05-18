# -*- coding: utf-8 -*-
import json

from codec.decoder import get_response_body_length, Response
from codec.encoder import encode
from connection.connections import connection


class DubboClient(object):
    class _Method(object):
        def __init__(self, client_instance, method):
            self.client_instance = client_instance
            self.method = method

        def __call__(self, *args, **kwargs):
            return self.client_instance.call(self.method, *args, **kwargs)

    def __init__(self, interface, version='1.0.0', dubbo_version='2.4.10'):
        self.interface = interface
        self.version = version
        self.dubbo_version = dubbo_version

    def __getattr__(self, method, *args, **kwargs):
        return self._Method(client_instance=self, method=method)

    def call(self, method, *args):
        client = connection.get_connection(self.interface)

        request_param = {
            'dubbo_version': self.dubbo_version,
            'version': self.version,
            'path': self.interface,
            'method': method,
            'arguments': args
        }
        request = encode(request_param)
        client.write(request)

        # 响应数据的头部大小为16个字节
        response_head = client.read(16)
        response_body_length = get_response_body_length(response_head)

        response_body = client.read(response_body_length)
        res = Response(response_body)
        res.read_int()  # 响应的状态
        return res.read_next()


def pretty_print(value):
    print json.dumps(value, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == '__main__':
    dubbo = DubboClient('me.hourui.echo.provider.Echo')
    pretty_print(dubbo.echo('张老师', '三', 19, 2000.0, True))
    pretty_print(dubbo.echo1('昊天金阙无上至尊自然妙有弥罗至真高天上圣大慈仁者玉皇赦罪锡福大天尊玄穹高上帝'))
    pretty_print(dubbo.echo2(False))
    pretty_print(dubbo.echo3(1000000000, 0x7ff, 100000, 10000))
    pretty_print(dubbo.echo4(1.00000004, 100000.0, 1.0, 2.0, 0.0))
    assert 200 == dubbo.echo5(200)
    assert 10000 == dubbo.echo5(10000)

    assert 0.0 == dubbo.echo6(0.0)
    assert 1.0 == dubbo.echo6(1.0)
    assert 100.0 == dubbo.echo6(100.0)
    assert 100000.0 == dubbo.echo6(100000.0)

    assert 10000000000 == dubbo.echo7(10000000000)
    assert 0 == dubbo.echo7(0)
    assert 100 == dubbo.echo7(100)
    assert 1000 == dubbo.echo7(1000)
    assert 100000 == dubbo.echo7(100000)

    pretty_print(dubbo.echo8())
    pretty_print(dubbo.echo9())
    pretty_print(dubbo.echo10())
    pretty_print(dubbo.echo11())
    pretty_print(dubbo.echo12())
    pretty_print(dubbo.echo13())
    pretty_print(dubbo.echo14())
    pretty_print(dubbo.echo15())
    pretty_print(dubbo.echo16())
