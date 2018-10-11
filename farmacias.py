import requests
import xlsxwriter
from bs4 import BeautifulSoup
import json

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('pharma.xlsx')
worksheet = workbook.add_worksheet()

# headers
worksheet.write('A1', 'Farmacia')
worksheet.write('B1', 'localizacao')
worksheet.write('C1', 'Contacto')

#key
key=open('gmapskey.txt', 'r').read()

#content
url = 'http://www.portaldefarmacias.com/farmacias'
for link in range(1, 15):
    if requests.get(url + '/' + str(link), proxies=proxies).status_code == 200:
        req = requests.get(url + '/' + str(link), proxies=proxies)
        c = req.content
        soup = BeautifulSoup(c, 'lxml')

        # infos
        linfo = []
        linfo2 = []
        linfo3 = []
        linfo4 = []
        for info in soup.findAll('div', style="width:700px;float:left;"):
            linfo.append(info.get_text().split('\r\n'))
        for info2 in linfo:
            for info3 in info2:
                linfo2.append(info3.strip())
        for info4 in linfo2:
            linfo3.append(info4.replace(
                u'                             \n\xbb ver mais', ''))
        for info5 in linfo3:
            linfo4.append(info5.replace(
                '                             \nDados incorrectos? Actualize aqui.', ''))
        # subagrupar em casa resultado e fora
        linfo4 = [linfo4[x:x + 3] for x in xrange(0, len(linfo4), 3)]
        for conjuntos in linfo4:
            for local in conjuntos:
                url2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
                    local.replace(" ", "+") + \
                    '&key='+key
                req2 = requests.get(url2, proxies=proxies)
                data = json.loads(req.text)
                lng = data['results'][0]['geometry']['location']['lng']
                lat = data['results'][0]['geometry']['location']['lat']
        #print linfo4

        # fill
        i = 0
        j = link - 1
        for x in linfo4:
            cell = 'A' + str(i + 2 + j * 5)  # loop para o local a escrever
            cell2 = 'D' + str(i + 2 + j * 5)
            worksheet.write_row(cell, linfo4[i])
            worksheet.write_row(cell, linfo4[i + 3])
            i = i + 1
    else:
        print('error')

workbook.close()
