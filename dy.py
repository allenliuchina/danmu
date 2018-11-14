import socket
import re


class Msg(object):
    def __init__(self, code=689, **kwargs):
        self.dict = {}
        self.dict.update(**kwargs)
        self.code = code
        self.msg = ''
        self.pack()
        # 第一个信息长度不计入总长度
        self.len = len(self.msg.encode()) + 8
        self.msg_end = int.to_bytes(self.len, 4, 'little') + int.to_bytes(self.len, 4, 'little') + \
                       int.to_bytes(code, 4, 'little') + self.msg.encode()

    def pack(self):
        for k, v in self.dict.items():
            self.msg += k + '@=' + v + '/'
        self.msg += '\0'

    def send(self, sk):
        sk.send(self.msg_end)


def danmu():
    room_id = input('输入房间号： ')
    # 斗鱼接口改变，无法正常发送keep_live信息
    keep_live = Msg(type='mrkl')
    login = Msg(type='loginreq', room_id=room_id)
    join_room = Msg(type='joingroup', rid=room_id, gid='-9999')
    msg_re = re.compile(b'txt@=(.+?)/cid@')
    sk = socket.socket()
    sk.connect(("openbarrage.douyutv.com", 8601))
    login.send(sk)
    join_room.send(sk)
    while True:
        recive_msg = sk.recv(1024)
        msg = msg_re.findall(recive_msg)
        for m in msg:
            print(m.decode())


if __name__ == '__main__':
    danmu()
