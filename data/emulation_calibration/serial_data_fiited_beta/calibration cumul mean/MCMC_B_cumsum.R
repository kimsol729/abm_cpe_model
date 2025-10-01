rm(list=ls())
set.seed(1234)
#setwd('/Users/whiskeyindia/Library/Mobile Documents/com~apple~CloudDocs/ABM')
load('dataB2.RData');
dat<-t(mdata)
cumsum_dat <- apply(dat, 2, cumsum)
#require(devtools)
#install_url('https://cran.r-project.org/src/contrib/Archive/geofd/geofd_2.0.tar.gz')
library(geofd);library(mvtnorm)

# Constants
n<-dim(dat)[1];argvals<-seq(1,n,by=1);
obs<-matrix(obs, nrow=1);nbasis<-25
cumsum_obs <- matrix(cumsum(obs), nrow=1)
N.iter<-20000;

step.b<-0.005;
step.s<-0.15;

theta<-as.numeric(colnames(dat))
coords<-cbind(theta, rep(0, dim(dat)[2]));acc.B<-acc.S<-0
cov.model<-"matern"
E.samp<-matrix(NA,nrow=n, ncol=N.iter);E.samp[,1]<-runif(n,0,10)
B.samp<-matrix(NA,nrow=1, ncol=N.iter);B.samp[,1]<-0.08
S.samp<-matrix(NA,nrow=1, ncol=N.iter);S.samp[,1]<-1

# MCMC
for(i in 2:N.iter){
  #B
  prop<-cbind(rnorm(1,B.samp[,i-1],sd=step.b),0)
  if(prop[1]<min(theta) | prop[1]>max(theta)){
    B.samp[,i]<-B.samp[,i-1]
    E.samp[,i]<-E.samp[,i-1]
  }
  else{
    E<-t(okfd(new.coords=prop, coords=coords, data=cumsum_dat, smooth.type="bsplines",
              nbasis=nbasis, argvals=argvals, cov.model=cov.model)$krig.new.data)
    ll_pr<-dmvnorm(E, cumsum_obs, sigma=S.samp[,i-1]*diag(n), log=T)
    ll_cu<-dmvnorm(E.samp[,i-1], cumsum_obs, sigma=S.samp[,i-1]*diag(n), log=T)
    acc<-ll_pr-ll_cu
    if(log(runif(1))<acc){ #accept
      B.samp[,i]<-prop[1]
      E.samp[,i]<-E
      acc.B<-acc.B+1
    }
    else{
      B.samp[,i]<-B.samp[,i-1]
      E.samp[,i]<-E.samp[,i-1]
    }
  }
  
  #S
  prop<-rnorm(1,S.samp[,i-1],sd=step.s)
  if(prop<=0 | prop>1){
    S.samp[,i]<-S.samp[,i-1]
  }
  else{
    ll_pr<-dmvnorm(E.samp[,i], cumsum_obs, sigma=prop*diag(n), log=T)
    ll_cu<-dmvnorm(E.samp[,i], cumsum_obs, sigma=S.samp[,i-1]*diag(n), log=T)
    acc<-ll_pr-ll_cu
    if(log(runif(1))<acc){ #accept
      S.samp[,i]<-prop
      acc.S<-acc.S+1
    }
    else{
      S.samp[,i]<-S.samp[,i-1]
    }
  }
}

paste("Acc.Rate-beta: ", acc.B/N.iter, "Acc.Rate-sigma: ", acc.S/N.iter)
ts.plot(as.numeric(B.samp)[2000:N.iter], main="Beta posterior samples", ylab='beta')
ts.plot(as.numeric(S.samp)[2000:N.iter])
save(B.samp, E.samp, S.samp, acc.B, acc.S, file="MCMCchain_s01.RData")

acf(as.numeric(B.samp), main="ACF Plot of Beta Samples")
acf(as.numeric(S.samp), main="ACF Plot of Sigma Samples")


if(T){
  par(mfrow=c(1,1))
  new.coords<-cbind(mean(as.numeric(B.samp)),0)
  coords<-cbind(as.numeric(colnames(cumsum_dat)), rep(0, dim(cumsum_dat)[2]))
  okfd.res<-okfd(new.coords=new.coords, coords=coords, data=cumsum_dat, smooth.type="bsplines",
                 nbasis=nbasis, argvals=argvals, cov.model=cov.model)
  
  matplot(cumsum_dat, type="l", lty=2, xlab="Month", ylab="Infected",
          main="Simulation result (A)", ylim=c(0, 60))
  
  matplot(okfd.res$krig.new.data,type="l", add=T, col="grey", lty=2)
  lines(okfd.res$krig.new.data, col=2, lwd=2)
  lines(t(cumsum_obs), lwd=2, col="lightgreen")
}
# 원본 시뮬레이션 곡선 모두 점선으로 그림
matplot(cumsum_dat, type="l", lty=2, col="grey",
        xlab="Month", ylab="Infected",
        main="Simulation result (A)", ylim=range(c(cumsum_dat, cumsum_obs)))

# 모든 B.samp 값에 대한 예측곡선 계산
krig.mat <- do.call(cbind, lapply(as.numeric(B.samp), function(b) {
  okfd(cbind(b,0), coords, cumsum_dat,
       smooth.type="bsplines", nbasis=nbasis,
       argvals=argvals, cov.model=cov.model)$krig.new.data
}))

# 최소/최대/평균 계산
curve.min <- apply(krig.mat, 1, min)
curve.max <- apply(krig.mat, 1, max)
curve.mean <- rowMeans(krig.mat)

# 최소~최대 영역 색칠
polygon(c(argvals, rev(argvals)), c(curve.min, rev(curve.max)),
        col=rgb(0.8,0.8,0.8,0.5), border=NA)

# 평균 시뮬레이션
lines(curve.mean, col=2, lwd=2)

# 관측치
lines(t(cumsum_obs), col="lightgreen", lwd=2)


## Cumulative summation
load("MCMCchain1.RData")

# 열 이름, 행 이름 제거하고 데이터만 저장
write.table(as.vector(B.samp),
            "Beta_samp_B.csv",
            sep = ",",
            row.names = FALSE,
            col.names = FALSE)
