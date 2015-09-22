#!/usr/bin/python

import sys
import logging
import random

class GenAlgException(Exception):
    """Informs about execution errors in genalg"""
    pass


class AbstractChromoson(object):
    _fitness = None

    def getFitness(self):
        return self._fitness

    def getId(self):
        raise GenAlgException("Abstract Method")

    def mutate(self):
        raise GenAlgException("Abstract Method")
        return 0

    def clone(self):
        raise GenAlgException("Abstract Method")

    def isCrossovered(self):
        raise GenAlgException("Abstract Method")

    def crossover(self, otherChromoson):
        raise GenAlgException("Abstract Method")
        return 0

    def isMutated(self):
        raise GenAlgException("Abstract Method") 


class ChromosonSelector(object):
    _chromoson = None
    _fitnessSum = None

    def __init__(self, chromoson, lastFitnessSum):
        self._chromoson = chromoson
        self._fitnessSum = lastFitnessSum + chromoson.getFitness()

    def getChromoson(self):
        return self._chromoson

    def getFitnessSum(self):
        return self._fitnessSum


class AbstractGenAlg(object):

    STEP_COUNT = 1
    WMUT = 0.05
    WCROSS = 0.3
    IS_ELITE_PROTECTED = True

    _step = 0
    _popsize = None
    _population = None
    _currentMaxFitness = 0.0
    _currentMinFitness = sys.maxint
    _currentMeanFitness = 0.0
    _totalMaxFitness = 0.0
    _totalMinFitness = sys.maxint
    _countCrossovers = 0
    _countTotalCrossovers = 0
    _countMutations = 0
    _countTotalMutations = 0
    _countImprovementsThroughCrossover = 0
    _countImprovementsThroughMutation = 0
    _countImprovementsThroughBoth = 0

    _verbose = False
    _debug = False

    def getCountCrossovers(self):
        return self._countCrossovers

    def getCountTotalCrossovers(self):
        return self._countTotalCrossovers

    def getCountMutations(self):
        return self._countMutations

    def getCountTotalMutations(self):
        return self._countTotalMutations

    def getStep(self):
        return self._step

    def getCurrentMaxFitness(self):
        return self._currentMaxFitness

    def getCurrentMinFitness(self):
        return self._currentMinFitness

    def getCurrentMeanFitness(self):
        return self._currentMeanFitness

    def getTotalMaxFitness(self):
        return self._totalMaxFitness

    def getTotalMinFitness(self):
        return self._totalMinFitness

    def setWMUT(self, wmut):
        self.WMUT = wmut

    def getWMUT(self):
        return self.WMUT

    def getPopsize(self):
        return self._popsize

    def setWCROSS(self, wcross):
        self.WCROSS = wcross

    def getWCROSS(self):
        return self.WCROSS

    def setIS_ELITE_PROTECTED(self, is_elite_protected):
        self.IS_ELITE_PROTECTED = is_elite_protected

    def getCountImprovementsThroughCrossover(self):
        return self._countImprovementsThroughCrossover

    def getCountImprovementsThroughMutation(self):
        return self._countImprovementsThroughMutation

    def getCountImprovementsThroughBoth(self):
        return self._countImprovementsThroughBoth

    def getFittest(self):
        fittest = None
        for chromoson in self._population:
            if fittest == None:
                fittest = chromoson
                continue
            elif chromoson.getFitness() > fittest.getFitness():
                fittest = chromoson

        return fittest

    def evolutePopulation(self):

        if len(self._population) == 0:
            raise GenAlgException("Population empty!")

        for i in range(self.STEP_COUNT):
            self._step += 1
            if self._verbose:
                logging.info("Start evolution: %s" % self._step)
                logging.info("Popsize: %s" % len(self._population))

            self._logPopulation('Start evolution')
            if self._step > 1:
                self._select()
                self._logPopulation('After selection')
            self._mutcross()
            self._logPopulation('After Mutation')
            self._setChromosonFitness()
            self._calcDifferentFitnessValues()
            self._countImprovement()

            self._logPopulation('End evolution')

    def _setChromosonFitness(self):
        pass

    def _countImprovement(self):
        fittest = self.getFittest()
        if fittest.isCrossovered() and fittest.isMutated():
            self._countImprovementsThroughBoth += 1
        elif fittest.isCrossovered():
            self._countImprovementsThroughCrossover += 1
        elif fittest.isMutated():
            self._countImprovementsThroughMutation += 1

    def _calcDifferentFitnessValues(self):

        self._currentMaxFitness = 0
        self._currentMinFitness = sys.maxint
        self._currentMeanFitness = 0

        for chromoson in self._population:
            fitness = chromoson.getFitness()
            self._currentMaxFitness = max(self._currentMaxFitness, fitness)
            self._currentMinFitness = min(self._currentMinFitness, fitness)
            self._currentMeanFitness += fitness

        self._totalMaxFitness = max(self._totalMaxFitness, self._currentMaxFitness)
        self._totalMinFitness = min(self._totalMinFitness, self._currentMinFitness)
        self._currentMeanFitness /= len(self._population)

        if self._debug:
            logging.debug("CurrentMaxFitness: %s" % self._currentMaxFitness)
            logging.debug("CurrentMinFitness: %s" % self._currentMinFitness)
            logging.debug("CurrentMeanFitness: %s" % self._currentMeanFitness)

            logging.debug("TotalMaxFitness: %s" % self._totalMaxFitness)
            logging.debug("TotalMinFitness: %s" % self._totalMinFitness)


            logging.debug("Crossovers: %s" % self._countCrossovers)
            logging.debug("TotalCrossovers: %s" % self._countTotalCrossovers)

            logging.debug("Mutation: %s" % self._countMutations)
            logging.debug("TotalMutations: %s" % self._countTotalMutations)


    def _mutcross(self):

        if self._verbose:
            logging.info("Start mutcross: %s" % self._step)
        self._countCrossovers = 0
        self._countMutations = 0

        for chromoson in self._population[1:]:

            self._countMutations += chromoson.mutate()
            if (not chromoson.isCrossovered()) and (random.random() <= self.WCROSS):
                crossoverPartner = self._getCrossoverPartner()
                chromoson.crossover(crossoverPartner)
                self._countCrossovers += 1

        self._countTotalMutations += self._countMutations
        self._countTotalCrossovers += self._countCrossovers 

    def _getCrossoverPartner(self):
        intervalStart = 0
        intervalEnd = len(self._population) - 1

        if self.IS_ELITE_PROTECTED:
            intervalStart = 1

        pos = random.randint(intervalStart, intervalEnd)
        return self._population[pos]

    def _select(self):

        if self._verbose:
            logging.info("Start select: %s" % self._step)

        # Create select list
        chromSelectorList = []
        firstChromSelector = ChromosonSelector(self._population[0], 0)
        chromSelectorList.append(firstChromSelector)

        lastFitnessSum = firstChromSelector.getFitnessSum()

        for chromoson in self._population[1:]:
            tmpChromSelector = ChromosonSelector(chromoson, lastFitnessSum)
            chromSelectorList.append(tmpChromSelector)
            lastFitnessSum = tmpChromSelector.getFitnessSum()

        maxFit = chromSelectorList[-1].getFitnessSum()
       
        # Best chromoson first in new population
        for i in range(len(self._population)):
            if(self._population[0].getFitness() < self._population[i].getFitness()):
                self._population[0] = self._population[i].clone()

        if self._debug:
            logging.debug("Best fitness: %s" % self._population[0].getFitness())
            logging.debug("Best chromoson: %s" % self._population[0])

        # Elite protection
        startPosition = 1
        if self.IS_ELITE_PROTECTED and len(self._population) > 1:
            self._population[1] = self._population[0].clone() 
            startPosition = 2

        for i in range(startPosition, len(self._population)):
            tmpFitness = random.random() * maxFit
            for j in range(len(self._population)):
                if chromSelectorList[j].getFitnessSum() >= tmpFitness:
                    self._population[i] = chromSelectorList[j].getChromoson().clone()
                    break

    def getPopulation(self):
        return self._population

    def getSTEP_COUNT(self):
        return self.STEP_COUNT

    def setSTEP_COUNT(self, step_count):
        self.STEP_COUNT = step_count

    def getWorst(self):
        worst = None
        for chromoson in self._population:
            if worst == None:
                worst = chromoson
                continue

            if chromoson.getFitness() < worst.getFitness():
                worst = chromoson

        return worst

    def _logPopulation(self, tag):
        if self._verbose:
            logging.info("Logging current population... (%s)" % tag)
            i = 1
            maxPos = len(str(len(self._population)))
            for chromoson in self._population:
                logging.info("%s. Id: %s; Fitness: %s" % (str(i).zfill(maxPos), chromoson.getId(), chromoson.getFitness()))
                i += 1

