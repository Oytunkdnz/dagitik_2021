import socket
import sys
import threading
import time
import csv
import pandas as pd
import numpy as np


#HELLO ve SEARCH mesajlaşmaları


google_playstore_apps_df= pd.read_csv('/Users/oytunakdeniz/Downloads/googleplaystore.csv')
google_playstore_apps_df=google_playstore_apps_df.drop_duplicates()
app = google_playstore_apps_df.App.unique()
apps= np.sort(app)
applist = apps.tolist()

appslist = [word for line in applist for word in line.split()]
#google_playstore_apps_df.describe()
arg = []
index = 0
sonuclar = {}
results = []

def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]




threshold = 0.80     # if needed


class connThread(threading.Thread):
    def __init__(self, threadID, conn, c_addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
        self.c_addr = c_addr
        self.state = True

    def protokol(self, data):
        print(data)
        if data == "HELLO":

            self.conn.send("HELLO::Oytun".encode())
        elif (data.split())[0]== "SEARCH":
            #x = ((data.split("::"))[1].split(":"))[0]
            #y = ((data.split("::"))[2].split(":"))[0]
            #z = ((data.split("::"))[3].split(":"))[0]
            #if x == "P":

            #index = appslist.index((data.split())[1])
            #print(index)
            for key in applist:
                key = key.lower()
                for word in (data.split())[1:]:
                    word = word.lower()
                    try:
                        # print(key)
                        # print(word)
                        #res = cosdis(word2vec(word), word2vec(key))
                        # print(res)
                        #print("The cosine similarity between : {} and : {} is: {}".format(word, key, res*100))
                        if key.find(word) != -1:
                            sonuclar[key] = key.find(word)
                            #print(key)
                            #index = applist.index(key)
                            #print("APPFOUND :: {} ".format(applist[index]))

                    except IndexError:
                        pass
            #print(applist)
            #sonuclarbu = np.sort(sonuclar.values())
            #print(np.sort(sonuclar.values().items))

            for k in range(3):
                min = 100
                y = ""
                for i in sonuclar.keys():
                    if sonuclar[i] < min:
                        y = i
                        min = sonuclar[i]
                results.append(y)
                sonuclar.pop(y)
                for j in results:
                    self.conn.send(j.encode())
            #self.conn.send("Iyiyim, sagol".encode())
        elif data == "Hava":
            self.conn.send("Yagmurlu".encode())
        elif data == "Haber":
            self.conn.send("Korona".encode())
        elif data == "Kapan":
            self.conn.send("Gule gule".encode())
            self.conn.send("\n\n".encode())
            print("baglanti kesiliyor %s" % str(self.c_addr))
            self.state = False #rundaki while looptan cikmak icin
        else:
            self.conn.send("Anlamadim".encode())

    def run(self):
        saat = time.localtime()
        self.conn.send(("Saat su an " + str(saat.tm_hour) + ":" + str(saat.tm_min) + ":" + str(saat.tm_sec)).encode()) #string degil bit gonderiyoruz?
        #self.conn.send(b"hosgeldiniz") alternatively
        print("Baglanti kuruldu %s" % str(self.c_addr))
        while self.state:
            data = conn.recv(1024)
            data_str = data.decode().strip()  # gelen datadaki new line i atmazsak problem
            self.protokol(data_str)
        self.conn.close()
        print("thread %s kapaniyor" % str(self.threadID))

s = socket.socket()
s.settimeout(5)

ip = "localhost"
port = 12419

addr_server = (ip, port)
s.bind(addr_server)

s.listen(5) #??
counter = 0
threads = []
while True:
    try:
        conn, addr = s.accept()# accept bindingdir baglanti istegi gelene kdr bekletir buradan sonrasi sadece istek geldikten sonra devreye girer bu yuzden try except ve timeout koymak lzm
        newConnThread = connThread(counter, conn, addr)
        threads.insert(counter, newConnThread)
        newConnThread.start()
        counter += 1

    except: # socket.timeout:
        try:
            pass
        except KeyboardInterrupt:
            print("exiting very gracefully")
            sys.exit(0)

    for i in range(len(threads)):
        if not threads[i].isAlive() :
            threads.pop(i)
            break
print(counter)
s.close()
