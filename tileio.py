list = []
a = 20
f = open('viwiki-latest-all-titles','r')
fout = open("output","w")
fout.write("namespace       title")
for lines in range(2690254):
    line = f.readline().split()
    line[1]=line[1].replace('"','')
    line[1]=line[1].replace('_',' ')
    line[1]=line[1].replace("''","")
    list.append(line)
    s= line[0]+'   '+line[1]
    print(s)
print(list[2690254-1])


