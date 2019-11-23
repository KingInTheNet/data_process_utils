import wikipedia
import time
wikipedia.set_lang('vi')
f = open('output2','r')
fout = open('out','w')
li = []

for lines in range(2690254):
    start = time.time()
    line = list(f.readline().split("'"))
    #print(line)
    s = line[3]
    print(s)
    item = []
    try:
        s1=wikipedia.summary(s,3)
        item.append(line[3])
        item.append(s1)
        fout.write("%s\n" % item)
        li.append(item)
        print("    "+str(time.time()-start))
    except Exception as e:
        print(e)

