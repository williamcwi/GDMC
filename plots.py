import random
import numpy as np
from logger import Logger
from copy import deepcopy

logger = Logger('Plot')

def initialise(gridArray):
    # try:
        buildingDict = {
            "towncentre": [12,7],
            "simplehouse": [3,3],
            "bench": [1,1]
        }

        plotDict = {
            "towncentre": 1,
            "simplehouse": 9999,
            "bench": 9999
        }

        plotWeightingDict = {
            "towncentre": 100,
            "simplehouse": 50,
            "bench": 10
        }

        buildingNumDict = {}

        population_size = 10

        def getBuildableplot(individual):
            posArray = []
            pos = np.where(individual == 1)
            for x, z in zip(pos[0], pos[1]):
                posArray.append([x,z])
            return (posArray)

        def getRandomPlot(currentPlotWeightingDict, buildingDict, randomWeighting):
            for key in currentPlotWeightingDict: #FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
                randomWeighting -= currentPlotWeightingDict[key]
                if randomWeighting <= 0:
                    plotName = key #FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
                    plot = buildingDict[key] #FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
                    # logger.info(u'{} {}'.format(plot, plotName))
                    return plot, plotName
        
        def fitting(pos, plot):
            for x in range(plot[0]):
                for z in range(plot[1]):
                    if (pos[0] + x < len(individual) and pos[1] + z < len(individual[0])):
                        if ((individual[pos[0] + x][pos[1] + z])) != 1:
                            return False
                    else:
                        return False
            return True
        
        def placing(pos, plot, plotName, buildingNum):
            for x in range(plot[0]):
                for z in range(plot[1]):
                    individual[pos[0] + x][pos[1] + z] = buildingNum
            buildingNumDict[buildingNum] = plotName
            buildingNum += 1
            plotDict[plotName] -= 1
            if plotDict[plotName] == 0:
                plotWeightingDict[plotName] = 0
            return buildingNum

        population = []
        buildingNum = 100

        for pop in range(population_size):
            individual = deepcopy(gridArray)

            plotRemaining = len(getBuildableplot(individual))
            while plotRemaining >= 1: # Generating each individual
                buildablePlotPos = getBuildableplot(individual)
                pos = buildablePlotPos[(random.randint(0, len(buildablePlotPos)-1))]
                currentPlotWeightingDict = dict(plotWeightingDict)
                totalWeighting = sum(currentPlotWeightingDict.values())
                randomWeighting = random.randint(0, totalWeighting)
                plot, plotName = getRandomPlot(currentPlotWeightingDict, buildingDict, randomWeighting)
                isFit = (fitting(pos, plot))
                # logger.info(u'trying {} {}'.format(pos, plotName))
                times = 0

                while not isFit:
                    currentPlotWeightingDict[plotName] = 0 # remove weighting from dict
                    totalWeighting = sum(currentPlotWeightingDict.values())
                    randomWeighting = random.randint(0, totalWeighting)
                    # logger.info(u'{} {} {}'.format(currentPlotWeightingDict, totalWeighting, randomWeighting))
                    plot, plotName = getRandomPlot(currentPlotWeightingDict, buildingDict, randomWeighting) # get another random plot
                    isFit = (fitting(pos, plot))
                    times += 1
                    # logger.info(u'try again - {} {} {}'.format(times, pos, plotName))

                buildingNum = placing(pos, plot, plotName, buildingNum)
                # logger.info(u'placed {} {}'.format(pos, plotName))
                plotRemaining = len(getBuildableplot(individual))
                
            population.append(individual)
        return population, buildingNumDict
    # except Exception as e:
    #     logger.error(e)

def evaluate():
    try:
        pass
    except Exception as e:
        logger.error(e)

def select():
    try:
        pass
    except Exception as e:
        logger.error(e)

def crossover():
    try:
        pass
    except Exception as e:
        logger.error(e)

def mutation():
    try:
        pass
    except Exception as e:
        logger.error(e)

def run(gridArray):
    # try:
        pop, buildingNumDict = initialise(gridArray)
        logger.info(pop)

    # except Exception as e:
    #     logger.error(e)