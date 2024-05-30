import numpy as np
import json
import random
import math
import functools
from sklearn.preprocessing import minmax_scale
import time
import concurrent.futures

futureData = []
tau = 6
epsilon = 0
initTheta = 1000000.0
alpha = 0.0045
xi = 1
cardinalityK = 20.0
POPULATION_SIZE = 100
MAX_GENERATION = 150
generationCheckedConsecutiveNumToConvergenceDecision = 79
# upsilon = 0.06

printAllowed = True
def myPrint(content):
    if not printAllowed:
        return
    print(content)

def printSolution(content):
    print(content)

def loadDataInput(inputString):
    data = json.loads(inputString)
    for i in data['stocks']:
        myPrint(i)

    return data

class Individual(object):
    '''
    Class representing individual in population
    '''

    def __init__(self, cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash,
                 fitnesses, aggregatedFitness, finalFitness, aggregatedFitnessNom, finalFitnessNom,
                 frontier, crowdingDistance, crowdingDistances, cashEndMonth):
        self.cashBeginMonth = cashBeginMonth
        self.holdingStocks = holdingStocks
        self.buyingStocks = buyingStocks
        self.sellingStocks = sellingStocks
        self.finalCash = finalCash
        self.fitnesses = fitnesses
        self.aggregatedFitness = aggregatedFitness
        self.finalFitness = finalFitness
        self.aggregatedFitnessNom = aggregatedFitnessNom
        self.finalFitnessNom = finalFitnessNom
        self.frontier = frontier
        self.crowdingDistance = crowdingDistance
        self.crowdingDistances = crowdingDistances
        self.cashEndMonth = cashEndMonth

def non_zero_indices(array):
    count = 0
    for element in array:
        if element != 0:
            count += 1

    non_zero_indices = [0] * count
    index = 0
    for i in range(len(array)):
        if array[i] != 0:
            non_zero_indices[index] = i
            index += 1

    return non_zero_indices

def canReleaseAllAtTheFinalMonth(j, t, tau, futureData, spendableCash, holdingAmount, price):
    for month in range(t, tau, 1):
        for priceObject in futureData['stocks'][j]['prices']:
            if priceObject['month'] - 1 == month:
                holdingAmount = holdingAmount - priceObject['matchedTradingVolume']
                if holdingAmount <= 0:
                    return spendableCash
    if holdingAmount > 0:
        return spendableCash - holdingAmount * price
    return spendableCash

def shouldSellAsManyAsFromNowAmount(t, tau, j, futureData, holdingAmount):
    for month in range(tau, t, 1):
        for priceObject in futureData['stocks'][j]['prices']:
            if priceObject['month'] - 1 == month:
                holdingAmount = holdingAmount - priceObject['matchedTradingVolume']
                if holdingAmount < 0:
                    return 0
    if holdingAmount > 0:
        return holdingAmount
    return 0

def chooseFromWhichParent(hasParents):
    if hasParents == False:
        return 0
    prob = random.random()

    # if prob is less than 0.45, insert gene
    # from parent 1
    if prob < 0.45:
        return 1
    # if prob is between 0.45 and 0.90, insert
    # gene from parent 2
    elif prob < 0.90:
        return 2
    # otherwise insert random gene(mutate),
    # for maintaining diversity
    else:
        return 0

def prinfReSult(population, frontierNumPassed, generationNumUntilReachingLastPivot, log_dn, log_gn, log_fitnesses, futureData):
    myPrint("Printing result")
    log_dn.append(frontierNumPassed)
    log_gn.append(generationNumUntilReachingLastPivot)
    log_fitnesses.append(population.aggregatedFitness)
    printSolution(f'To gain the solution needed {generationNumUntilReachingLastPivot} generations, and went through {frontierNumPassed} frontiers')
    printSolution('final cash = ')
    printSolution(population.finalCash)
    printSolution('fitness = ')
    printSolution(population.aggregatedFitness)
    printSolution('buying = ')
    printSolution(population.buyingStocks)
    printSolution('holding = ')
    printSolution(population.holdingStocks)
    printSolution('selling = ')
    printSolution(population.sellingStocks)
    stocksLen = len(futureData['stocks'])
    for t in range(tau):
        boughtStocks = ""
        # futureData['stocks'][j]['prices'][t-1]['value']
        for j in range(stocksLen):
            if population.buyingStocks[t][j] != 0:
                boughtStocks += "\n\t\t\t" + str(population.buyingStocks[t][j]) + " " + str(
                    futureData['stocks'][j]['symbol']) + " -" + str(
                    population.buyingStocks[t][j] * futureData['stocks'][j]['prices'][t]['value'] * (1 + epsilon))

        sellStocks = ""
        for j in range(stocksLen):
            if population.sellingStocks[t][j] != 0:
                sellStocks += "\n\t\t\t" + str(population.sellingStocks[t][j]) + " " + str(
                    futureData['stocks'][j]['symbol']) + " +" + str(
                    population.sellingStocks[t][j] * futureData['stocks'][j]['prices'][t]['value'] * (1 - epsilon))

        dividends = ""
        for j in range(stocksLen):
            if population.holdingStocks != 0:
                dividendsSplitingLen = len(futureData['stocks'][j]['dividendSpitingHistories'])
                if dividendsSplitingLen > 0:
                    for d in range(dividendsSplitingLen):
                        if population.holdingStocks[t - 1][j] > 0 and \
                                futureData['stocks'][j]['dividendSpitingHistories'][d]["month"] - 1 == t and t - 1 > 0:
                            dividends += "\n\t\t\t" + str(population.holdingStocks[t - 1][j]) + " " + str(
                                futureData['stocks'][j]['symbol']) + " +" + str(futureData['stocks'][j]['dividendSpitingHistories'][d]["value"] * population.holdingStocks[t - 1][j])

        printSolution("\nMonth= " + str(t) + "\n\t>>Cash=" + str(population.cashBeginMonth[
                                                                     t]) + "\n\t>>Bought= " + boughtStocks + "\n\t>>Sold= " + sellStocks + "\n\t>>Dividend payout= " + dividends + "\n\t>>Bank deposit=" + str(population.cashEndMonth[t]))
    myPrint("DONE")


def genInvestmentPlan(futureData, parent1, parent2, currentSaSolution):
    myPrint("gen investment plan from 2 parents")
    inputLen = len(futureData['stocks'])
    myPrint('len >> %d' % inputLen)

    rows, cols = (tau + 1, inputLen)
    holdingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    buyingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    sellingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    cashBeginMonth = []
    cashEndMonth = []

    hasParent = False
    if parent1 is not None:
        hasParent = True

    findNeighborModifiedMonth = random.choice(range(tau - 2))

    availableCash = initTheta
    bankingDeposit = 0
    # myPrint(random.choice(range(inputLen)))
    for t in range(tau + 1):
        myPrint(t)

        # update budget
        if t <= 0:
            availableCash = initTheta
        if t > 0:
            availableCash += bankingDeposit * (1 + alpha)
            for j in range(inputLen):
                availableCash += sellingStocks[t - 1][j] * futureData['stocks'][j]['prices'][t - 1]['value'] * (1 - epsilon)

        # plus dividends if eligible for it
        if t > 2:
            for j in range(inputLen):
                for object in futureData['stocks'][j]['dividendSpitingHistories']:
                    if object['month'] - 1 == t - 1:
                        availableCash += holdingStocks[t - 2][j] * object['value'] / 1000  # kVND

        cashBeginMonth.append(availableCash)
        # random to see how many stocks should we buy
        shouldBuyStockNum = random.choice(range(math.floor(cardinalityK)))
        shouldBuyStockIndices = random.sample(range(inputLen), shouldBuyStockNum)

        chooseFrom = chooseFromWhichParent(hasParent)
        if chooseFrom == 1:
            # shouldBuyStockIndices = [v for v in parent1.buyingStocks[t] if v != 0]
            shouldBuyStockIndices = non_zero_indices(parent1.buyingStocks[t])
        elif chooseFrom == 2:
            # shouldBuyStockIndices = [v for v in parent2.buyingStocks[t] if v != 0]
            shouldBuyStockIndices = non_zero_indices(parent2.buyingStocks[t])

        justBoughtStocks = []
        for j in shouldBuyStockIndices:
            if np.count_nonzero(holdingStocks[t]) >= cardinalityK or t >= tau - 2:
                break
            myPrint("Buying stock index = {}; symbol = {}".format(j, futureData['stocks'][j]['symbol']))
            # random buy stock amount if valid (budget, trading capability, dividend constrains
            spendableCash = availableCash
            priceObject = futureData['stocks'][j]['prices'][t]
            jPrice = priceObject['value']
            if priceObject['matchedTradingVolume'] * jPrice < availableCash:
                spendableCash = priceObject['matchedTradingVolume'] * jPrice

            spendableCash = canReleaseAllAtTheFinalMonth(j, t, tau, futureData, spendableCash, holdingStocks[t][j],
                                                         jPrice)
            if spendableCash <= 0:
                continue

            spendableCashFloor = math.floor(spendableCash)
            if spendableCashFloor > 0:
                if chooseFrom == 1 and parent1.buyingStocks[t][j] * jPrice <= spendableCash:
                    buyingStocks[t][j] = parent1.buyingStocks[t][j]
                elif chooseFrom == 2 and parent2.buyingStocks[t][j] * jPrice <= spendableCash:
                    buyingStocks[t][j] = parent2.buyingStocks[t][j]
                else:
                    myPrint("math.floor(spendableCash))= %s" % spendableCashFloor)
                    buyingStocks[t][j] = math.floor(
                        math.floor(random.choice(range(spendableCashFloor)) / jPrice) / xi) * xi
                    if currentSaSolution is not None:
                        if t < findNeighborModifiedMonth:
                            buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j]
                        elif t == findNeighborModifiedMonth:
                            if random.choice(range(2)) == 1:
                                buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j] + random.choice(
                                    [1, 2, 3]) * xi
                            else:
                                buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j] - random.choice(
                                    [1, 2, 3]) * xi
            while buyingStocks[t][j] * jPrice * (1 + epsilon) > spendableCash:  # constraint 6
                buyingStocks[t][j] -= xi

            if buyingStocks[t][j] > 0:
                justBoughtStocks.append(j)
                # decrease budget
                availableCash -= buyingStocks[t][j] * jPrice * (1 + epsilon)
            else:
                buyingStocks[t][j] = 0
            holdingStocks[t][j] = holdingStocks[t - 1][j] + buyingStocks[t][j]

        # update holding amount
        for j in range(inputLen):
            if j in justBoughtStocks:
                continue
            holdingStocks[t][j] = holdingStocks[t - 1][j] + buyingStocks[t][j]

        myPrint('About to sell....')
        # selling stocks
        for j in range(inputLen):
            if holdingStocks[t][j] <= 0 or j in justBoughtStocks or buyingStocks[t - 1][j] > 0:
                continue
            myPrint("Selling stock index = {}; symbol = {}".format(j, futureData['stocks'][j]['symbol']))
            canHaveDividendNextMonth = False
            for dividendSpitingHistoriesObject in futureData['stocks'][j]['dividendSpitingHistories']:
                if dividendSpitingHistoriesObject['month'] == t + 1:
                    canHaveDividendNextMonth = True
                    break
            if canHaveDividendNextMonth and t < tau - 2:
                continue

            for priceObject in futureData['stocks'][j]['prices']:
                if priceObject['month'] - 1 == t:
                    canSellNum = holdingStocks[t][j]
                    if canSellNum > priceObject['matchedTradingVolume']:
                        canSellNum = priceObject['matchedTradingVolume']

                    sellingStocks[t][j] = shouldSellAsManyAsFromNowAmount(t, tau, j, futureData, holdingStocks[t][j])
                    if sellingStocks[t][j] <= 0:
                        if chooseFrom == 1 and parent1.sellingStocks[t][j] <= canSellNum:
                            sellingStocks[t][j] = parent1.sellingStocks[t][j]
                        elif chooseFrom == 2 and parent2.sellingStocks[t][j] <= canSellNum:
                            sellingStocks[t][j] = parent2.sellingStocks[t][j]
                        else:
                            sellingStocks[t][j] = random.choice(range(math.floor(canSellNum / xi))) * xi
                            if currentSaSolution is not None:
                                if t < findNeighborModifiedMonth:
                                    sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j]
                                elif t == findNeighborModifiedMonth:
                                    if random.choice(range(2)) == 1:
                                        sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j] + random.choice(
                                            [1, 2, 3]) * xi
                                    else:
                                        sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j] - random.choice(
                                            [1, 2, 3]) * xi

                    holdingStocks[t][j] -= sellingStocks[t][j]

        # deposit to the bank the remaining budget
        if t < tau:
            cashEndMonth.append(availableCash)
            bankingDeposit = availableCash
            availableCash = 0
        # end plan

    fitnesses = [[0 for _ in range(4)] for _ in
                 range(tau)]  # mean(variances), mean(skewness), mean(kurtosis), mean(entropy), tau profit

    #TODO: calculate wCVaR
    aggregatedFitness=[]
    finalFitness=0
    # for t in range(tau):
    #     w = genWeightVector(holdingStocks[t])
    #     fitnesses[t][0] = calVariance(M2, w)
    #     fitnesses[t][1] = calSkewness(M3, w)
    #     fitnesses[t][2] = calKurtosis(M4, w)
    #     fitnesses[t][3] = calEntropy(w)
    # fitnesses_norm = minmax_scale(fitnesses, feature_range=(0,1), axis=0)

    # tempAggregatedFitness = np.mean(fitnesses, axis=0)
    # aggregatedFitness = [0 for _ in range(5)]
    # for i in range(4):
    #     aggregatedFitness[i] = tempAggregatedFitness[i]
    # aggregatedFitness[4] = availableCash
    # finalFitness = calFitnessNom(aggregatedFitness)

    finalCash = availableCash


    frontier = -math.inf
    crowdingDistance = -math.inf
    return cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance, cashEndMonth


def verifyInvestmentPlan(holdingStocks, buyingStocks, sellingStocks, futureData):
    if np.count_nonzero(sellingStocks[0]) > 0:
        return False, "at t=0, no stock j is sold out"
    # Add more validation checks as per requirement
    for t in range(tau):
        totalSecurities = 0
        for j in range(len(holdingStocks[0])):
            totalSecurities += holdingStocks[t][j]

            if t > 0 and sellingStocks[t][j] > holdingStocks[t - 1][j]:
                return False, "the number of stock j sold out cannot exceed the number of stock j is holding"

            if buyingStocks[t][j] < 0 or sellingStocks[t][j] < 0:
                return False, "Negative stock transactions are not possible."

            if buyingStocks[t][j] % xi > 0 or sellingStocks[t][j] % xi > 0:
                return False, "The quantity of stock j available for purchase or sale is subject to its lot size constraint."

            for priceObject in futureData['stocks'][j]['prices']:
                if priceObject['month'] == t + 1:
                    if priceObject['matchedTradingVolume'] < buyingStocks[t][j] or priceObject['matchedTradingVolume'] < sellingStocks[t][j]:
                        return False, 'the volume of stock j that can be bought or sold is limited by its maximum trading volume.'

        if totalSecurities < 0:
            return False, "Negative securities holding is not possible."
        if np.count_nonzero(holdingStocks[t]) > cardinalityK:
            return False, 'Violate cardinality at month t=%s' % t

    if np.count_nonzero(holdingStocks[tau - 1]) > 0:
        return False, "at t=tau, sell all the holding stocks"

    return True, "Investment plan is valid."

def nsga3():
    myPrint("starting NSGA-III")

    population = []

    # P_{t=0}
    for _ in range(POPULATION_SIZE):
        cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance, cashEndMonth = genInvestmentPlan(
            futureData, None, None, None)
        population.append(Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses,
                                      aggregatedFitness, finalFitness, [], 0.0, frontier, crowdingDistance,
                                      [0, 0, 0, 0, 0], cashEndMonth))


    myPrint('done giving birth')



def main():
    jsonInput2023 = '{"stocks":[{"symbol":"ACB","companyName":"Ngân hàng TMCP Á Châu","type":"VN30","year":2023,"prices":[{"month":1,"value":26.35,"matchedTradingVolume":5.499E7},{"month":2,"value":25.8,"matchedTradingVolume":6.3237E7},{"month":3,"value":25.35,"matchedTradingVolume":9.20633E7},{"month":4,"value":25.3,"matchedTradingVolume":8.14876E7},{"month":5,"value":25.4,"matchedTradingVolume":1.608784E8},{"month":6,"value":22.3,"matchedTradingVolume":1.920848E8},{"month":7,"value":22.95,"matchedTradingVolume":1.640575E8},{"month":8,"value":24.4,"matchedTradingVolume":2.570596E8},{"month":9,"value":22.95,"matchedTradingVolume":1.263825E8},{"month":10,"value":22.8,"matchedTradingVolume":1.01492E8},{"month":11,"value":23.3,"matchedTradingVolume":1.540952E8},{"month":12,"value":23.9,"matchedTradingVolume":1.309384E8}],"dividendSpitingHistories":[]},{"symbol":"BCM","companyName":"Tổng Công ty Đầu tư và Phát triển Công nghiệp – CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":85.2,"matchedTradingVolume":1681700.0},{"month":2,"value":86.0,"matchedTradingVolume":1668200.0},{"month":3,"value":84.5,"matchedTradingVolume":2201700.0},{"month":4,"value":83.5,"matchedTradingVolume":1124200.0},{"month":5,"value":78.5,"matchedTradingVolume":1003200.0},{"month":6,"value":82.1,"matchedTradingVolume":6718400.0},{"month":7,"value":81.0,"matchedTradingVolume":5792000.0},{"month":8,"value":79.0,"matchedTradingVolume":5927500.0},{"month":9,"value":72.6,"matchedTradingVolume":5679800.0},{"month":10,"value":69.5,"matchedTradingVolume":4024400.0},{"month":11,"value":62.4,"matchedTradingVolume":6680300.0},{"month":12,"value":66.0,"matchedTradingVolume":1.05481E7}],"dividendSpitingHistories":[{"month":11,"value":800.0}]},{"symbol":"BID","companyName":"Ngân hàng TMCP Đầu tư và Phát triển Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":45.95,"matchedTradingVolume":2.88095E7},{"month":2,"value":47.2,"matchedTradingVolume":2.70027E7},{"month":3,"value":48.0,"matchedTradingVolume":1.78979E7},{"month":4,"value":46.0,"matchedTradingVolume":1.53768E7},{"month":5,"value":45.1,"matchedTradingVolume":1.2405E7},{"month":6,"value":45.35,"matchedTradingVolume":2.61229E7},{"month":7,"value":47.35,"matchedTradingVolume":3.93465E7},{"month":8,"value":49.1,"matchedTradingVolume":4.26147E7},{"month":9,"value":47.5,"matchedTradingVolume":2.19276E7},{"month":10,"value":43.95,"matchedTradingVolume":2.0611E7},{"month":11,"value":44.15,"matchedTradingVolume":1.78062E7},{"month":12,"value":43.4,"matchedTradingVolume":2.24373E7}],"dividendSpitingHistories":[]},{"symbol":"BVH","companyName":"Tập đoàn Bảo Việt","type":"VN30","year":2023,"prices":[{"month":1,"value":51.0,"matchedTradingVolume":7621200.0},{"month":2,"value":51.2,"matchedTradingVolume":9028400.0},{"month":3,"value":50.0,"matchedTradingVolume":5479800.0},{"month":4,"value":49.2,"matchedTradingVolume":5394500.0},{"month":5,"value":46.0,"matchedTradingVolume":1.05267E7},{"month":6,"value":45.3,"matchedTradingVolume":2.13723E7},{"month":7,"value":48.15,"matchedTradingVolume":2.26194E7},{"month":8,"value":48.0,"matchedTradingVolume":1.95543E7},{"month":9,"value":45.8,"matchedTradingVolume":1.30652E7},{"month":10,"value":42.65,"matchedTradingVolume":6368600.0},{"month":11,"value":41.3,"matchedTradingVolume":6801500.0},{"month":12,"value":40.5,"matchedTradingVolume":6636100.0}],"dividendSpitingHistories":[{"month":11,"value":954.0}]},{"symbol":"CTG","companyName":"Ngân hàng TMCP Công Thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":31.1,"matchedTradingVolume":6.19356E7},{"month":2,"value":30.45,"matchedTradingVolume":5.62202E7},{"month":3,"value":29.5,"matchedTradingVolume":4.62949E7},{"month":4,"value":30.0,"matchedTradingVolume":4.04912E7},{"month":5,"value":28.4,"matchedTradingVolume":7.05504E7},{"month":6,"value":30.0,"matchedTradingVolume":1.20986E8},{"month":7,"value":30.3,"matchedTradingVolume":1.269248E8},{"month":8,"value":32.6,"matchedTradingVolume":1.849013E8},{"month":9,"value":33.2,"matchedTradingVolume":1.252328E8},{"month":10,"value":29.95,"matchedTradingVolume":6.47939E7},{"month":11,"value":30.25,"matchedTradingVolume":6.29258E7},{"month":12,"value":27.1,"matchedTradingVolume":7.30158E7}],"dividendSpitingHistories":[]},{"symbol":"FPT","companyName":"CTCP FPT","type":"VN30","year":2023,"prices":[{"month":1,"value":84.0,"matchedTradingVolume":1.49761E7},{"month":2,"value":82.8,"matchedTradingVolume":1.6827E7},{"month":3,"value":80.6,"matchedTradingVolume":1.51259E7},{"month":4,"value":80.9,"matchedTradingVolume":1.11001E7},{"month":5,"value":84.1,"matchedTradingVolume":1.65431E7},{"month":6,"value":87.3,"matchedTradingVolume":1.93342E7},{"month":7,"value":87.0,"matchedTradingVolume":2.72301E7},{"month":8,"value":96.7,"matchedTradingVolume":4.53975E7},{"month":9,"value":99.0,"matchedTradingVolume":5.49667E7},{"month":10,"value":97.0,"matchedTradingVolume":5.85186E7},{"month":11,"value":93.0,"matchedTradingVolume":4.69906E7},{"month":12,"value":97.2,"matchedTradingVolume":4.36497E7}],"dividendSpitingHistories":[{"month":8,"value":1000.0}]},{"symbol":"GAS","companyName":"Tổng Công ty Khí Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":108.2,"matchedTradingVolume":3892900.0},{"month":2,"value":109.0,"matchedTradingVolume":4822000.0},{"month":3,"value":108.1,"matchedTradingVolume":4192400.0},{"month":4,"value":102.5,"matchedTradingVolume":6178600.0},{"month":5,"value":94.9,"matchedTradingVolume":7790900.0},{"month":6,"value":96.6,"matchedTradingVolume":1.45087E7},{"month":7,"value":101.6,"matchedTradingVolume":1.42296E7},{"month":8,"value":103.2,"matchedTradingVolume":1.20026E7},{"month":9,"value":110.0,"matchedTradingVolume":1.18793E7},{"month":10,"value":89.3,"matchedTradingVolume":1.23912E7},{"month":11,"value":80.1,"matchedTradingVolume":1.12482E7},{"month":12,"value":79.8,"matchedTradingVolume":1.5394E7}],"dividendSpitingHistories":[{"month":8,"value":3600.0}]},{"symbol":"GVR","companyName":"Tập đoàn Công nghiệp Cao su Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":16.85,"matchedTradingVolume":4.1546E7},{"month":2,"value":15.6,"matchedTradingVolume":3.46376E7},{"month":3,"value":15.5,"matchedTradingVolume":4.22057E7},{"month":4,"value":16.35,"matchedTradingVolume":4.92206E7},{"month":5,"value":18.4,"matchedTradingVolume":7.46486E7},{"month":6,"value":19.6,"matchedTradingVolume":8.05328E7},{"month":7,"value":22.35,"matchedTradingVolume":6.63856E7},{"month":8,"value":22.7,"matchedTradingVolume":6.33971E7},{"month":9,"value":23.2,"matchedTradingVolume":7.73157E7},{"month":10,"value":21.45,"matchedTradingVolume":6.5337E7},{"month":11,"value":20.15,"matchedTradingVolume":4.46305E7},{"month":12,"value":21.2,"matchedTradingVolume":3.96708E7}],"dividendSpitingHistories":[{"month":11,"value":350.0}]},{"symbol":"HDB","companyName":"Ngân hàng TMCP Phát triển TP. HCM","type":"VN30","year":2023,"prices":[{"month":1,"value":18.65,"matchedTradingVolume":3.22759E7},{"month":2,"value":19.0,"matchedTradingVolume":4.4446E7},{"month":3,"value":19.25,"matchedTradingVolume":5.77437E7},{"month":4,"value":19.7,"matchedTradingVolume":4.51794E7},{"month":5,"value":19.6,"matchedTradingVolume":3.38232E7},{"month":6,"value":19.2,"matchedTradingVolume":5.41306E7},{"month":7,"value":18.9,"matchedTradingVolume":6.66127E7},{"month":8,"value":17.55,"matchedTradingVolume":6.28059E7},{"month":9,"value":18.0,"matchedTradingVolume":1.529976E8},{"month":10,"value":17.75,"matchedTradingVolume":1.780465E8},{"month":11,"value":18.95,"matchedTradingVolume":1.868925E8},{"month":12,"value":20.3,"matchedTradingVolume":1.556088E8}],"dividendSpitingHistories":[{"month":5,"value":1000.0}]},{"symbol":"HPG","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":22.1,"matchedTradingVolume":4.281135E8},{"month":2,"value":21.9,"matchedTradingVolume":4.94953E8},{"month":3,"value":21.3,"matchedTradingVolume":4.610696E8},{"month":4,"value":22.0,"matchedTradingVolume":3.30845E8},{"month":5,"value":22.35,"matchedTradingVolume":3.350429E8},{"month":6,"value":26.6,"matchedTradingVolume":5.626958E8},{"month":7,"value":28.4,"matchedTradingVolume":4.653832E8},{"month":8,"value":28.15,"matchedTradingVolume":6.43047E8},{"month":9,"value":29.0,"matchedTradingVolume":6.05131E8},{"month":10,"value":26.2,"matchedTradingVolume":4.011388E8},{"month":11,"value":27.2,"matchedTradingVolume":5.466178E8},{"month":12,"value":27.95,"matchedTradingVolume":5.610034E8}],"dividendSpitingHistories":[]},{"symbol":"MBB","companyName":"Ngân hàng TMCP Quân Đội","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":1.510583E8},{"month":2,"value":18.95,"matchedTradingVolume":1.687588E8},{"month":3,"value":18.3,"matchedTradingVolume":1.717558E8},{"month":4,"value":18.8,"matchedTradingVolume":1.492544E8},{"month":5,"value":18.85,"matchedTradingVolume":1.334826E8},{"month":6,"value":20.7,"matchedTradingVolume":2.836777E8},{"month":7,"value":21.2,"matchedTradingVolume":2.36432E8},{"month":8,"value":19.35,"matchedTradingVolume":2.173509E8},{"month":9,"value":19.4,"matchedTradingVolume":2.572516E8},{"month":10,"value":18.6,"matchedTradingVolume":1.466942E8},{"month":11,"value":18.55,"matchedTradingVolume":1.853708E8},{"month":12,"value":18.65,"matchedTradingVolume":1.511428E8}],"dividendSpitingHistories":[{"month":6,"value":500.0}]},{"symbol":"MSN","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":103.7,"matchedTradingVolume":8950100.0},{"month":2,"value":96.7,"matchedTradingVolume":1.24483E7},{"month":3,"value":84.7,"matchedTradingVolume":2.91468E7},{"month":4,"value":79.5,"matchedTradingVolume":2.07545E7},{"month":5,"value":74.4,"matchedTradingVolume":1.62996E7},{"month":6,"value":78.8,"matchedTradingVolume":3.0083E7},{"month":7,"value":87.3,"matchedTradingVolume":3.79388E7},{"month":8,"value":89.2,"matchedTradingVolume":5.02759E7},{"month":9,"value":82.7,"matchedTradingVolume":3.77362E7},{"month":10,"value":77.4,"matchedTradingVolume":4.0633E7},{"month":11,"value":66.0,"matchedTradingVolume":3.84334E7},{"month":12,"value":67.5,"matchedTradingVolume":5.12021E7}],"dividendSpitingHistories":[]},{"symbol":"MWG","companyName":"CTCP Đầu tư Thế giới Di động","type":"VN30","year":2023,"prices":[{"month":1,"value":46.5,"matchedTradingVolume":3.38651E7},{"month":2,"value":49.9,"matchedTradingVolume":4.56642E7},{"month":3,"value":40.8,"matchedTradingVolume":4.16636E7},{"month":4,"value":41.05,"matchedTradingVolume":5.23766E7},{"month":5,"value":39.4,"matchedTradingVolume":3.71724E7},{"month":6,"value":44.35,"matchedTradingVolume":8.65595E7},{"month":7,"value":54.5,"matchedTradingVolume":1.189389E8},{"month":8,"value":54.2,"matchedTradingVolume":1.698499E8},{"month":9,"value":57.5,"matchedTradingVolume":1.511657E8},{"month":10,"value":51.9,"matchedTradingVolume":1.695161E8},{"month":11,"value":41.9,"matchedTradingVolume":2.478952E8},{"month":12,"value":43.05,"matchedTradingVolume":1.675436E8}],"dividendSpitingHistories":[{"month":7,"value":500.0}]},{"symbol":"PLX","companyName":"Tập đoàn Xăng Dầu Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":38.1,"matchedTradingVolume":1.25733E7},{"month":2,"value":40.6,"matchedTradingVolume":1.61479E7},{"month":3,"value":39.0,"matchedTradingVolume":2.69045E7},{"month":4,"value":38.05,"matchedTradingVolume":1.50825E7},{"month":5,"value":38.05,"matchedTradingVolume":1.33605E7},{"month":6,"value":39.1,"matchedTradingVolume":1.56871E7},{"month":7,"value":41.8,"matchedTradingVolume":3.82708E7},{"month":8,"value":41.0,"matchedTradingVolume":3.29293E7},{"month":9,"value":40.4,"matchedTradingVolume":2.22712E7},{"month":10,"value":37.5,"matchedTradingVolume":2.2156E7},{"month":11,"value":35.8,"matchedTradingVolume":1.91929E7},{"month":12,"value":35.9,"matchedTradingVolume":1.31123E7}],"dividendSpitingHistories":[{"month":9,"value":700.0}]},{"symbol":"POW","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":12.4,"matchedTradingVolume":1.438163E8},{"month":2,"value":12.65,"matchedTradingVolume":1.506917E8},{"month":3,"value":13.5,"matchedTradingVolume":2.060467E8},{"month":4,"value":13.65,"matchedTradingVolume":1.477345E8},{"month":5,"value":13.65,"matchedTradingVolume":1.43022E8},{"month":6,"value":13.95,"matchedTradingVolume":1.552269E8},{"month":7,"value":13.7,"matchedTradingVolume":1.968232E8},{"month":8,"value":14.1,"matchedTradingVolume":2.620184E8},{"month":9,"value":13.0,"matchedTradingVolume":1.309333E8},{"month":10,"value":11.75,"matchedTradingVolume":1.067952E8},{"month":11,"value":11.9,"matchedTradingVolume":1.264731E8},{"month":12,"value":11.65,"matchedTradingVolume":8.40602E7}],"dividendSpitingHistories":[]},{"symbol":"SAB","companyName":"Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn","type":"VN30","year":2023,"prices":[{"month":1,"value":193.1,"matchedTradingVolume":2013100.0},{"month":2,"value":197.2,"matchedTradingVolume":1559600.0},{"month":3,"value":192.5,"matchedTradingVolume":3412700.0},{"month":4,"value":181.0,"matchedTradingVolume":3651800.0},{"month":5,"value":166.6,"matchedTradingVolume":2221900.0},{"month":6,"value":162.0,"matchedTradingVolume":3096200.0},{"month":7,"value":161.6,"matchedTradingVolume":3568900.0},{"month":8,"value":161.6,"matchedTradingVolume":6019000.0},{"month":9,"value":168.9,"matchedTradingVolume":9361900.0},{"month":10,"value":73.0,"matchedTradingVolume":9713900.0},{"month":11,"value":66.2,"matchedTradingVolume":1.61096E7},{"month":12,"value":65.6,"matchedTradingVolume":1.22324E7}],"dividendSpitingHistories":[{"month":3,"value":1000.0},{"month":6,"value":1500.0}]},{"symbol":"SHB","companyName":"Ngân hàng TMCP Sài Gòn - Hà Nội","type":"VN30","year":2023,"prices":[{"month":1,"value":11.2,"matchedTradingVolume":2.939803E8},{"month":2,"value":10.6,"matchedTradingVolume":2.209531E8},{"month":3,"value":10.85,"matchedTradingVolume":3.662555E8},{"month":4,"value":12.2,"matchedTradingVolume":6.056328E8},{"month":5,"value":12.0,"matchedTradingVolume":4.061201E8},{"month":6,"value":12.85,"matchedTradingVolume":6.039741E8},{"month":7,"value":14.4,"matchedTradingVolume":4.546979E8},{"month":8,"value":13.45,"matchedTradingVolume":4.740001E8},{"month":9,"value":12.75,"matchedTradingVolume":4.439107E8},{"month":10,"value":11.05,"matchedTradingVolume":2.494628E8},{"month":11,"value":11.6,"matchedTradingVolume":3.637048E8},{"month":12,"value":11.15,"matchedTradingVolume":3.281995E8}],"dividendSpitingHistories":[]},{"symbol":"SSI","companyName":"CTCP Chứng khoán SSI","type":"VN30","year":2023,"prices":[{"month":1,"value":21.6,"matchedTradingVolume":2.43128E8},{"month":2,"value":20.75,"matchedTradingVolume":2.701936E8},{"month":3,"value":21.5,"matchedTradingVolume":3.972755E8},{"month":4,"value":22.6,"matchedTradingVolume":4.024856E8},{"month":5,"value":23.4,"matchedTradingVolume":3.739481E8},{"month":6,"value":26.6,"matchedTradingVolume":4.523384E8},{"month":7,"value":29.75,"matchedTradingVolume":3.768438E8},{"month":8,"value":33.5,"matchedTradingVolume":6.115069E8},{"month":9,"value":36.45,"matchedTradingVolume":5.979921E8},{"month":10,"value":34.0,"matchedTradingVolume":5.601314E8},{"month":11,"value":32.9,"matchedTradingVolume":5.212175E8},{"month":12,"value":33.6,"matchedTradingVolume":3.923282E8}],"dividendSpitingHistories":[{"month":6,"value":1000.0}]},{"symbol":"STB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":27.1,"matchedTradingVolume":2.330793E8},{"month":2,"value":26.15,"matchedTradingVolume":3.772336E8},{"month":3,"value":26.5,"matchedTradingVolume":4.59574E8},{"month":4,"value":26.9,"matchedTradingVolume":3.08058E8},{"month":5,"value":28.15,"matchedTradingVolume":3.174901E8},{"month":6,"value":30.3,"matchedTradingVolume":3.506546E8},{"month":7,"value":30.0,"matchedTradingVolume":4.686863E8},{"month":8,"value":32.9,"matchedTradingVolume":6.076624E8},{"month":9,"value":33.3,"matchedTradingVolume":4.282722E8},{"month":10,"value":31.75,"matchedTradingVolume":3.745102E8},{"month":11,"value":30.2,"matchedTradingVolume":3.661731E8},{"month":12,"value":28.55,"matchedTradingVolume":3.171983E8}],"dividendSpitingHistories":[]},{"symbol":"TCB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":29.4,"matchedTradingVolume":6.18252E7},{"month":2,"value":28.6,"matchedTradingVolume":6.10217E7},{"month":3,"value":28.35,"matchedTradingVolume":6.78293E7},{"month":4,"value":30.7,"matchedTradingVolume":9.0173E7},{"month":5,"value":30.5,"matchedTradingVolume":6.91356E7},{"month":6,"value":33.3,"matchedTradingVolume":1.050967E8},{"month":7,"value":34.3,"matchedTradingVolume":1.146862E8},{"month":8,"value":35.3,"matchedTradingVolume":1.43969E8},{"month":9,"value":35.75,"matchedTradingVolume":1.089254E8},{"month":10,"value":33.15,"matchedTradingVolume":7.11959E7},{"month":11,"value":31.8,"matchedTradingVolume":7.9431E7},{"month":12,"value":31.8,"matchedTradingVolume":5.98825E7}],"dividendSpitingHistories":[]},{"symbol":"TPB","companyName":"Ngân hàng TMCP Tiên Phong","type":"VN30","year":2023,"prices":[{"month":1,"value":25.0,"matchedTradingVolume":1.168169E8},{"month":2,"value":24.8,"matchedTradingVolume":1.293128E8},{"month":3,"value":25.3,"matchedTradingVolume":9.12826E7},{"month":4,"value":23.8,"matchedTradingVolume":8.51845E7},{"month":5,"value":25.0,"matchedTradingVolume":6.7704E7},{"month":6,"value":26.3,"matchedTradingVolume":1.226153E8},{"month":7,"value":19.0,"matchedTradingVolume":1.497795E8},{"month":8,"value":19.6,"matchedTradingVolume":1.981773E8},{"month":9,"value":19.75,"matchedTradingVolume":1.483994E8},{"month":10,"value":17.5,"matchedTradingVolume":9.66153E7},{"month":11,"value":17.7,"matchedTradingVolume":1.206297E8},{"month":12,"value":17.55,"matchedTradingVolume":1.051146E8}],"dividendSpitingHistories":[{"month":3,"value":2500.0}]},{"symbol":"VCB","companyName":"Ngân hàng TMCP Ngoại thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":93.0,"matchedTradingVolume":1.95707E7},{"month":2,"value":96.0,"matchedTradingVolume":1.77834E7},{"month":3,"value":93.2,"matchedTradingVolume":2.03676E7},{"month":4,"value":92.8,"matchedTradingVolume":1.05433E7},{"month":5,"value":95.0,"matchedTradingVolume":1.21852E7},{"month":6,"value":105.0,"matchedTradingVolume":1.97517E7},{"month":7,"value":106.5,"matchedTradingVolume":2.00989E7},{"month":8,"value":91.5,"matchedTradingVolume":3.03631E7},{"month":9,"value":90.2,"matchedTradingVolume":2.82153E7},{"month":10,"value":86.8,"matchedTradingVolume":1.90875E7},{"month":11,"value":89.5,"matchedTradingVolume":2.49941E7},{"month":12,"value":86.0,"matchedTradingVolume":2.70841E7}],"dividendSpitingHistories":[]},{"symbol":"VHM","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":53.3,"matchedTradingVolume":2.15012E7},{"month":2,"value":48.1,"matchedTradingVolume":5.98349E7},{"month":3,"value":51.5,"matchedTradingVolume":5.67558E7},{"month":4,"value":52.6,"matchedTradingVolume":3.09891E7},{"month":5,"value":55.5,"matchedTradingVolume":3.01862E7},{"month":6,"value":57.0,"matchedTradingVolume":3.66415E7},{"month":7,"value":63.0,"matchedTradingVolume":5.51829E7},{"month":8,"value":63.0,"matchedTradingVolume":1.229843E8},{"month":9,"value":55.9,"matchedTradingVolume":1.448709E8},{"month":10,"value":48.0,"matchedTradingVolume":1.006912E8},{"month":11,"value":42.9,"matchedTradingVolume":1.672199E8},{"month":12,"value":43.7,"matchedTradingVolume":1.506395E8}],"dividendSpitingHistories":[]},{"symbol":"VIB","companyName":"Ngân hàng TMCP Quốc tế Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":23.55,"matchedTradingVolume":6.51873E7},{"month":2,"value":24.3,"matchedTradingVolume":6.42993E7},{"month":3,"value":21.4,"matchedTradingVolume":8.48303E7},{"month":4,"value":22.1,"matchedTradingVolume":7.98868E7},{"month":5,"value":21.6,"matchedTradingVolume":9.82021E7},{"month":6,"value":23.6,"matchedTradingVolume":1.718345E8},{"month":7,"value":21.0,"matchedTradingVolume":9.72921E7},{"month":8,"value":21.4,"matchedTradingVolume":1.057553E8},{"month":9,"value":21.7,"matchedTradingVolume":1.414188E8},{"month":10,"value":19.65,"matchedTradingVolume":7.06346E7},{"month":11,"value":19.65,"matchedTradingVolume":6.65855E7},{"month":12,"value":19.65,"matchedTradingVolume":7.1574E7}],"dividendSpitingHistories":[{"month":2,"value":1000.0},{"month":4,"value":500.0}]},{"symbol":"VIC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":59.2,"matchedTradingVolume":2.56029E7},{"month":2,"value":56.0,"matchedTradingVolume":3.974E7},{"month":3,"value":55.0,"matchedTradingVolume":3.25647E7},{"month":4,"value":58.0,"matchedTradingVolume":4.44255E7},{"month":5,"value":54.4,"matchedTradingVolume":3.62615E7},{"month":6,"value":54.1,"matchedTradingVolume":4.21094E7},{"month":7,"value":55.1,"matchedTradingVolume":6.40446E7},{"month":8,"value":75.6,"matchedTradingVolume":3.762692E8},{"month":9,"value":62.3,"matchedTradingVolume":2.936844E8},{"month":10,"value":46.9,"matchedTradingVolume":1.483437E8},{"month":11,"value":45.4,"matchedTradingVolume":9.69235E7},{"month":12,"value":44.6,"matchedTradingVolume":6.27363E7}],"dividendSpitingHistories":[]},{"symbol":"VJC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":116.3,"matchedTradingVolume":5537500.0},{"month":2,"value":113.9,"matchedTradingVolume":5160700.0},{"month":3,"value":108.9,"matchedTradingVolume":6564900.0},{"month":4,"value":103.0,"matchedTradingVolume":3872700.0},{"month":5,"value":99.5,"matchedTradingVolume":1.26274E7},{"month":6,"value":97.7,"matchedTradingVolume":1.6206E7},{"month":7,"value":102.0,"matchedTradingVolume":1.96767E7},{"month":8,"value":103.0,"matchedTradingVolume":2.02222E7},{"month":9,"value":101.9,"matchedTradingVolume":2.19183E7},{"month":10,"value":105.2,"matchedTradingVolume":2.09001E7},{"month":11,"value":113.0,"matchedTradingVolume":2.00095E7},{"month":12,"value":108.0,"matchedTradingVolume":2.01093E7}],"dividendSpitingHistories":[]},{"symbol":"VNM","companyName":"CTCP Sữa Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":81.3,"matchedTradingVolume":2.71532E7},{"month":2,"value":77.5,"matchedTradingVolume":2.8004E7},{"month":3,"value":77.1,"matchedTradingVolume":3.09558E7},{"month":4,"value":74.7,"matchedTradingVolume":2.10868E7},{"month":5,"value":70.7,"matchedTradingVolume":3.00439E7},{"month":6,"value":71.9,"matchedTradingVolume":1.092673E8},{"month":7,"value":78.0,"matchedTradingVolume":9.18289E7},{"month":8,"value":77.9,"matchedTradingVolume":8.24544E7},{"month":9,"value":80.3,"matchedTradingVolume":5.63057E7},{"month":10,"value":75.8,"matchedTradingVolume":4.31485E7},{"month":11,"value":71.4,"matchedTradingVolume":4.87116E7},{"month":12,"value":70.0,"matchedTradingVolume":5.76954E7}],"dividendSpitingHistories":[{"month":8,"value":1500.0},{"month":8,"value":1500.0},{"month":12,"value":500.0}]},{"symbol":"VPB","companyName":"Ngân hàng TMCP Việt Nam Thịnh Vượng","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":3.624271E8},{"month":2,"value":18.5,"matchedTradingVolume":3.291333E8},{"month":3,"value":21.25,"matchedTradingVolume":4.78505E8},{"month":4,"value":21.4,"matchedTradingVolume":2.156825E8},{"month":5,"value":19.8,"matchedTradingVolume":1.600067E8},{"month":6,"value":20.25,"matchedTradingVolume":3.597209E8},{"month":7,"value":22.15,"matchedTradingVolume":4.10663E8},{"month":8,"value":22.65,"matchedTradingVolume":4.072212E8},{"month":9,"value":22.55,"matchedTradingVolume":3.543629E8},{"month":10,"value":22.7,"matchedTradingVolume":2.767039E8},{"month":11,"value":21.35,"matchedTradingVolume":2.212622E8},{"month":12,"value":19.65,"matchedTradingVolume":2.219054E8}],"dividendSpitingHistories":[{"month":11,"value":1000.0}]},{"symbol":"VRE","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":30.3,"matchedTradingVolume":2.95246E7},{"month":2,"value":29.6,"matchedTradingVolume":3.32765E7},{"month":3,"value":29.9,"matchedTradingVolume":7.12347E7},{"month":4,"value":29.6,"matchedTradingVolume":4.78106E7},{"month":5,"value":28.4,"matchedTradingVolume":5.91646E7},{"month":6,"value":27.45,"matchedTradingVolume":7.98341E7},{"month":7,"value":29.65,"matchedTradingVolume":1.388173E8},{"month":8,"value":31.5,"matchedTradingVolume":1.701563E8},{"month":9,"value":30.3,"matchedTradingVolume":9.07252E7},{"month":10,"value":27.45,"matchedTradingVolume":7.55509E7},{"month":11,"value":24.4,"matchedTradingVolume":1.089259E8},{"month":12,"value":23.65,"matchedTradingVolume":7.37884E7}],"dividendSpitingHistories":[]}]}'
    futureData = loadDataInput(jsonInput2023)
    cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance, cashEndMonth = genInvestmentPlan(futureData, None, None, None)
    individual = Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash,
                            fitnesses, aggregatedFitness, finalFitness, [], 0.0, frontier,
                            crowdingDistance, [0, 0, 0, 0, 0], cashEndMonth)
    prinfReSult(individual, 0, 0,
                [], [], [], futureData)
    printSolution(finalCash)
main()
