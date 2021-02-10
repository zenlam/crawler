from subprocess import Popen, PIPE
import json
import requests

# subprocess.call("php /home/zen/PhpstormProjects/cPanel_Scripting/dns_api.php")

# user = 'zen1234'
# password = 'lamyanli123'
# dict = {
#     'user': 'zen123',
#     'password': 'lamyanli123'
# }
#
#
user = 'pilotrun'
proc = Popen(['php', '/home/zen/PhpstormProjects/cPanel_Scripting/dns_api.php', user], stdout=PIPE)
script_response = proc.stdout.read()
print(script_response.decode("utf-8"))


# url = 'http://customer.pivotino.com/cpanel_api.php'
# data = [('1','aaaaaaa')]
#
# respond = requests.post(url, data=data)
# print('----------------->',respond.text)

