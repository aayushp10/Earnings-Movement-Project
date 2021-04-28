import pandas_datareader as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import datetime as dt 
import seaborn as sb

class ComprableAnalysis:

    def __init__(self, tickers):
        self.tickers = tickers

    def getAdjClose(self, startDate, endDate):
        stockPrices = pd.DataFrame()
        for stock in self.tickers:
            stockPrices[stock] = web.DataReader(stock, 'yahoo', start=startDate, end=endDate)['Adj Close']
        stockPrices = stockPrices.reset_index()
        return stockPrices


    def stockCorrelation(self, startDate, endDate):
        stockPrices = self.getAdjClose(startDate, endDate)
        corrMatrix = stockPrices.corr(method='pearson')
        return corrMatrix

    def EPSCorrelation(self, df, covariance=False):
        print('IN EPS CORREKATION RIGHT BEFORE CORR FUNCTION')
        print(df)
        stockMatrix = self.stockCorrelation(startDate="2018-01-01", endDate="2020-06-01")
        if (covariance):

            return [df.cov(), stockMatrix]

        return [df.corr(method='pearson'), stockMatrix]


    def plotCorrelations(self, corrPlots):


        fig, axes = plt.subplots(ncols=2, figsize=(16, 8))
        ax1, ax2 = axes
        sb.heatmap(corrPlots[0], ax=ax1,cmap="RdBu_r", annot=True)
        sb.heatmap(corrPlots[1], ax=ax2, cmap="RdBu_r", annot=True)
        ax1.set_title('EPS Corr')
        ax2.set_title('Stock Corr')

        pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
        pdf.savefig(fig)
        pdf.close()
        # plt.show()


    def plotCorrelationsOfRevenue(self, corrArray):

        pdf = matplotlib.backends.backend_pdf.PdfPages("RevenueCorrs.pdf")

        for i in range(0, len(corrArray)):
            fig, axes = plt.subplots(figsize=(16, 16))
            ax1 = axes
            sb.heatmap(corrArray[i], ax=ax1, cmap="RdBu_r", annot=True)
            ax1.set_title('Revenue Corr')

            pdf.savefig(fig)

        pdf.close()
        print('DONE WITH PDF')
        # plt.show()




    def plotAllCorrelations(self, corrPlots2DArray):

        pdf = matplotlib.backends.backend_pdf.PdfPages("EPSBacktest3.pdf")

        for i in range(0, len(corrPlots2DArray)):


            try:
                fig, axes = plt.subplots(ncols=2, figsize=(32 , 16 ))
                ax1, ax2 = axes
                sb.heatmap(corrPlots2DArray[i][0], ax=ax1, cmap="RdBu_r", annot=True)
                sb.heatmap(corrPlots2DArray[i][1], ax=ax2, cmap="RdBu_r", annot=True)
                ax1.set_title('EPS Corr')
                ax2.set_title('Stock Corr')
                pdf.savefig(fig)
            except:
                print(i)
                print(corrPlots2DArray[0][0])
        pdf.close()

            # except:


                # print(corrPlots2DArray)




        print('DONE WITH PDF')
        # plt.show()


