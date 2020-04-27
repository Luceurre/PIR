#Ce code a pour but  de récupérer le nombre de sortie par jour pour un individu

library(readr)
library(ggplot2)

data<-read.csv("originaldata.csv")

Individu=subset(data,data$device=="Device 1005")

Nombre_de_mesures<-length(Individu$device)
#On numérote le jours 1,...15 la date exacte n'est pas importante pour l'instant
#Le problème c'est qu'il n'y a pas eu de mesures tous les jours.
#Et que l'étude n'a pas commencé le même jour pour tous les individus

Premier_jour<-Individu$jour[1]
Dernier_jour<-Individu$jour[Nombre_de_mesures]

pjour<-as.integer(Premier_jour)
djour<-as.integer(Dernier_jour)

duree_de_letude<-1+djour-pjour

days<-c()
trips<-c()

for(i in 1:duree_de_letude){
  days<-c(days,i)
  trips<-c(trips,0)
}

Journees<-unique(Individu$jour)

for(i in 1:length(Journees)){
  day=as.integer(Journees[i])
  nb=sum(Individu$jour==Journees[i])
  trips[day]<-nb
}
#On combine sour forme de dataframe pour ggplot2

montruc<-cbind(days,trips)
mydata<-as.data.frame(montruc)

#Il ne reste qu'à tracer
png("graphs/device1005parjour.png")

ggplot(data=mydata,aes(days,trips,fill=trips))+
  geom_bar(stat="identity")+
  scale_fill_gradient(low="green",high = "red")

dev.off()