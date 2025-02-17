### CRE_ABM Emulation ###
## Reset environment ## 
rm(list = ls())

## put the path of "emulation_calibration" folder in setwd()
setwd('/Users/solkim/Downloads/emulation_calibration')
## Set seed number to regenerate the result again
set.seed(1234)

## Load ABM simulator data and observation for data A and B
load("simulation_data.RData")
obs.a<-read.csv('dataA_per_months.csv');obs.b<-read.csv('dataB_per_months.csv')
obs.a<-obs.a$PHAI_counts;obs.b<-obs.b$PHAI_counts
obs.a<-obs.a[3:length(obs.a)];obs.b<-obs.b[1:30]

## Visualize simulator output
par(mfrow=c(1,2))
plot(x=theta$x, y=exp(response.a$response), type="o", main = "simulator output (A)",
     lwd=2, xlab="input parameter", ylab="mean output")
plot(x=theta$x, y=exp(response.b$response), type="o", main = "simulator output (B)",
     lwd=2, xlab="input parameter", ylab="mean output")


## packages
library(DiceKriging);library(splines)

## Fit an emulator 
fit.emul.a<-km(~x+I(x^2)+I(x^3), design=theta, response=response.a)
fit.emul.b<-km(~x+I(x^2)+I(x^3), design=theta, response=response.b)

## Visualize; Does it interpolate between the points well?
new.grid<-data.frame(x=seq(theta[1,1], theta[dim(theta)[1],1], length.out=200))
pred.emul.a<-predict.km(fit.emul.a, newdata = new.grid, "UK")
pred.emul.b<-predict.km(fit.emul.b, newdata = new.grid, "UK")

par(mfrow=c(1,2))
plot(x=new.grid[,1],y=simulate(fit.emul.a, newdata=new.grid), type="l",
     col="grey",lty=3, xlab="beta",ylab="emul",main="Emulation output(A)")
for(i in 1:50){
  lines(x=new.grid[,1],y=simulate(fit.emul.a, newdata=new.grid),
        col="grey",lty=3)
}
lines(x=seq(theta[1,1], theta[dim(theta)[1],1], length.out=200), y=pred.emul.a$mean,lwd=3)
points(x=theta[,1], y=response.a[,1])
legend("topleft", legend = c("mean function", "samples"), col=c("black","grey"), lty=c(1, 3), lwd=c(3,1))


plot(x=new.grid[,1],y=simulate(fit.emul.b, newdata=new.grid), type="l",
     col="grey",lty=3, xlab="beta",ylab="emul",main="Emulation output(B)")
for(i in 1:50){
  lines(x=new.grid[,1],y=simulate(fit.emul.b, newdata=new.grid),
        col="grey",lty=3)
}
lines(x=seq(theta[1,1], theta[dim(theta)[1],1], length.out=200), y=pred.emul.b$mean,lwd=3)
points(x=theta[,1], y=response.b[,1])

legend("topleft", legend = c("mean function", "samples"), col=c("black","grey"), lty=c(1, 3), lwd=c(3,1))

#################
## Calibration ##
#################
## Let emulator output eta = log-intensity of Poisson distribution
## Then we can model the observation Z_i ~ Pois(exp(eta))
## Model;
## Z|eta ~ Poisson (eta)
## beta ~ Unif(0.05, 0.16)

## MCMC
## constants
n.iter<-50000; init.beta<-0.1; step_size<-0.01; 
init.eta<-exp(simulate(fit.emul.a,newdata=data.frame(x=init.beta)))
beta.sample<-numeric(n.iter); eta.sample<-numeric(n.iter)
beta.sample[1]<-init.beta; eta.sample[1]<-init.eta; acc_rate<-0


## Run MCMC
for(i in 2:n.iter){
  prop <- rnorm(1,beta.sample[i-1],sd=step_size)
  if(prop<min(theta) | prop>max(theta)){
    beta.sample[i]<-beta.sample[i-1]
    eta.sample[i]<-eta.sample[i-1]
  }
  else{
    eta_pr<-exp(simulate(fit.emul.a,newdata=data.frame(x=prop)))
    ll_pr<-sum(dpois(obs.a, eta_pr, log=T))
    ll_cu<-sum(dpois(obs.a, (eta.sample[i-1]), log=T))
    acc<-ll_pr-ll_cu
    if(log(runif(1))<acc){ #accept
      beta.sample[i]<-prop
      eta.sample[i]<-eta_pr
      acc_rate<-acc_rate+1
    }
    else{
      beta.sample[i]<-beta.sample[i-1]
      eta.sample[i]<-eta.sample[i-1]
    }
  }
}


acc_rate<-acc_rate/n.iter ## Ideal acceptance rate is in range 0.2 ~ 0.5
acc_rate

## Sample visualization without burn-in
par(mfrow=c(2,2))
ts.plot(eta.sample, main="Emulator samples_A") 
ts.plot(beta.sample, main="Parameter (beta) samples_A")

## For data B
## MCMC
## constants
n.iter<-50000; init.beta<-0.1; step_size<-0.005; 
init.eta<-exp(simulate(fit.emul.b,newdata=data.frame(x=init.beta)))
beta.sample2<-numeric(n.iter); eta.sample2<-numeric(n.iter)
beta.sample2[1]<-init.beta; eta.sample2[1]<-init.eta; acc_rate2<-0
obs.b<-read.csv('/Users/whiskeyindia/Downloads/Personal_reasearch/ABM_with_Sol_Kim/emulation_calibration/dataB_per_months.csv')
obs.b<-obs.b$PHAI_counts[1:30]

for(i in 2:n.iter){
  prop <- rnorm(1,beta.sample2[i-1],sd=step_size)
  if(prop<min(theta) | prop>max(theta)){
    beta.sample2[i]<-beta.sample2[i-1]
    eta.sample2[i]<-eta.sample2[i-1]
  }
  else{
    eta_pr<-exp(simulate(fit.emul.b,newdata=data.frame(x=prop)))
    ll_pr<-sum(dpois(obs.b, eta_pr, log=T))
    ll_cu<-sum(dpois(obs.b, (eta.sample2[i-1]), log=T))
    acc<-ll_pr-ll_cu
    if(log(runif(1)) < acc){ #accept
      beta.sample2[i]<-prop
      eta.sample2[i]<-eta_pr
      acc_rate2<-acc_rate2+1
    }
    else{
      beta.sample2[i]<-beta.sample2[i-1]
      eta.sample2[i]<-eta.sample2[i-1]
    }
  }
}

acc_rate2<-acc_rate2/n.iter
acc_rate2
ts.plot(eta.sample2, main="Emulator samples_B")
ts.plot(beta.sample2, main="Parameter (beta) samples_B")

## Post-processing
n.burnin<-1000;
beta.sample<-beta.sample[n.burnin:length(beta.sample)]
beta.sample2<-beta.sample2[n.burnin:length(beta.sample2)]

# After diagnosis
par(mfrow=c(2,1))

# Visualize: Trace, acf
ts.plot(beta.sample, main="Parameter (beta) samples_A")
ts.plot(beta.sample2, main="Parameter (beta) samples_B")
acf(beta.sample);acf(beta.sample2)

### Compare both results
par(mfrow=c(1,1))
boxplot(beta.sample, beta.sample2, ylab="beta", xlab="Calibration scenario",
        names=c("data_A","data_B"), main="Posterior sample boxplot")
mean(beta.sample);mean(beta.sample2)
quantile(beta.sample); quantile(beta.sample2)

write.csv(beta.sample, file="calibration_results_A.csv")
write.csv(beta.sample2, file="calibration_results_B.csv")
save(beta.sample, beta.sample2, eta.sample, eta.sample2, acc_rate, acc_rate2, 
     file = "calibration_results.RData")


