
args=(commandArgs(TRUE))
if(length(args)==0){
  print("No arguments supplied.")
  ##supply default values
  Inputfile = ""
  OutputFile=""
  nsrep=0
  srep=0
  }else{
  for(i in 1:length(args)){
    eval(parse(text=args[[i]]))
  }
}

normalization <-function(fileControl,outputfileName,nsrep,srep){

  library(stats)
  library(car)
  data.without.controls=read.table(paste(fileControl,"/AllPlatesWithoutControl.txt",sep=""),header=TRUE,sep="\t")
  data.copy=data.without.controls
  data.without.controls$IntegralIntensity_um2=log2(data.without.controls$IntegralIntensity_um2)
  aov.out <- aov(IntegralIntensity_um2 ~ SourceWell * SourcePlate, data.without.controls) # build a model without using the control samples
#  print(summary(aov.out))
  data.without.controls$residuals <- aov.out$residuals
  data.without.controls$IntegralIntensity_um2=data.copy$IntegralIntensity_um2
  write.table(data.without.controls,file=outputfileName,sep="\t",row.names=F)
## now make a plot for controls+
  AllPlatesWithControl <- read.table(paste(fileControl,"/AllPlatesOnlyControl.txt",sep=""),header=TRUE,sep="\t")
  controls <- subset(AllPlatesWithControl, AllPlatesWithControl$type == "control+")
  controls$IntegralIntensity_um2=log2(controls$IntegralIntensity_um2)
  pdf(file=paste(fileControl,'/BoxPlotControlsAllPlates.pdf',sep=""))
  par(oma=c(1,1,1,1))
  Boxplot(IntegralIntensity_um2~SourcePlate,controls,id.method="none",las=2,col=c(2:8),outline=F,xlab='',ylab='')
  mtext('Source Plates', side = 1, line = 4, cex = 1, font = 1)
  mtext('log2(Integral intensity)', side = 2, line = 4, cex = 1, font = 1)
  mtext('BoxPlot for controls+', side = 3, line = 2, cex = 1, font = 2)
  dev.off()
## now make a plot for SD+ FC
  AllPlatesWithsd <- read.table(paste(fileControl,"/AllPlatesOnlyControl_IntegralIntensity.txt",sep=""),header=TRUE,sep="\t")
  sd <- subset(AllPlatesWithsd, AllPlatesWithsd$Type == "control+")
  end=6+nsrep+srep
  data=as.matrix(sd[7:end]) ## logged
  cl <- rep(c(0,1),c(nsrep,srep))
  x=which(cl==0) ##control
  y=which(cl==1) ## test
  data1 <- as.matrix(data[,x]) ##data under condition1 i.e NS
  data2 <- as.matrix(data[,y])  ##data under condition2 i.e S
  data1.ave=apply(data1,1,mean) # NS average
  data2.ave=apply(data2,1,mean)
  fold.change=data2.ave/data1.ave
  sd$FC=fold.change
  pdf(file=paste(fileControl,'/BoxPlotSD+AllPlates.pdf',sep=""))
  par(oma=c(1,1,1,1))
  Boxplot(FC~SourcePlate,sd,id.method="none",las=2,col=c(2:8),outline=F,xlab='',ylab='')
  mtext('Source Plates', side = 1, line = 4, cex = 1, font = 1)
  mtext('FC', side = 2, line = 3, cex = 1, font = 1)
  mtext('BoxPlot for SD+', side = 3, line = 2, cex = 1, font = 2)
  dev.off()

}


#fileControl="C:/Users/surya/Desktop/ProjectData/MAPPI-DATdata/18Jan16/MAPPIDAT_OutPut/"

normalization(Inputfile,OutputFile,nsrep,srep)