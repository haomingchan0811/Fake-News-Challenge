import pickle
import math
from statistics import *
from collections import Counter
class Feature:
    def __init__(self, statFileName = 'doc_statistics'):
        self.stat = Statistics.load(statFileName)

    def BM25(self, title, bodyId, body, k1 = 1.2, b = 0.3):
        # title, body as list of tokenized words
        score = 0
        intersect = set(title).intersection(body)
        N = self.stat.cf() 
        docLen = self.stat.getDocLen(bodyId)
        avgDocLen = 1.0 * self.stat.cf() / self.stat.getDocNum()
        for t in intersect:
            df = self.stat.df(t)
            tf = self.stat.tf(bodyId,t)
            rsjWeight = math.log((N - df + 0.5) / (df + 0.5))
            tfWeight = tf / (tf + k1 * ((1 - b) + b * docLen / avgDocLen))
            # assume user weight = 1
            score += rsjWeight * tfWeight
        return score

    def Indri(self, title, bodyId, body, lamb = 0.4, mu = 2500):
        # title, body as list of tokenized words
        score = 1
        titleSet = set(title)
        bodySet = set(body)
        docLen = self.stat.getDocLen(bodyId)
        totalLen = self.stat.cf()
        for t in bodySet:
            if t in titleSet:
                df = self.stat.df(t)
                tf = self.stat.tf(bodyId,t)
                p1 = (1 - lamb) * (tf + mu * df / totalLen) / (docLen + mu)
                p2 = lamb * df / totalLen
                score *= (p1 + p2) ** (1.0 / len(title))
                titleSet.remove(t)
        if len(titleSet) == len(title):
            # no overlap
            return 0
        for remainingWord in titleSet:
            # default Indri score
            df = self.stat.df(t)
            p1 = (1 - lamb) * (mu * df / totalLen) / (docLen + mu)
            p2 = lamb * df / totalLen
            score *= (p1 + p2) ** (1.0 / len(title))
        return score

    def cosSim(self, title, bodyId, body):
        countTitle = Counter(title)
        countBody = Counter(body)
        intersect = set(title).intersection(body)
        return sum([countTitle[w] * countBody[w] for w in intersect]) / (math.sqrt(sum([countTitle[w] ** 2 for w in countTitle.keys()])) * math.sqrt(sum([countBody[w] ** 2 for w in countBody.keys()])))

    



if __name__ == '__main__':
    feature = Feature()
    body = 'people duped fake news story claiming nasa forecast total blackout earth six days story entitled confirms earth experience days total darkness december originated website well known publishing fake stories sensational bogus report confirmed earth experience days almost complete darkness happen dates tuesday monday world remain three days without sunlight due solar storm cause dust space debris become plentiful thus block head nasa charles bolden made announcement asked everyone remain product solar storm largest last years period hours six days darkness soon come officials say earth experience major problems since six days darkness nowhere near enough cause major damage adding article also carried quote nasa scientist earl godoy solely rely artificial light six days problem many twitter users believed fake news report expressed going complete days darkness due solar storm nervous janella october days total darkness jammie macaranas october confirms earth experience days total darkness december tt october confirms earth experience days total darkness december omg october islam know means im scared confirms earth experience days total darkness december hiatus october website previously published fake report american rapper actor tupac shakur claiming relatedhalloween friday first time years declared hoaxshah rukh son aryan aishwarya rai niece leaked sex tape fakeebola victims fake news story goes viral sparks outrage social mediaeminem music checking rehab heroin satirical article creates stir social'
    body = body.split(' ')
    title = 'confirms earth experience days total darkness december fake news story goes viral'
    title = title.split(' ')
    bodyId = 154
    print feature.BM25(title, bodyId, body)
    print feature.Indri(title, bodyId, body)
    print feature.cosSim(title, bodyId, body)
    bodyId = 155
    body = 'allegedly pulled strings get one customers fired job prestigious accounting firm complained billing issues false former comcast identified told story site whose readers named comcast worst company two years conal says trouble started erratic bills sometimes show charged equipment never activated actually customer service reps promised problems would instead things got significantly hellish october last according conal comcast sent nearly equipment never ordered want tried bill accountant trade problem documenting every billing error overcharge brought spreadsheet dropped unwanted dvrs modems even conal says able get money instead comcast sent collections conal made call allegedly cost per chose try going customer service help year subscriber instead contacted office spoke someone office promised conal would receive call back address describes callback rep identifying company calling starting help kept insisting technician shown appointment specify rep began asking color tried office let know rep sent way failed miserably considering even comcast acknowledges customer service experience broken could take years reform hardly blame customer understands corporate structures escalating comcast blame conal consumerist point shortly call someone comcast contacted partner firm discuss led ethics investigation subsequent dismissal job says received positive feedback reviews creepiest part although allegedly fired throwing around name powerful surprise happens business swears never told anyone comcast believes went extra mile look online contact comcast comcast confirmed least one part letter lawyer considering filing suit cable provider lawyer said company contact counsel says position complain firm came customer service seems arguing phone minutes trying talk paying fees know fradulent nowhere near worst thing comcast inflict apparently also wreck life ways nothing cable internet really looking forward comcast becoming basically cable provider consumerist'
    body = body.split(' ')
    print feature.BM25(title, bodyId, body)
    print feature.Indri(title, bodyId, body)
    print feature.cosSim(title, bodyId, body)
    




        




