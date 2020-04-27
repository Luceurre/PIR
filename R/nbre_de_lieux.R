#Ce code trace la courbe du nombre de lieux visités par individu 

library(readr)
library(ggplot2)
library(RColorBrewer)
display.brewer.all()
#Importation des données

data<-read_csv("~/PycharmProjects/PIR/data/data_4.csv")

#Récupération de l'ensemble des individus

Individus=unique(data$device)

#On parcourt la liste des individus en remplissant deux vecteurs pour un plot :

nbre<-c()
ind<-c()
i<-1

for(Individu in Individus){
  ind<-c(ind,i)
  d<-subset(data,data$device==Individu)
  lieux<-unique(d$ID_sejour_1km)
  nbre<-c(nbre,length(lieux))
  i<-i+1
}

individus=as.factor(ind)

matt<-cbind(ind,nbre)

donnee<-as.data.frame(matt)

png("~/PycharmProjects/PIR/R/graphs/nombre_de_lieux_par_individus.png")

ggplot(data=donnee, aes(x = ind,y = nbre,fill=nbre))+
  geom_bar(stat="identity")+
  scale_fill_gradient(low = "yellow",high="red")

dev.off()


#On peut également tracer la distribution du nombre de lieux sur 100 individus

png("~/PycharmProjects/PIR/R/graphs/distribution_du_nombre_de_lieux.png")

g<-ggplot(data=donnee,aes(nbre))

print(g)

dev.off()