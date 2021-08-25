import pandas as pd
import talib as ta
import numpy as np
from ta.momentum import stochrsi_d,stochrsi_k
import math
def StochRSIMACD(prediction1,CloseStream,signal1,signal2):
    Close = np.array(CloseStream)
    fastd = np.array(stochrsi_d(pd.Series(CloseStream)))
    fastk = np.array(stochrsi_k(pd.Series(CloseStream)))
    RSI = ta.RSI(Close)
    macd, macdsignal, macdhist = ta.MACD(Close)
    ##buy signal
    if fastk[-1] <=20 and fastd[-1] <=20:
        signal1 = 1
    elif fastk[-1] >=80 and fastd[-1] >=80:
        signal1 = 0

    if signal1 ==1:
        if RSI[-1]>50:
            if macdsignal[-1]<macd[-1]:
                signal2=1
    elif signal1 == 0:
        if RSI[-1]<50:
            if macdsignal[-1] > macd[-1]:
                signal2=0

    if signal1 == signal2 == 0:
        if fastk[-1] >= 20 and fastd[-1] >= 20:
            prediction1=0
        else:
            signal1=-99
            signal2 = -99

    elif signal1 == signal2 == 1:
        if fastk[-1] <=80 and fastd[-1] <=80:
            prediction1=1
        else:
            signal1=-99
            signal2 = -99

    return prediction1,signal1,signal2,2


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def tripleEMAStochasticRSIATR(CloseStream,signal1,signal2,prediction1):
    newOrder = 0
    Close = np.array(CloseStream)
    EMA50 = ta.EMA(Close,timeperiod=50)
    EMA14 = ta.EMA(Close,timeperiod=14)
    EMA8 = ta.EMA(Close,timeperiod=8)
    fastd = np.array(stochrsi_d(pd.Series(CloseStream)))
    fastk = np.array(stochrsi_k(pd.Series(CloseStream)))
    ##buy signal
    if (Close[-1]>EMA8[-1]>EMA14[-1]>EMA50[-1]) and ((fastk[-1]>fastd[-1]) and (fastk[-2]<fastd[-2])): #and (fastk[-1]<80 and fastd[-1]<80):
        signal1=1
    elif (Close[-1]<EMA8[-1]<EMA14[-1]<EMA50[-1]) and ((fastk[-1]<fastd[-1]) and (fastk[-2]>fastd[-2])) : #and (fastk[-1]>20 and fastd[-1]>20):
        signal1=0
    else:
        signal1=-99

    if signal1 == 0:
        prediction1=0
    elif signal1 == 1:
        prediction1=1
    return  prediction1, signal1, signal2, 1

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


def Fractal(CloseStream,LowStream,HighStream,signal1,prediction1):
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)

    RSI = ta.RSI(Close)
    EMA50 = ta.EMA(Close, timeperiod=50)
    EMA20 = ta.EMA(Close, timeperiod=20)

    if High[-5]<High[-4]<High[-3] and High[-3]>High[-2]>High[-1]:
        signal1=0
    elif Low[-5]>Low[-4]>Low[-3] and Low[-3]<Low[-2]<Low[-1]:
        signal1=1
    else:
        signal1=-99



    if signal1 and EMA50[-1]<Low[-1]<EMA20[-1]:
        prediction1=1
    elif signal1==0 and EMA50[-1]>High[-1]>EMA20[-1]:
        prediction1=0
    else:
        signal1=-99
        prediction1=-99



    return prediction1,1

def Fractal2(CloseStream,LowStream,HighStream,signal1,prediction1):
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)

    RSI = ta.RSI(Close)
    EMA200 = ta.EMA(Close, timeperiod=200)
    #EMA100 = ta.EMA(Close, timeperiod=100)
    EMA50 = ta.EMA(Close, timeperiod=50)
    EMA21 = ta.EMA(Close, timeperiod=21)

    if Close[-5]<Close[-4]<Close[-3] and Close[-3]>Close[-2]>Close[-1]:
        signal1=0
    elif Close[-5]>Close[-4]>Close[-3] and Close[-3]<Close[-2]<Close[-1]:
        signal1=1
    else:
        signal1=-99



    if signal1 and EMA200[-1]<EMA50[-1]<EMA21[-1]<Close[-1] and RSI[-1]>50:
        prediction1=1
    elif signal1==0 and Close[-1]>EMA200[-1]>EMA50[-1]>EMA21[-1] and RSI[-1]<50:
        prediction1=0
    else:
        signal1=-99
        prediction1=-99



    return prediction1,3


def MovingAverage(CloseStream,prediction1):
    Close = np.array(CloseStream)

    EMA9 = ta.EMA(Close,timeperiod=9)
    SMA9 = ta.EMA(Close, timeperiod=11)

    if EMA9[-1]<SMA9[-1] and SMA9[-2]<EMA9[-2]:# and EMA9[-1]<SMA13[-1] and SMA13[-2]<EMA9[-2]:
        prediction1=0
        newOrder=1
    elif EMA9[-1]>SMA9[-1] and SMA9[-2]>EMA9[-2]:# and EMA9[-1]>SMA13[-1] and SMA13[-2]>EMA9[-2]:
        prediction1=1
        newOrder=1
    else:
        prediction1=-99

    return prediction1,1


def UltOscMACD(prediction1,CloseStream,HighStream,LowStream,signal1,signal2,HighestUlt,Highest):
    newOrder=0
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)
    ULT = ta.ULTOSC(High,Low,Close)

    if ULT[-1]>HighestUlt and ULT[-1]>70:
        signal1=0
        HighestUlt = ULT[-1]
        Highest = High[-1]
    elif ULT[-1]<HighestUlt and ULT[-1]<30:
        signal1=1
        HighestUlt = ULT[-1]
        Highest = Low[-1]

    ##Bearish Divergence
    if signal1==0 and ULT[-1]<HighestUlt and High[-1]>Highest:
        signal2=0

    ##Bullish Divergence
    elif signal1==1 and ULT[-1]>HighestUlt and Low[-1]<Highest:
        signal2=1


    RSI = ta.RSI(Close)
    macd, macdsignal, macdhist = ta.MACD(Close)



    if signal2 ==1 and RSI[-1]>50:# and macdsignal[-1]<macd[-1]:
        prediction1=1
        signal1=-99
        signal2=-99
    elif signal2 == 0 and RSI[-1]<50:# and macdsignal[-1] > macd[-1]:
        prediction1=0
        signal1 = -99
        signal2 = -99



    return prediction1,signal1,signal2,HighestUlt,Highest,1


def RSIStochEMA200(prediction1,CloseStream,HighStream,LowStream,signal1,signal2,currentPos):
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)
    fastd = np.array(stochrsi_d(pd.Series(CloseStream)))
    fastk = np.array(stochrsi_k(pd.Series(CloseStream)))
    RSI = ta.RSI(Close)
    EMA200 = ta.EMA(Close,timeperiod=200)
    EMA50 = ta.EMA(Close,timeperiod=50)
    largestRSI=RSI[len(RSI)-16]
    largestLow=Close[len(Close)-16] #Low[len(Low)-51] #Close[len(Close)-51]
    for i in range(len(RSI)-15,len(RSI)):
        if Close[i]>largestLow and Close[-1]>EMA200[-1]:
            largestLow=Close[i] ##Low
            if RSI[i]<largestRSI:
                ##Higher Low & Lower RSI => Bullish Divergence
                signal1=1
            largestRSI=RSI[i]
        elif Close[i]<largestLow and Close[-1]<EMA200[-1]:
            largestLow=Close[i] ##High
            if RSI[i]>largestRSI:
                ##Lower High & Higher RSI => Bearish Divergence
                signal1=0
            largestRSI=RSI[i]
    ##Bullish Divergence
    if signal1==1 and fastk[-1]>fastd[-1] and fastk[-2]<fastd[-2] and Close[-1]>EMA200[-1] and Close[-1]>EMA50[-1]:
        prediction1=1
        signal1=-99

    ##Bearish Divergence
    elif signal1==0 and fastk[-1]<fastd[-1] and fastk[-2]>fastd[-2] and Close[-1]<EMA200[-1] and Close[-1]<EMA50[-1]:
        prediction1=0
        signal1=-99

    if currentPos!=-99:
        signal1=-99
        signal2=-99

    return prediction1, signal1, 4


##############################################################################################################

def stochBB(prediction1,CloseStream):
    Close = np.array(CloseStream)

    fastd = np.array(stochrsi_d(pd.Series(CloseStream)))
    fastk = np.array(stochrsi_k(pd.Series(CloseStream)))

    #print(fastd[-1],fastk[-1])
    upperband, middleband, lowerband = ta.BBANDS(Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    percent_B= (Close[-1]-lowerband[-1])/(upperband[-1]-lowerband[-1]) #(Current Price - Lower Band) / (Upper Band - Lower Band)
    percent_B1 = (Close[-2]-lowerband[-2])/(upperband[-2]-lowerband[-2]) #(Current Price - Lower Band) / (Upper Band - Lower Band)
    percent_B2 = (Close[-3] - lowerband[-3]) / (upperband[-3] - lowerband[-3])  # (Current Price - Lower Band) / (Upper Band - Lower Band)
    percent_B3 = (Close[-4] - lowerband[-4]) / (upperband[-4] - lowerband[-4])  # (Current Price - Lower Band) / (Upper Band - Lower Band)
    #print(percent_B)
    if fastk[-1]<.2 and fastd[-1]<.2 and (fastk[-1]>fastd[-1] and fastk[-2]<fastd[-2])   and (percent_B<0 or percent_B1<0 or percent_B2<0 or percent_B3<0):# or percent_B2<.05):
        prediction1=1
    elif fastk[-1]>.8 and fastd[-1]>.8 and (fastk[-1]<fastd[-1] and fastk[-2]>fastd[-2])  and (percent_B>1 or percent_B1>1 or percent_B2>1 or percent_B3>1):# or percent_B2>1):
        prediction1=0

    return prediction1,6






def SARMACD200EMA(stoplossval, takeprofitval,CloseStream,HighStream,LowStream,prediction1,CurrentPos,signal1):
    newOrder=0
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)
    SAR=ta.SAR(High,Low,acceleration=.02,maximum=.2)
    EMA200 = ta.EMA(Close,timeperiod=200)
    macd, macdsignal, macdhist = ta.MACD(Close)

    if Close[-1]>EMA200[-1] and macd[-1]>macdsignal[-1] and macd[-2]<macdsignal[-2]:
        signal1=1
    elif Close[-1]<EMA200[-1] and macd[-1]<macdsignal[-1] and macd[-2]>macdsignal[-2]:
        signal1=0




    if signal1==1 and SAR[-1]<Close[-1] and macd[-1]>macdsignal[-1]:
        prediction1=1
        newOrder=1
    elif signal1==0 and SAR[-1]>Close[-1] and macd[-1]<macdsignal[-1]:
        prediction1=0
        newOrder=1


    if newOrder:
        Close = np.array(CloseStream)
        High = np.array(HighStream)
        Low = np.array(LowStream)
        ATR = ta.ATR(High, Low, Close, timeperiod=14)
        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = 2 * ATR[-1]
            takeprofitval = 5 * ATR[-1]
        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = 2 * ATR[-1]
            takeprofitval = 5 * ATR[-1]
        '''highswing = HighStream[-2]
        Lowswing = LowStream[-2]
        highflag = 0
        lowflag = 0
        for j in range(-3, -60, -1):
            if HighStream[j] > highswing and HighStream[j] > HighStream[j - 1] and HighStream[j] > HighStream[
                j - 2] and highflag == 0:
                highswing = HighStream[j]
                highflag = 1
            if LowStream[j] < Lowswing and LowStream[j] < LowStream[j - 1] and LowStream[j] < LowStream[
                j - 2] and lowflag == 0:
                Lowswing = LowStream[j]
                lowflag = 1

        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = (highswing - CloseStream[-1])
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2

        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = (CloseStream[-1] - Lowswing)
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2'''
        '''if prediction1 == 0 and CurrentPos == -99:
            stoplossval = SAR[-1] - CloseStream[-1]
            if stoplossval > 0.007 * CloseStream[-1]:
                stoplossval = 0.007 * CloseStream[-1]
            takeprofitval = 1.5*stoplossval
            signal1=-99

        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = CloseStream[-1] - SAR[-1]
            if stoplossval > 0.007*CloseStream[-1]:
                stoplossval = 0.007*CloseStream[-1]
            takeprofitval = 1.5*stoplossval
            signal1 = -99'''

    return takeprofitval,stoplossval,prediction1,signal1


def TripleEMA(stoplossval, takeprofitval,CloseStream,HighStream,LowStream,prediction1,CurrentPos,signal1):
    newOrder=0
    Close = np.array(CloseStream)
    High = np.array(HighStream)
    Low = np.array(LowStream)

    EMA10 = ta.EMA(Close,timeperiod=10)
    EMA20 = ta.EMA(Close, timeperiod=20)
    EMA50 = ta.EMA(Close, timeperiod=50)

    ##uptrend
    if (EMA10[-1]-EMA10[-5])/5>30 and (EMA20[-1]-EMA20[-5])/5>30 and (EMA50[-1]-EMA50[-5])/5>30:
        if Close[-1]>EMA10[-1] and Close[-2]<EMA10[-2]:
            newOrder=1
            prediction1=1
    ##downtrend
    elif (EMA10[-1]-EMA10[-5])/5<-30 and (EMA20[-1]-EMA20[-5])/5<-30 and (EMA50[-1]-EMA50[-5])/5<-30:
        if Close[-1]<EMA10[-1] and Close[-2]>EMA10[-2]:
            newOrder=1
            prediction1 = 0




    if newOrder:
        highswing = HighStream[-2]
        Lowswing = LowStream[-2]
        highflag = 0
        lowflag = 0
        for j in range(-3, -60, -1):
            if HighStream[j] > highswing and HighStream[j] > HighStream[j - 1] and HighStream[j] > HighStream[
                j - 2] and highflag == 0:
                highswing = HighStream[j]
                highflag = 1
            if LowStream[j] < Lowswing and LowStream[j] < LowStream[j - 1] and LowStream[j] < LowStream[
                j - 2] and lowflag == 0:
                Lowswing = LowStream[j]
                lowflag = 1

        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = (highswing - CloseStream[-1])
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2

        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = (CloseStream[-1] - Lowswing)
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2

    return takeprofitval, stoplossval, prediction1, signal1


def SetSLTP(stoplossval, takeprofitval,CloseStream,HighStream,LowStream,prediction1,CurrentPos,Type):
    ##Average True Range with multipliers
    if Type==1:
        Close = np.array(CloseStream)
        High = np.array(HighStream)
        Low = np.array(LowStream)
        ATR = ta.ATR(High, Low, Close, timeperiod=14)
        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = 1.5 * ATR[-1]
            takeprofitval = 8 * ATR[-1]
        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = 1.5 * ATR[-1]
            takeprofitval = 8 * ATR[-1]

    ## Highest/Lowest Close in last 30 periods
    elif Type==2:
        highswing = CloseStream[-2]
        Lowswing = CloseStream[-2]
        highflag = 0
        lowflag = 0
        for j in range(-3, -20, -1):
            if CloseStream[j] > highswing and highflag == 0:
                highswing = CloseStream[j]
            if CloseStream[j] < Lowswing and lowflag == 0:
                Lowswing = CloseStream[j]

        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = (highswing - CloseStream[-1])
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2
        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = (CloseStream[-1] - Lowswing)
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2

    ## Closest Swing High/Low in Last 20 periods
    elif Type==3:
        highswing = HighStream[-2]
        Lowswing = LowStream[-2]
        highflag = 0
        lowflag = 0
        for j in range(-3, -15, -1):
            if HighStream[j] > highswing and HighStream[j] > HighStream[j - 1] and HighStream[j] > HighStream[j - 2] and highflag == 0:
                highswing = HighStream[j]
                highflag = 1
            if LowStream[j] < Lowswing and LowStream[j] < LowStream[j - 1] and LowStream[j] < LowStream[j - 2] and lowflag == 0:
                Lowswing = LowStream[j]
                lowflag = 1

        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = (highswing - CloseStream[-1])
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2

        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = (CloseStream[-1] - Lowswing)
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2
    ## Closest Swing Close in Last 60 periods
    elif Type == 4:
        highswing = CloseStream[-1]
        Lowswing = CloseStream[-1]
        highflag = 0
        lowflag = 0
        for j in range(-3, -60, -1):
            if CloseStream[j] > highswing and CloseStream[j] > CloseStream[j - 1] and CloseStream[j] > CloseStream[j - 2] and \
                    CloseStream[j] > CloseStream[j + 2] and CloseStream[j] > CloseStream[j + 1] and highflag == 0:
                highswing = CloseStream[j]
                highflag = 1
            if CloseStream[j] < Lowswing and CloseStream[j] < CloseStream[j - 1] and CloseStream[j] < CloseStream[j - 2] and \
                    CloseStream[j] < CloseStream[j + 2] and CloseStream[j] < CloseStream[j + 1] and lowflag == 0:
                Lowswing = CloseStream[j]
                lowflag = 1

        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = .5*(highswing - CloseStream[-1])
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2.5

        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = .5*(CloseStream[-1] - Lowswing)
            if stoplossval < 0:
                stoplossval *= -1
            takeprofitval = stoplossval * 2.5

    elif Type==5:
        Close = np.array(CloseStream)
        High = np.array(HighStream)
        Low = np.array(LowStream)
        ATR = ta.ATR(High, Low, Close, timeperiod=14)

        highswing = HighStream[-1]
        Lowswing = LowStream[-1]
        highflag = 0
        lowflag = 0
        for j in range(-3, -60, -1):
            if HighStream[j] > highswing and HighStream[j] > HighStream[j - 1] and HighStream[j] > HighStream[j - 2] and HighStream[j] > HighStream[j + 2] and HighStream[j] > HighStream[j + 1] and highflag == 0:
                highswing = HighStream[j]
                highflag = 1
            if LowStream[j] < Lowswing and LowStream[j] < LowStream[j - 1] and LowStream[j] < LowStream[j - 2] and LowStream[j] < LowStream[j + 2] and LowStream[j] < LowStream[j + 1] and lowflag == 0:
                Lowswing = LowStream[j]
                lowflag = 1

        if prediction1 == 0 and CurrentPos == -99:
            temp = (highswing - CloseStream[-1])
            stoplossval = 1.25 * ATR[-1]
            if temp < 0:
                temp *= -1
            takeprofitval = temp * 2

        elif prediction1 == 1 and CurrentPos == -99:
            temp = (CloseStream[-1] - Lowswing)
            stoplossval = 1.25 * ATR[-1]
            if temp < 0:
                temp *= -1
            takeprofitval = temp * 2

    elif Type==6:
        Close = np.array(CloseStream)
        High = np.array(HighStream)
        Low = np.array(LowStream)
        ATR = ta.ATR(High, Low, Close, timeperiod=14)
        if prediction1 == 0 and CurrentPos == -99:
            stoplossval = 1.35 * ATR[-1]
            takeprofitval = 3 * ATR[-1]
        elif prediction1 == 1 and CurrentPos == -99:
            stoplossval = 1.35 * ATR[-1]
            takeprofitval = 3 * ATR[-1]
    return stoplossval,takeprofitval
 
