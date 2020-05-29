import codecs
import matplotlib.pyplot as plt

sendCount = 0
receivedCount = 0
time = 0.0
responseArray = []
with codecs.open("iz.tr", "r", "cp1252") as inputFile:
    inputFile=inputFile.readlines()
for line in inputFile:
    item = line.split(" ")

    line_dictionary = {}

    line_dictionary['event'] = item[0]
    line_dictionary['time'] = float(item[1])
    line_dictionary['from_node'] = item[2]
    line_dictionary['to_node'] = item[3]
    line_dictionary['packet_type'] = item[4]
    line_dictionary['packet_size'] = int(item[5])
    line_dictionary['flags'] = item[6]
    line_dictionary['flow_id'] = item[7]
    line_dictionary['source_address'] = item[8]
    line_dictionary['destination_address'] = item[9]
    line_dictionary['sequence_num'] = item[10]
    line_dictionary['pid'] = int(item[11])

    if(line_dictionary['time'] > time):
        if line_dictionary['event'] == '+':
            sendCount += 1
        elif line_dictionary['event'] == 'r':
            receivedCount += 1

        temp = {}
        temp["time"] = time
        if sendCount != 0:
            temp['pdr'] = receivedCount / sendCount
        else:
            temp['pdr'] = 0.0
        time += 1
        sendCount = 0
        receivedCount = 0
        responseArray.append(temp)

    else:
        if line_dictionary['event'] == '+':
            sendCount += 1
        elif line_dictionary['event'] == 'r':
            receivedCount += 1

timeValues = []
pdrValues = []
for item in responseArray:
    timeValues.append(item['time'])
    pdrValues.append(item['pdr'])



fig, ax = plt.subplots()
ax.plot(timeValues, pdrValues, linestyle='-', marker='o')

ax.set(xlabel='Zaman (s)', ylabel='Paket İletim Oranları',
       title='Paket İletim Oranlarının Zamana Bağlı Grafiği')
ax.grid()

fig.savefig("packetDeliveryRatio.png")
plt.show()
