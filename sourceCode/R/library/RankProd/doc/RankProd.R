### R code from vignette source 'RankProd.Rnw'

###################################################
### code chunk number 1: RankProd.Rnw:79-80
###################################################
library(RankProd)


###################################################
### code chunk number 2: RankProd.Rnw:84-85
###################################################
data(arab)


###################################################
### code chunk number 3: RankProd.Rnw:101-104
###################################################
n <- 5
cl <- rep(1,5)
cl


###################################################
### code chunk number 4: RankProd.Rnw:110-114
###################################################
n1 <- 5
n2 <- 4
cl <- rep(c(0,1),c(n1,n2))
cl


###################################################
### code chunk number 5: RankProd.Rnw:123-129
###################################################
n1 <- 5
n2 <- 4
cl <- rep(c(0,1),c(n1,n2))
cl
origin <- rep(1, n1+n2)
origin


###################################################
### code chunk number 6: RankProd.Rnw:133-138
###################################################
n <- 9
cl <- rep(1,n)
cl
origin <- rep(1, n)
origin


###################################################
### code chunk number 7: RankProd.Rnw:147-149
###################################################
origin <- c(rep(1, 6), rep(2,4), rep(3,8))
origin


###################################################
### code chunk number 8: RankProd.Rnw:157-160
###################################################
colnames(arab)
arab.cl
arab.origin


###################################################
### code chunk number 9: RankProd.Rnw:170-173
###################################################
arab.sub <- arab[,which(arab.origin==1)]
arab.cl.sub <- arab.cl[which(arab.origin==1)]
arab.origin.sub <- arab.origin[which(arab.origin==1)]


###################################################
### code chunk number 10: RankProd.Rnw:176-178
###################################################
RP.out <- RP(arab.sub,arab.cl.sub, num.perm=100, logged=TRUE,
na.rm=FALSE,plot=FALSE,  rand=123)


###################################################
### code chunk number 11: RankProd.Rnw:208-209
###################################################
plotRP(RP.out, cutoff=0.05)


###################################################
### code chunk number 12: RankProd.Rnw:224-225
###################################################
topGene(RP.out,cutoff=0.05,method="pfp",logged=TRUE,logbase=2,gene.names=arab.gnames)


###################################################
### code chunk number 13: RankProd.Rnw:253-256
###################################################
##identify differentially expressed  genes
RP.adv.out <-  RPadvance(arab,arab.cl,arab.origin,num.perm=100,
logged=TRUE,gene.names=arab.gnames,rand=123)


###################################################
### code chunk number 14: RankProd.Rnw:260-261
###################################################
plotRP(RP.adv.out, cutoff=0.05)


###################################################
### code chunk number 15: RankProd.Rnw:284-285
###################################################
data(lymphoma)


###################################################
### code chunk number 16: RankProd.Rnw:316-323
###################################################
refrs <- (1:8)*2-1
samps <- (1:8)*2
M <- lym.exp[,samps]-lym.exp[,refrs]
colnames(M)
cl <- c(rep(0,4),rep(1,4))
cl  #"CLL" is class 1, and "DLCL" is class 2
RP.out <- RP(M,cl, logged=TRUE, rand=123)


###################################################
### code chunk number 17: RankProd.Rnw:325-326
###################################################
topGene(RP.out,cutoff=0.05,logged=TRUE,logbase=exp(1))


###################################################
### code chunk number 18: RankProd.Rnw:369-373
###################################################
arab.cl2 <- arab.cl
arab.cl2[arab.cl==0 &arab.origin==2] <- 1
arab.cl2[arab.cl==1 &arab.origin==2] <- 0
arab.cl2


###################################################
### code chunk number 19: RankProd.Rnw:376-379
###################################################
Rsum.adv.out <- RSadvance(arab,arab.cl2,arab.origin,num.perm=100,
logged=TRUE,gene.names=arab.gnames,rand=123)
topGene(Rsum.adv.out,cutoff=0.05,gene.names=arab.gnames)


###################################################
### code chunk number 20: RankProd.Rnw:383-384
###################################################
topGene(Rsum.adv.out,num.gene=10,gene.names=arab.gnames)


###################################################
### code chunk number 21: RankProd.Rnw:387-388
###################################################
plotRP(Rsum.adv.out,cutoff=0.05)


###################################################
### code chunk number 22: RankProd.Rnw:394-396
###################################################
RP.adv.out <- RPadvance(arab,arab.cl2,arab.origin,num.perm=100,
logged=TRUE,gene.names=arab.gnames,rand=123)


###################################################
### code chunk number 23: RankProd.Rnw:399-400
###################################################
topGene(RP.adv.out,cutoff=0.05,gene.names=arab.gnames)


