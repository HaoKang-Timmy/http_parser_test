'''
Author: Beta Cat 466904389@qq.com
Date: 2022-11-30 13:57:14
LastEditors: Beta Cat 466904389@qq.com
LastEditTime: 2022-11-30 20:53:51
FilePath: /research/UW/works/test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import llhttp
from pprint import pprint
import argparse
parser = argparse.ArgumentParser(description='Propert ResNets for CIFAR10 in pytorch')
parser.add_argument('-l', '--header-length', default=10, type=int)
parser.add_argument('-n', '--number', default=100, type=int)
parser.add_argument('-i', '--input-length', default=2, type=int)
args = parser.parse_args()
pprint({"version": llhttp.version})
header_list = []
class request_parser(llhttp.Request):
    headers = {}

    url = b''
    current_header_field = None
    current_header_value = None

    def on_message_begin(self):
        print(f"MESSAGE BEGIN")

    def on_url(self, url):
        self.url += url
        self.pause()

    def on_url_complete(self):
        print(f"URL {self.url}")

    def on_header_field(self, field):
        assert self.current_header_value is None
        if self.current_header_field is None:
            self.current_header_field = bytearray(field)
        else:
            self.current_header_field += field

    def on_header_field_complete(self):
        self.current_header_field = self.current_header_field.decode('iso-8859-1').lower()
        assert self.current_header_field not in self.headers

    def on_header_value(self, value):
        assert self.current_header_field is not None
        if self.current_header_value is None:
            self.current_header_value = bytearray(value)
        else:
            self.current_header_value += value

    def on_header_value_complete(self):
        assert self.current_header_field is not None
        self.current_header_value = bytes(self.current_header_value)
        # print(f"HEADER {self.current_header_field}: {self.current_header_value}")
        self.headers[self.current_header_field] = self.current_header_value
        self.current_header_field = None
        self.current_header_value = None

    def on_headers_complete(self):
        assert self.current_header_field is None
        assert self.current_header_value is None

    def on_message_complete(self):
        print("MESSAGE COMPLETE")
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
def generate_buff(words):
    buffer = "GET /test HTTP/1.1"
    for i in range(words):
        header = randomword(args.header_length)
        
        while header in header_list:
            header = randomword(args.header_length)
        header_list.append(header)
        input = randomword(args.input_length)
        buffer= buffer + "\r\n"+header+":"+input
        # buffer.append(randomword(2)+":")
        # buffer.append(randomword(2))
    buffer = buffer + "\r\n\r\n"
    buffer = str.encode(buffer)
    # buffer = bbufer
    return buffer
        

    
parser = request_parser()

assert parser.lenient_headers is not True
parser.lenient_headers = True
parser.reset()
assert parser.lenient_headers is True
buffer = generate_buff(args.number)
# print(buffer)
# buffer = b"GET /test HTTP/1.1\r\nlOl:wut\r\nOH: hai\r\nOz: haz\r\n\r\n"
# print(buffer)
import time
start = time.time()
while buffer:
    consumed = parser.execute(buffer[:2])
    buffer = buffer[consumed:]
    if parser.is_paused:
        print("UNPAUSING")
        parser.unpause()

parser.finish()
end = time.time()
# pprint({
#     "method": parser.method,
#     "url": parser.url,
#     "version": f"{parser.major}.{parser.minor}",
#     "headers": parser.headers,
# })
print("time:",end - start)