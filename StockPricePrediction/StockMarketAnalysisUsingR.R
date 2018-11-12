#forecast Tata Steel Stock Price using differnt Time Series Methods

data <- read.csv("D:\\datasets\\StockAnalysis\\ts_TataSteel_MonthlyPrice.csv", header = TRUE)
str(data)
head(data)
tail(data)
#create a vector cotaining the stock price
vec = data[[2]]
str(vec)
class(vec)
#create a time series
ts<-ts(vec, start=c(2010, 10), end=c(2018, 10), frequency=12)
#load the required libraries
library("TTR")
library("forecast")

plot(ts)

#Try Holt-winter's method

#Plot componenets of time series
#Observed= Trend+seasonal+Random

plot(decompose(ts,type='additive'))

#Plot componenets of time series-multiplicative
#Observed=Trend*Seasonal*Random

plot(decompose(ts,type='multiplicative'))

decomposed_add<-decompose(ts,type='additive')

decomposed_add$seasonal
decomposed_add$trend

#plot seasonal and trend component for Additive
plot(decomposed_add$seasonal)
plot(decomposed_add$trend)

decomposed_mul<-decompose(ts,type='multiplicative')

decomposed_mul$seasonal
decomposed_mul$trend

#plot seasonal and trend component for Multiplicative
plot(decomposed_mul$seasonal)
plot(decomposed_mul$trend)

#Holt-winter using additive seasonality
forecast_add1<-HoltWinters(ts,seasonal='additive')
summary(forecast_add1)

#show fitted values

forecast_add1$fitted

plot(forecast_add1,main="Holt winters Exponential smoothing-Additive")
forecast_add2<-forecast(forecast_add1,n=20)
forecast_add2
#write to csv
write.csv(forecast_add2, file = "D:\\datasets\\StockAnalysis\\TataMotors_Monthly_Predicted_HoltWinter_Additive.csv")
#check accuracy
mae_holt_add=mean(abs(forecast_add2$residuals),na.rm=TRUE)
mae_holt_add
#it is 38.45

#Holt-winter using multiplicative seasonality
forecast_mul1<-HoltWinters(ts,seasonal='multiplicative')
summary(forecast_mul1)

#show fitted values

forecast_mul1$fitted

plot(forecast_mul1,main="Holt winters Eponential smoothing-Multiplicative")
forecast_mul2<-forecast(forecast_mul1,n=20)
forecast_mul2
#write to csv
write.csv(forecast_mul2, file = "D:\\datasets\\StockAnalysis\\TataMotors_Monthly_Predicted_HoltWinter_Multiplicative.csv")
#check accuracy of the model
mae_holt_mul=mean(abs(forecast_mul2$residuals),na.rm=TRUE)
mae_holt_mul
#it is 36.69

#Try Auto-arima
#Check whether there is trend by putting a straight line
plot(ts)
abline(reg=lm(ts~time(ts)))

#box plot of the time series
boxplot(ts~cycle(ts), xlab='Months', ylab='Stock Price')

#Test stationarity of the time series with augmented dicky-fuller test
library(forecast)
library(tseries)
adf.test(ts, alternative = "stationary", k=12 )
#p-value = 0.7752 is not less than 0.05, so we cannot reject null hypothesis
# and the series is non-stationary

#Making series staionary by Log Transformation and Differencing
plot(ts)
plot(log(ts))
plot(diff(log(ts)))
plot(diff(diff(log(ts))))

#test stationarity
adf.test(log(ts), alternative = "stationary", k=12 )
#p-value = 0.7106, it is greater than 0.05 and hence H0 cannot be rejected

adf.test(diff(log(ts)), alternative = "stationary", k=12 )
#p-value = 0.7106, it is greater than 0.05 and hence H0 cannot be rejected

adf.test(diff(log(ts)), alternative = "stationary", k=12 )
#p-value = 0.08162, it is greater than 0.05 but close to 0.05

adf.test(diff(diff(log(ts))), alternative = "stationary", k=12 )
#p-value = 0.2115, it is greater than 0.05 and hence H0 cannot be rejected

#Fit Arima model
model_auto_arima = auto.arima(ts)
model_auto_arima

resd = model_auto_arima$residuals

#plot residuals, ACF and PACF
plot(resd)
acf(resd)
pacf(resd)

#Test stationarity of the residuals
adf.test(resd, alternative = "stationary")
#p value = 0.01 is smaller than 0.05

#test whether residuals are normally distributed
qqnorm(resd)
qqline(resd)
#it is a good model as the errors are following almost a normal distribution

#now forecast it
forecast_autoArima = forecast(model_auto_arima, h = 28)
forecast_autoArima

plot(forecast_autoArima)
#write to csv
write.csv(forecast_autoArima, file = "D:\\datasets\\StockAnalysis\\TataMotors_Monthly_Predicted_AutoArima.csv")
#check accuracy of the model

#MAE
mae_auto_arima = mean(abs(forecast_autoArima$residuals), na.rm=TRUE)
mae_auto_arima
#it is 25.72
