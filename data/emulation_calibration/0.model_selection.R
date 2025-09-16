### CRE_ABM Emulation ###
## Reset environment ## 
rm(list = ls())

## put the path of "emulation_calibration" folder in setwd()
setwd('/Users/solkim/Downloads/emulation_calibration')


## Set seed number to regenerate the result again
set.seed(1234)

## Load ABM simulator data and observation for data A and B
load("simulation_data.RData")


## packages
library(DiceKriging);library(splines)

## Fit an emulator and Model comparison for datatype A
## Compute from linear trend to 6th order polynomial trend model
M1<-km(~x , design=theta, response=response.a)
M2<-km(~x+I(x^2), design=theta, response=response.a)
M3<-km(~x+I(x^2)+I(x^3), design=theta, response=response.a)
M4<-km(~x+I(x^2)+I(x^3)+I(x^4), design=theta, response=response.a)
M5<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5), design=theta, response=response.a)
M6<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5)+I(x^6), design=theta, response=response.a)
M7<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5)+I(x^6)+I(x^7), design=theta, response=response.a)

## Comparing AIC and BIC
## num_params=covariance parameter (1) + variance (1) + number of coef (order + 1)
num_params1 <- M1@covariance@param.n + 1 + 2
num_params2 <- M2@covariance@param.n + 1 + 3
num_params3 <- M3@covariance@param.n + 1 + 4
num_params4 <- M4@covariance@param.n + 1 + 5
num_params5 <- M5@covariance@param.n + 1 + 6
num_params6 <- M6@covariance@param.n + 1 + 7
num_params7 <- M7@covariance@param.n + 1 + 8

## Compute AIC: 2*the number of parameters - 2*maximum log likelihood
aic.1<-2*num_params1 -2*M1@logLik
aic.2<-2*num_params2 -2*M2@logLik
aic.3<-2*num_params3 -2*M3@logLik
aic.4<-2*num_params4 -2*M4@logLik
aic.5<-2*num_params5 -2*M5@logLik
aic.6<-2*num_params6 -2*M6@logLik
aic.7<-2*num_params7 -2*M7@logLik

## Compute BIC: the number of parameters * log(the number of obs) - 2 * maximum log liklihood
bic.1<-num_params1*log(M1@n) -2*M1@logLik
bic.2<-num_params2*log(M2@n) -2*M2@logLik
bic.3<-num_params3*log(M3@n) -2*M3@logLik
bic.4<-num_params4*log(M4@n) -2*M4@logLik
bic.5<-num_params5*log(M5@n) -2*M5@logLik
bic.6<-num_params6*log(M6@n) -2*M6@logLik
bic.7<-num_params7*log(M6@n) -2*M7@logLik

## Now, Fit an emulator and Model comparison for datatype B
## Compute from linear trend to 6th order polynomial trend model
M11<-km(~x , design=theta, response=response.b)
M21<-km(~x+I(x^2), design=theta, response=response.b)
M31<-km(~x+I(x^2)+I(x^3), design=theta, response=response.b)
M41<-km(~x+I(x^2)+I(x^3)+I(x^4), design=theta, response=response.b)
M51<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5), design=theta, response=response.b)
M61<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5)+I(x^6), design=theta, response=response.b)
M71<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5)+I(x^6)+I(x^7), design=theta, response=response.b)
M81<-km(~x+I(x^2)+I(x^3)+I(x^4)+I(x^5)+I(x^6)+I(x^7)+I(x^8), design=theta, response=response.b)

## Comparing AIC and BIC
## num_params=covariance parameter (1) + variance (1) + number of coef (order + 1)
num_params1 <- M11@covariance@param.n + 1 + 2
num_params2 <- M21@covariance@param.n + 1 + 3
num_params3 <- M31@covariance@param.n + 1 + 4
num_params4 <- M41@covariance@param.n + 1 + 5
num_params5 <- M51@covariance@param.n + 1 + 6
num_params6 <- M61@covariance@param.n + 1 + 7
num_params7 <- M71@covariance@param.n + 1 + 8
num_params8 <- M81@covariance@param.n + 1 + 9

## Compute AIC: 2*the number of parameters - 2*maximum log likelihood
aic.11<-2*num_params1 -2*M11@logLik
aic.21<-2*num_params2 -2*M21@logLik
aic.31<-2*num_params3 -2*M31@logLik
aic.41<-2*num_params4 -2*M41@logLik
aic.51<-2*num_params5 -2*M51@logLik
aic.61<-2*num_params6 -2*M61@logLik
aic.71<-2*num_params7 -2*M71@logLik
aic.81<-2*num_params8 -2*M81@logLik

## Compute BIC: the number of parameters * log(the number of obs) - 2 * maximum log liklihood
bic.11<-num_params1*log(M11@n) -2*M11@logLik
bic.21<-num_params2*log(M21@n) -2*M21@logLik
bic.31<-num_params3*log(M31@n) -2*M31@logLik
bic.41<-num_params4*log(M41@n) -2*M41@logLik
bic.51<-num_params5*log(M51@n) -2*M51@logLik
bic.61<-num_params6*log(M61@n) -2*M61@logLik
bic.71<-num_params7*log(M71@n) -2*M71@logLik
bic.81<-num_params8*log(M81@n) -2*M81@logLik


## AIC and BIC visualize
par(mfrow=c(1,2))
aic<-c(aic.1,aic.2,aic.3,aic.4,aic.5,aic.6, aic.7)
bic<-c(bic.1,bic.2,bic.3,bic.4,bic.5,bic.6, bic.7)
xtick<-c("linear","2nd polynoimal","3rd polynoimal","4th polynoimal",
         "5th polynoimal", "6th polynoimal", "7th polynoimal")
plot(aic, type="o",col="black",lwd=2,main="AIC and BIC visualize (A)",ylab="AIC and BIC",
     xaxt="n",xlab="models",ylim=c(-10,20))
lines(bic, type="o", col="red",lwd=2)
axis(1, at = 1:length(aic), labels = xtick)
legend("topright", legend = c("AIC", "BIC"),col = c("black", "red"), lty=1, lwd = 2)

aic1<-c(aic.11,aic.21,aic.31,aic.41,aic.51,aic.61,aic.71,aic.81)
bic1<-c(bic.11,bic.21,bic.31,bic.41,bic.51,bic.61,bic.71,bic.81)
xtick<-c("linear","2nd polynoimal","3rd polynoimal","4th polynoimal",
         "5th polynoimal", "6th polynoimal", "7th polynoimal", "8th polynomial")
plot(aic1, type="o",col="black",lwd=2,main="AIC and BIC visualize (B)",ylab="AIC and BIC",
     xaxt="n",xlab="models", ylim = c(-100, 10))
lines(bic1, type="o", col="red",lwd=2)
axis(1, at = 1:length(aic1), labels = xtick)
legend("topright", legend = c("AIC", "BIC"),col = c("black", "red"), lty=1, lwd = 2)


#### Result: We'll choose natural qubic spline basis with df = 3 for A and 7 for B.
