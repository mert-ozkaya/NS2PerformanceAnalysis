import codecs
import matplotlib.pyplot as plt

dictionaryArray = []
with codecs.open("iz.tr", "r", "cp1252") as inputFile:
    inputFile=inputFile.readlines()
for line in inputFile:
    item = line.split(" ")

    line_dictionary = {}

    line_dictionary['event'] = item[0]
    if(item[0] == '-'):
        continue
    line_dictionary['time'] = float(item[1])
    line_dictionary['packet_size'] = int(item[5])
    line_dictionary['source_address'] = item[8]
    line_dictionary['destination_address'] = item[9]
    line_dictionary['pid'] = int(item[11])

    dictionaryArray.append(line_dictionary)

#########################

resultArray = []
count = 0
time = 0.0
totalByte = 0
i = 0
aaa = 0
while i < len(dictionaryArray):
    while(dictionaryArray[i]['time'] > time):
        tempObject = {}
        tempObject['time'] = time
        tempObject['totalByte'] = totalByte

        resultArray.append(tempObject)
        time += 1
        totalByte = 0
        i += 1

    if(dictionaryArray[i]['event'] == '+'):
        j = i + 1
        if(dictionaryArray[j]['pid'] == dictionaryArray[i]['pid'] and
        dictionaryArray[j]['event'] == 'd' and
        dictionaryArray[j]['source_address'] == dictionaryArray[i]['source_address'] and
        dictionaryArray[j]['destination_address'] == dictionaryArray[i]['destination_address']):
            totalByte = totalByte + dictionaryArray[j]['packet_size']
            i += 1
            continue
        else:
            i += 1
    else:
        i += 1

timeValues = []
totalByteValues = []
for item in resultArray:
    timeValues.append(item['time'])
    totalByteValues.append((item['totalByte']*8) / (1024*1024))


fig, ax = plt.subplots()
ax.plot(timeValues, totalByteValues, linestyle='-', marker='o')

ax.set(xlabel='Zaman (s)', ylabel='Veri miktarı (Mb)',
       title='Drop edilen veri miktarının zamana bağlı değişik grafiği')
ax.grid()

fig.savefig("lossBytePerSecond.png")
plt.show()
