import pickle
class Statistics:
    def __init__(self):
        self.tfDict = {}
        self.dfDict = {}
        self.docLen = {}
        self.docNum = 0
        self.collFreq = 0

    def create(self,bodyFile, outputFile):
        f = open(bodyFile,'r')
        for line in f.xreadlines():
            line = line.split(',')
            bodyId = line[0]
            body = line[1].split(' ')
            self.tfDict[bodyId] = {}
            for word in body:
                self.tfDict[bodyId][word] = self.tfDict[bodyId].get(word,0) + 1
                self.dfDict[word] = self.dfDict.get(word,0) + 1
            self.docLen[bodyId] = len(body)
            self.collFreq += len(body)
            self.docNum += 1
        f.close()
        output = open(outputFile,'w')
        pickle.dump(self,output)
        output.close()

    @staticmethod
    def load(statisticFileName):
        f = open(statisticFileName,'r')
        res = pickle.load(f)
        f.close()
        return res

    def tf(self,bodyId, word):
        bodyId = str(bodyId)
        if bodyId not in self.tfDict or word not in self.tfDict[bodyId]:
            return -1
        return self.tfDict[bodyId][word]

    def df(self,word):
        return self.dfDict.get(word,-1)

    def getDocLen(self,bodyId):
        bodyId = str(bodyId)
        return self.docLen.get(bodyId,-1)

    def getDocNum(self):
        return self.docNum

    def cf(self):
        return self.collFreq


if __name__ == '__main__':
    # s = Statistics()
    # s.create('train_bodies_tokenized.csv','doc_statistics')
    s = Statistics.load('doc_statistics')
    print s.tf('0','meteorite')
    print s.df('meteorite')
    print s.getDocLen(0)
    print s.getDocNum()
    print s.cf()