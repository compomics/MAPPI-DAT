### R code from vignette source 'SSPA.Rnw'

###################################################
### code chunk number 1: SSPA.Rnw:46-47
###################################################
options(width=60)


###################################################
### code chunk number 2: simulated-data-generation
###################################################
library(SSPA)
library(genefilter)
set.seed(12345)
m <- 5000
J <- 10
pi0 <- 0.8
m0 <- as.integer(m*pi0)
mu <- rbitri(m - m0, a = log2(1.2), b = log2(4), m = log2(2))
data <- simdat(mu, m=m, pi0=pi0, J=J, noise=0.01)
statistics <- rowttests(data, factor(rep(c(0, 1), each=J)))$statistic


###################################################
### code chunk number 3: simulated-data-plotting
###################################################
pdD <- pilotData(statistics = statistics, 
                 samplesize = sqrt(1/(1/J +1/J)), 
                 distribution="norm")
pdD
plot(pdD)


###################################################
### code chunk number 4: simulated-data-deconvolution
###################################################
ssD <- sampleSize(pdD, control=list(from=-6, to=6))
ssD
plot(ssD, panel = function(x, y, ...)
     { 
       panel.xyplot(x, y)
       panel.curve(dbitri(x), lwd=2, lty=2, n=500)
     },
     ylim=c(0, 0.6))


###################################################
### code chunk number 5: simulated-data-power
###################################################
Jpred <- seq(10, 20, by=2)
N <- sqrt(Jpred/2)
pwrD <- predictpower(ssD, samplesizes=N, alpha=0.05)
matplot(Jpred, pwrD, type="b", pch=16, ylim=c(0, 1),
        ylab="predicted power", xlab="sample size (per group)")
grid()


###################################################
### code chunk number 6: simulated-data-effectsize
###################################################
pdC <- pilotData(statistics = statistics, 
                 samplesize = sqrt(2*J), 
                 distribution="t",
                 df=2*J-2)
ssC <- sampleSize(pdC, 
                  method="congrad", 
                  control=list(from=-6, to=6, resolution=250))
plot(ssC, panel = function(x, y, ...)
     { 
       panel.xyplot(x, y)
       panel.curve(2*dbitri(2*x), lwd=2, lty=2, n=500)
     },
     xlim=c(-2,2), ylim=c(0, 1.2))


###################################################
### code chunk number 7: tikohonov
###################################################
ssT <- sampleSize(pdC, 
                  method="tikhonov", 
                  control=list(resolution=250, 
                    scale="pdfstat", 
                    lambda = 10^seq(-10, 10, length=50), 
                    verbose=FALSE, 
                    modelselection="lcurve"))
plot(ssT, panel = function(x, y, ...)
     { 
       panel.xyplot(x, y, type="b")
       panel.curve(2*dbitri(2*x), lwd=2, lty=2, n=500)
     }, 
     xlim=c(-2,2), ylim=c(0, 1.2))


###################################################
### code chunk number 8: nutrigenomics-effectsize
###################################################
library(lattice)
data(Nutrigenomics)
str(Nutrigenomics)
pd <- apply(Nutrigenomics, 2, 
            function(x) pilotData(statistics=x[-1], 
                                  samplesize=sqrt(x[1]), 
                                  distribution="norm"))
ss <- lapply(pd, sampleSize,  
             control=list(pi0Method="Storey", a=0, resolution=2^10, verbose=FALSE))

##ss <- lapply(pd, sampleSize,  
##             method = "congrad", 
##             control=list(verbose=FALSE, resolution=2^10, from=-10, to=10))

compounds <- c("Wy14,643",  "fenofibrate", "trilinolenin (C18:3)", "Wy14,643", "fenofibrate")
exposure <- c("5 Days", "6 Hours")

effectsize <- data.frame(exposure = factor(rep(rep(exposure, c(2, 3)), each=1024)), 
                         compound = factor(rep(compounds, each=1024)), 
                         lambda = as.vector(sapply(ss, 
                           function(x)x@lambda)), 
                         theta = as.vector(sapply(ss, 
                           function(x)x@theta)))

print(xyplot(lambda~theta|exposure, group=compound, data=effectsize, 
             type=c("g", "l"), layout=c(1,2), lwd=2, xlab="effect size", ylab="", 
             auto.key=list(columns=3, lines=TRUE, points=FALSE, cex=0.7)))


###################################################
### code chunk number 9: nutrigenomics-power
###################################################
samplesize <- seq(2, 8)
averagepower <- data.frame(power = as.vector(sapply(ss, 
                             function(x) as.numeric(predictpower(x, samplesize=sqrt(samplesize))))), 
                           exposure = factor(rep(rep(exposure, c(2, 3)), each=length(samplesize))), 
                           compound = factor(rep(compounds, each=length(samplesize))),
                           samplesize = rep(2*samplesize, 5))

print(xyplot(power~samplesize|exposure, group=compound, data=averagepower, type=c("g", "b"), 
             layout=c(1,2), lwd=2, pch=16, xlab="sample size (per group)", ylab="", 
             auto.key=list(columns=3, lines=TRUE, points=FALSE, cex=0.7)))


###################################################
### code chunk number 10: obtain-teststatistics (eval = FALSE)
###################################################
## ##files contains the full path and file names of each sample
## targets <- data.frame(files=files,
##                       group=rep(c("DCLK", "WT"), 4), 
##                       description=rep(c("transgenic (Dclk1) mouse hippocampus", 
##                         "wild-type mouse hippocampus"), 4))
## d <- readDGE(targets) ##reading the data
## ##filter out low read counts
## cpm.d <- cpm(d)
## d <- d[rowSums(cpm.d > 1) >= 4, ]
## 
## design <- model.matrix(~group, data=d$samples) 
## ##estimate dispersion
## disp <- estimateGLMCommonDisp(d, design)
## disp <- estimateGLMTagwiseDisp(disp, design)
## ##fit model
## glmfit.hoen <- glmFit(d, design, dispersion = disp$tagwise.dispersion)
## ##perform likelihood ratio test
## lrt.hoen <- glmLRT(glmfit.hoen)
## ##extract results
## tbl <- topTags(lrt.hoen, n=nrow(d))[[1]]
## statistics <- tbl$LR


###################################################
### code chunk number 11: deepsage-effectsize (eval = FALSE)
###################################################
## library(lattice)
## data(deepSAGE)
## str(deepSAGE)


###################################################
### code chunk number 12: sessioninfo
###################################################
toLatex(sessionInfo())


