import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import numpy
import urllib
import cv2
import os
import re
from io import BytesIO
import pytesseract
from PIL import Image
from pytesseract import image_to_string


domains = (domain.rstrip('\n') for domain in open('my-domain-list-test.txt'))
# proxies = (proxy.rstrip('\n') for proxy in open('proxy-list.txt'))
datalist = []
proxy_list = []

# for proxy in proxies:
#     proxy_list.append(proxy)

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
    # time.sleep(5)
    url = "https://who.is/whois/{0}".format(domain)
    # proxy = {"http": proxy, "https": proxy}
    response = requests.post(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    # print(doc)

    filename = domain + '.html'
    save_path = '/home/ubuntu/html'
    completeName = os.path.join(save_path, filename)
    with open(completeName, 'wb') as f:
        f.write(str(doc))

    for soup_contactbox in doc.find_all('div', class_='queryResponseContainer'):
        # print(soup_contactbox)
        # detail_name = []
        #
        ctitle = soup_contactbox.find('div', 'queryResponseBodyKey')
        cvalue = soup_contactbox.find('div', 'col-md-8 queryResponseBodyValue')
        craw = soup_contactbox.find('div', 'rawWhois')
        cname_server = soup_contactbox.findAll('a', href=re.compile('^/nameserver/'))
        m = 0
        if craw:
            for raw in craw:
                try:
                    grp = []
                    m += 1
                    title = re.search('(.*):', raw.text, re.U)
                    name = re.search('Name(.*)Organization', raw.text, re.U)
                    organization = re.search('Organization(.*)Address', raw.text, re.U)
                    address = re.search('Address(.*)City', raw.text, re.U)
                    city = re.search('City(.*)State / Province', raw.text, re.U)
                    state = re.search('Province(.*)Postal Code', raw.text, re.U)
                    postal = re.search('Postal Code(.*)Country', raw.text, re.U)
                    country = re.search('Country(.*)Phone', raw.text, re.U)
                    phone = re.search('Phone(.*)Fax', raw.text, re.U)
                    fax = re.search('Fax(.*)Email', raw.text, re.U)

                    email_link = raw.findAll('img')

                    grp.append(domain)
                    if title:
                        grp.append(title.group(1))
                        print(title.group(1))
                    if name:
                        grp.append(name.group(1))
                        print(name.group(1))

                    if email_link:
                        for email in email_link:
                            url = "https://who.is{0}".format(email['src'])
                            print(url)
                            if url:
                                grp.append(url)

                            resp = requests.post(url)
                            if resp:
                                img = Image.open(BytesIO(resp.content))
                                text = pytesseract.image_to_string(img)
                            # image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
                            # image1 = cv2.imdecode(image, cv2.IMREAD_COLOR)

                            # img = Image.open('image1')
                            # text = pytesseract.image_to_string(img)
                                if text:
                                    grp.append(text)

                    if organization:
                        grp.append(organization.group(1))
                        print(organization.group(1))
                    if address:
                        grp.append(address.group(1))
                        print(address.group(1))
                    if city:
                        grp.append(city.group(1))
                        print(city.group(1))
                    if state:
                        grp.append(state.group(1))
                        print(state.group(1))
                    if postal:
                        grp.append(postal.group(1))
                        print(postal.group(1))
                    if country:
                        grp.append(country.group(1))
                        print(country.group(1))
                    if phone:
                        grp.append(phone.group(1))
                        print(phone.group(1))
                    if fax:
                        grp.append(fax.group(1))
                        print(fax.group(1))

                    datalist.append(grp)
                except:
                    print('THERE IS AN ERROR')


        # if ctitle and ctitle.text == 'Whois Server' and cvalue.text:
        #     print(ctitle.text)
        #     print(cvalue.text)
        #     grp.append(cvalue.text)
        # if ctitle:
        #     grp.append(ctitle.text)
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
#     datalist.append(grp)
# print(datalist)
#
result = pd.concat([pd.DataFrame(datalist)], ignore_index=True)
#
# convert the pandas dataframe to JSON
json_records = result.to_json(orient='records')
#
# # pretty print to CLI with tabulate
# # converts to an ascii table
# print(tabulate(result, headers=["Domain", "Server"], tablefmt='psql'))
#
# # get current working directory
path = os.getcwd()
#
# # open, write, and close the file
filename = 'webnic_test.json'
with open(filename, 'wb') as f:
    f.write(json_records)
