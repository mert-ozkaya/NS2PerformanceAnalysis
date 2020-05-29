import codecs
import matplotlib.pyplot as plt

dictionaryArray = [] #iz dosyasından okuma yapıldıktan sonra satırların saklanacağı dizi

#iz dosyası okuma modunda açılır
with codecs.open("iz.tr", "r", "cp1252") as inputFile:
    inputFile=inputFile.readlines()
#her satır boşluğa göre parçalanır
#Performans metriği için gerekli her sütun dictionary tipinde isimlendirilerek saklanır
#dictionaryArray değişkenine alınan satır eklenir.
for line in inputFile:
    item = line.split(" ")

    line_dictionary = {}

    line_dictionary['event'] = item[0]
    if(item[0] == '-' or item[0] == '+' or item[0] == 'd'):
        continue
    line_dictionary['time'] = float(item[1])
    if(item[4] == 'ack'):
        continue
    else:
        line_dictionary['packet_type'] = item[4]

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

print('İşleniyor..')
#dictionaryArray sonuna kadar ilerle
while i < len(dictionaryArray):
    while(dictionaryArray[i]['time'] > time): #her saniye aralığı bu while döngüsü ile belirlenir
        tempObject = {}
        tempObject['time'] = time #aralığın değeri geçici bir objeye atanır
        tempObject['totalByte'] = totalByte #toplan 
        resultArray.append(tempObject)
        time += 1
        totalByte = 0
        i += 1

    if(dictionaryArray[i]['event'] == 'r'):
        totalByte = totalByte + dictionaryArray[i]['packet_size']
    i += 1

timeValues = []
totalByteValues = []
for item in resultArray:
    timeValues.append(item['time'])
    totalByteValues.append(item['totalByte'] * 8 / (1024*1024))

fig, ax = plt.subplots()
ax.plot(timeValues, totalByteValues, linestyle='-', marker='o')

ax.set(xlabel='Zaman (s)', ylabel='Verim (Mb)',
       title='ACK Paketlerinin Verim - Zaman Grafiği')
ax.grid()

fig.savefig("ackThroughput.png")
plt.show()
