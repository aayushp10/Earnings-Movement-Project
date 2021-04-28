import requests
import json
import pandas as pd
import math
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

from datetime import datetime
from ComprableAnalysis import ComprableAnalysis

FMP_CLOUD_API_KEY = "0d86afa66dcb2ff483d4be6c646f2710"
FMP_API_PARAM = "?apikey=" + FMP_CLOUD_API_KEY

FMP_BASE_URL = "https://fmpcloud.io/api/v3"
FMP_HISTORICAL_EARNINGS = "/historical/earning_calendar/"

class EarningsMovement:
    def __init__(self, tickers):
        self.tickers = tickers


    def loadRevenueData(self):
        sectorMapping = pd.read_csv("RevenuesMovementData.csv")
        # sectorMapping.set_index('Ticker', inplace=True)
        sectors = sectorMapping.Sector.unique()
        #sectorMapping.iloc[ticker].Sector

        df = pd.read_csv("RevenueTable.csv")

        revenueTickers = df.columns.tolist()
        print(revenueTickers)
        # print(df)
        for ticker in revenueTickers:
            if(ticker != 'Quarter'):
                df[ticker] = df[ticker].pct_change()

        accuracies = df.iloc[1::2, :]
        accuracies.drop(['Quarter'], axis=1, inplace=True)
        accuracies.reset_index(inplace=True)
        accuracies.drop(['index'], axis=1, inplace=True)

        print(accuracies)
        corrs = []
        for sector in sectors:
            temp = sectorMapping[sectorMapping['Sector'] == sector]
            tickers = temp.Ticker.unique()
            actualTickers = []
            print(tickers)
            for tick in tickers:
                if(tick in revenueTickers):
                    actualTickers.append(tick)
            if(len(actualTickers) > 0):
                corrs.append(accuracies[actualTickers].corr(method='pearson'))

        ComprableAnalysis([]).plotCorrelationsOfRevenue(corrs)

    def loadMovementData(self):
        df = pd.read_csv("EarningsMovementData.csv")
        sectors = df.Sector.unique()
        ticker2DArray = []
        for sector in sectors:
            temp = df[df['Sector'] == sector]
            tickers = temp['Ticker']
            ticker2DArray.append(tickers)
        return ticker2DArray

    def getEarningsData(self, ticker):

        r = requests.get(FMP_BASE_URL + FMP_HISTORICAL_EARNINGS + ticker + FMP_API_PARAM)
        r = json.loads(r.content)
        r = pd.read_json(json.dumps(r))

        r['eps_accuracy'] = ( r['eps'] - r['epsEstimated'])/r['epsEstimated']
        r['date'] = r['date'].transform(lambda x: x.to_pydatetime())
        end_date = "2020-07-01"
        before_end_date = r["date"] < end_date
        r = r.loc[before_end_date]
        r = r[3:13]


        for index, row in r.iterrows():

            if(row.eps == row.epsEstimated):
                r.at[index, 'beat'] = 0

            if(row.eps > row.epsEstimated):
                r.at[index, 'beat'] = 1
                if(row.eps_accuracy < 0):
                    eps_accuracy = -1* row.eps_accuracy
                    r.at[index, 'eps_accuracy'] = eps_accuracy

            if(row.eps < row.epsEstimated):
                r.at[index, 'beat'] = -1
                if (row.eps_accuracy > 0):
                    eps_accuracy = -1 * row.eps_accuracy
                    r.at[index, 'eps_accuracy'] = eps_accuracy



        # r['beat'] = 1 if r['eps_accuracy'] > 0 else 0
        print(r)
        return r




    def getEPSCorrelationMap(self):
        stockEPS = pd.DataFrame()
        for ticker in self.tickers:
            stockEPS[ticker] = self.getEarningsData(ticker)['eps_accuracy']
        for ticker in self.tickers:
            stockEPS = stockEPS[stockEPS[ticker].notna()]
        # print(stockEPS)
        ComprableAnalysis(self.tickers).EPSCorrelation(stockEPS)

    def getEPSCorrelationMapVariable(self, tickers):
        stockEPS = pd.DataFrame()
        for ticker in tickers:
            stockEPS[ticker] = self.getEarningsData(ticker)['eps_accuracy']
        for ticker in tickers:
            stockEPS = stockEPS[stockEPS[ticker].notna()]
        # print(stockEPS)

        # print(stockEPS)
        #when switching to accuracy turn off ovariance
        corrMatricesForTickers = ComprableAnalysis(tickers).EPSCorrelation(stockEPS, covariance=False)

        return corrMatricesForTickers

    def allHeatMaps(self):
        ticker2DArray = self.loadMovementData()
        corrMatrix2DArray = []
        for tickerArray in ticker2DArray:
            t = self.getEPSCorrelationMapVariable(tickerArray)
            corrMatrix2DArray.append(t)
        ComprableAnalysis(tickerArray).plotAllCorrelations(corrMatrix2DArray)



em = EarningsMovement(['AMZN', 'UPS', 'SHOP', 'SQ', 'W', 'ETSY', 'FDX'])
# print(em.getEarningsData('FDX'))
# em.getEPSCorrelationMap()

em.allHeatMaps()

# em.loadRevenueData()

