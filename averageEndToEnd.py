import codecs
import matplotlib.pyplot as plt


time = 0.0
dictionaryArray = []  #iz dosyasından okuma yapıldıktan sonra satırların saklanacağı dizi
print('Dosya okunuyor..')

with codecs.open("iz.tr", "r", "cp1252") as inputFile:
    inputFile=inputFile.readlines()
for line in inputFile:
    item = line.split(" ")

    line_dictionary = {}

    line_dictionary['event'] = item[0]
    if(line_dictionary['event'] == '-' or line_dictionary['event'] == 'd'):
        continue
    line_dictionary['time'] = float(item[1])
    line_dictionary['from_node'] = item[2]
    line_dictionary['to_node'] = item[3]
    line_dictionary['pid'] = int(item[11])

    dictionaryArray.append(line_dictionary)

receive_time = 0.0
send_time = 0.0
pay_toplam = 0.0

newArray = []
pktID = dictionaryArray[0]['pid']
for i in range(len(dictionaryArray)):
    if(dictionaryArray[i]['pid'] == pktID):
        newArray.append(dictionaryArray[i])


resultArray = []
count = 0
print('İşleniyor..')

for i in range(len(dictionaryArray)):
    while(dictionaryArray[i]['time'] > time):
        tempObject = {}
        tempObject['time'] = time
        if(count == 0):
            tempObject['EndToEnd'] = 0.0
        else:
            tempObject['EndToEnd'] = pay_toplam / count

        resultArray.append(tempObject)
        time += 1
        count = 0
        pay_toplam = 0

    if(dictionaryArray[i]['event'] == '+'):
        j = i + 1
        while j < len(dictionaryArray):
            if(dictionaryArray[j]['pid'] == dictionaryArray[i]['pid'] and
            dictionaryArray[j]['event'] == 'r' and
            dictionaryArray[j]['from_node'] == dictionaryArray[i]['from_node'] and
            dictionaryArray[j]['to_node'] == dictionaryArray[i]['to_node']):
                count += 1
                pay_toplam = pay_toplam + dictionaryArray[j]['time'] - dictionaryArray[i]['time']
                break
            else:
                j += 1
                continue
    else:
        i += 1

timeValues = []
eteValues = []
for item in resultArray:
    timeValues.append(item['time'])
    eteValues.append(item['EndToEnd'])


fig, ax = plt.subplots()
ax.plot(timeValues, eteValues, linestyle='-', marker='o')

ax.set(xlabel='Zaman (s)', ylabel='Uçtan Uca Ortalama Gecikme',
       title='Uçtan uca gecikme ortalamasının zamana bağlı grafiği')
ax.grid()

fig.savefig("averageEndToEnd.png")
plt.show()
