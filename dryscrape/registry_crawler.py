import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import os
import random


domains = (domain.rstrip('\n') for domain in open('my-domain-list-test.txt'))
#proxies = (proxy.rstrip('\n') for proxy in open('proxy-list.txt'))
datalist = []
proxy_list = []

#for proxy in proxies:
#    proxy_list.append(proxy)

n = 0
for domain in domains:
    n += 1
    # proxy = random.choice(proxy_list)
    # proxy.decode('utf-8')
    print(domain)
    print(n)
    # data = {
    #     'domain': domain,
    # }

    # Get the page
    # use .post
    # send the data
    # headers = requests.utils.default_headers()
    # headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    url = "https://who.is/whois/{0}".format(domain)
    # proxy = {"http": proxy, "https": proxy}
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')

    # filename = domain + '.html'
    # with open(filename, 'wb') as f:
    #     f.write(str(doc))
    grp = []
    grp.append(domain)

    for soup_contactbox in doc.find_all('div', class_='queryResponseBodyRow'):
        # print(soup_contactbox)
        # BeautifulSoup visits each Contact Box
        detail_name = []

        ctitle = soup_contactbox.find('div', 'queryResponseBodyKey')
        cvalue = soup_contactbox.find('div', 'queryResponseBodyValue')
        if ctitle and ctitle.text == 'Whois Server' and cvalue.text:
            print(ctitle.text)
            print(cvalue.text)
            grp.append(cvalue.text)
#         if ctitle:
#             grp.append(ctitle.text)
#         # for detail in soup_contactbox.find_all('td', 'cdetailsname'):
#         #     if detail:
#         #         detail_name.append(detail.text)
#         # if detail_name:
#         #     print(detail_name)
#         #     grp.append(', '.join(detail_name))
#         for cname in soup_contactbox.find_all('div', class_='df-value'):
#             if cname:
#                 grp.append(cname.text)
#         cemail = soup_contactbox.find('img')
#         if cemail:
#             grp.append(cemail['alt'])
#         # cemail_span = soup_contactbox.find('span', 'cemail')
#         # if cemail_span:
#         #     cemail = cemail_span.parent.find('a')
#         #     if cemail:
#         #         grp.append(cemail.text)
#
#
#         # Store the dataframe in a list
    datalist.append(grp)
print(datalist)
#
result = pd.concat([pd.DataFrame(datalist)], ignore_index=True)
#
# convert the pandas dataframe to JSON
json_records = result.to_json(orient='records')
#
# # pretty print to CLI with tabulate
# # converts to an ascii table
print(tabulate(result, headers=["Domain", "Server"], tablefmt='psql'))
#
# # get current working directory
path = os.getcwd()
#
# # open, write, and close the file
filename = 'webnic_test.json'
with open(filename, 'wb') as f:
    f.write(json_records)