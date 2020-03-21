import matplotlib.pyplot as plt
import datetime

f = open("000020.KS.csv", 'r')
data = []
date = []
while True:
    line = f.readline()
    if not line : break
    lin = line.split(',')
    if lin[5] == '' or lin[5] == '"End"': continue    # if no value, just pass
    value = lin[5].replace('\n','')
    data.append(float(value))
    date.append(datetime.datetime.strptime(lin[1],'%Y%m%d'))

f.close()
data = data[4800:]
date = date[4800:]

def weighted_filter(array,index,n,dense):  # return weighted moving average point for ndays
    
    if len(array) > index and index >= n-1 :
        window = array[index-n+1:index+1]
        value_sum = 0
        weight_sum = 0
        for i in range(0,len(window)):
            weight = (i+1)**dense/n
            value_sum += window[i]*weight
            weight_sum += weight
        weighted_avg = value_sum/weight_sum
        avg = sum(window)/len(window)
        return [weighted_avg,avg]
        
    else :
        return -1

n = 20
dense = 10
filtered_data = []
normal_avg = []
filtered_date = []
for i in range(0,len(data)):
    value = weighted_filter(data,i,n,dense)
    if value != -1 :
        filtered_data.append(value[0])
        normal_avg.append(value[1])
        filtered_date.append(date[i])

plt.plot(date,data,color='blue',label='original value')
plt.plot(filtered_date,normal_avg,color='green',label='normal moving avg')
plt.plot(filtered_date,filtered_data,color='red',label='weighted moving avg filter')
plt.title('weighted moving average filter')
plt.legend()
plt.show()
