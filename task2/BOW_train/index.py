import pickle
class Index:
    def __init__(self):
        self.tfDict = {}
        self.dfDict = {}
        self.docLen = {}
        self.id_to_body = {}
        self.id_to_body_sent = {}
        self.docNum = 0
        self.collFreq = 0

    def create(self,bodyFile, outputFile, bodySentFile = ''):
        f = open(bodyFile,'r')
        for line in f.xreadlines():
            line = line.replace('\n','').split(',')
            bodyId = line[0]
            body = line[1].split(' ')
            self.tfDict[bodyId] = {}
            self.id_to_body[bodyId] = body
            for word in body:
                self.tfDict[bodyId][word] = self.tfDict[bodyId].get(word,0) + 1
                self.dfDict[word] = self.dfDict.get(word,0) + 1
            self.docLen[bodyId] = len(body)
            self.collFreq += len(body)
            self.docNum += 1

        f.close()
        if len(bodySentFile) > 0:
            f = open(bodySentFile,'r')
            for line in f.xreadlines():
                line = line.replace('\n','').split(',')
                bodyId = line[0]
                bodySent = line[1].split('\t')
                self.id_to_body_sent[bodyId] = [sent.split(' ') for sent in bodySent]
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

    def getBody(self, bodyId):
        bodyId = str(bodyId)
        return self.id_to_body.get(bodyId,[])

    def getBodySent(self, bodyId):
        bodyId = str(bodyId)
        return self.id_to_body_sent.get(bodyId,[])


if __name__ == '__main__':
    s = Index()
    # s.create('train_bodies_tokenized_task2.csv','index_task2','train_bodies_tokenized_task2_sentence.csv')
    s = Index.load('index_task2')
    print s.tf('0','meteorite')
    print s.df('meteorite')
    print s.getDocLen(0)
    print s.getDocNum()
    print s.cf()
    print s.getBody(2532)
    print s.getBodySent(2532)
    # print s.getBodySent(1234)
    # print s.getBodySent(123)