setwd("~/Documents/bigData")
getwd()
library("dplyr")
library("data.table")
library("ggplot2")
library("ggridges")
library("gridExtra")
library("lattice")


#------------------------------------------------------------------------------------
#this part will prepare the data before any actions are made
stats=fread("Seasons_Stats.csv")
players1=fread("Players.csv")
players2=fread("player_data.csv")
players1=subset(players1,select = c(Player,height,weight))
stats= merge(stats,players1, by="Player")
stats$blanl=NULL;
stats$blank2=NULL;
mulTeam=(filter(stats,Tm=='TOT')) #playerTwoOrMoreTm

for(i in 1:nrow(mulTeam) ){
  stats= stats[!(stats$Player==mulTeam$Player[i] & stats$Year==mulTeam$Year[i] & stats$Tm!="TOT") ,]
}

statsM=stats;#maybe will change just to stats
statsM=statsM[complete.cases(statsM),]

#divide data to three main positions of the game (maybe add proper 5 positions)
  Guards=statsM[grep("G",statsM$Pos)];
  Forwards=statsM[grep("F",statsM$Pos)];
  Centers=statsM[grep("C",statsM$Pos)];

#-----------------------------------------------------------------------------------------------
  
  #avg height of positions just for observation
  height.table= data.table(pos="G",height=Guards$height)
  temp1=(data.table(pos= "F",height=Forwards$height))
  height.table=rbind(height.table,temp1)
  temp1=(data.table(pos= "C",height=Centers$height))
  height.table=rbind(height.table,temp1)
  
  # pdf("height comparison.pdf")
  # comarePlot =ggplot(height.table, aes(x = height, y = pos)) +
  #   geom_density_ridges(aes(fill = pos)) +
  #   scale_fill_manual(values = c("#00AFBB", "#E7B800", "#FC4E07"))
  # print(comarePlot)
  # dev.off()
  
  
  
#corraltions of the postions with the height  
  
pos.cor = function(Position){
  Position$Player=NULL
  Position$Tm=NULL
  Position$Pos=NULL
  coralation= cor(Position,Position$height)
  corTable=data.table(coralation)
  corTable = cbind(varaibles=colnames(Position),coralation=corTable)
  corTable = arrange(corTable, desc(corTable$coralation))
  return (corTable)
}
  
  GuardsCorr=pos.cor(Guards)
  ForwardsCorr=pos.cor(Forwards)
  CentersCorr=pos.cor(Centers)
  OverallCorr=pos.cor(statsM)
  
#-----------------------------------------------------------------------------------
  # varaibles that we took out of the main corralation table
  name.vec=c(OverallCorr$varaibles[3],OverallCorr$varaibles[5],OverallCorr$varaibles[12],OverallCorr$varaibles[17],
             OverallCorr$varaibles[45],OverallCorr$varaibles[46],OverallCorr$varaibles[49],OverallCorr$varaibles[50])
  
  pdf("StatsCor.pdf") 
  for (i in 1:length(name.vec)) {
    cor.compare(name.vec[i])
  }
  dev.off()
  cor.compare= function(StatName){
    par(mfrow=c(2,2))
    o1= ggplot(Guards,aes(height,Guards[[StatName]])) + geom_point() + geom_smooth(method='loess')  + ggtitle("Guards")+ labs(y=StatName)
    o2= ggplot(Forwards,aes(height,Forwards[[StatName]])) + geom_point() + geom_smooth(method='loess') + ggtitle("Forwards")+ labs(y=StatName)
    o3= ggplot(Centers,aes(height,Centers[[StatName]])) + geom_point() + geom_smooth(method='loess')  + ggtitle("Centers")+ labs(y=StatName)
    o4= ggplot(statsM,aes(height,statsM[[StatName]])) + geom_point() + geom_smooth(method='loess') + ggtitle("overall")+ labs(y=StatName)
    grid.arrange(o1, o2, o3, o4, ncol=2,nrow=2)
    
  }
  
   #we will make a new table that combines all Positions for calculation
   tempG= data.table(pos="G",Height=Guards$height,TRB=Guards[["TRB%"]],BLK=Guards[["BLK%"]],FG=Guards[["FG%"]]
                     ,WS48=Guards[["WS/48"]],FT=Guards[["FT%"]],P3=Guards[["3P%"]],STL=Guards[["STL%"]],AST=Guards[["AST%"]])
   tempF= data.table(pos="G",Height=Forwards$height,TRB=Forwards[["TRB%"]],BLK=Forwards[["BLK%"]],FG=Forwards[["FG%"]]
                     ,WS48=Forwards[["WS/48"]],FT=Forwards[["FT%"]],P3=Forwards[["3P%"]],STL=Forwards[["STL%"]],AST=Forwards[["AST%"]])
   tempC= data.table(pos="G",Height=Centers$height,TRB=Centers[["TRB%"]],BLK=Centers[["BLK%"]],FG=Centers[["FG%"]]
                     ,WS48=Centers[["WS/48"]],FT=Centers[["FT%"]],P3=Centers[["3P%"]],STL=Centers[["STL%"]],AST=Centers[["AST%"]])
   pramData= rbind(tempG,tempF,tempC)
  
   pdf("test315.pdf")
   ggscatterhist(
     pramData, y = "Height", x = "TRB",
     color = "pos", size = 3, alpha = 0.6,
     palette = c("#00AFBB", "#E7B800", "#FC4E07"),
     margin.params = list(fill = "pos", color = "black", size = 0.2)
   )
  dev.off()
  
  
   
  
  # pdf("HeightPCA.pdf")
  #  dataPPca= PCA(numericData,scale.unit = T,graph = T,quanti.sup = 49)
  #  PcaPlot = fviz_pca_var(dataPPca, labelsize = 0.1, repel = TRUE,cex=0.2)
  #  dev.off()
  

