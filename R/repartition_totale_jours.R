#Le but de ce code est de pour les 31 jours de l'étude (au total même si par individu l'étude dure 14-16 jours)
#avoir le nombre de déplacement faits ce jour-là au total

library(readr)
library(ggplot2)

data<-read.csv("originalData.csv")

#On récupère l'ensemble des journées de l'étude

Journees<-unique(data$jour)
Nbre_de_journees<-length(Journees) #Ca fait bien 31

#Pour chaque journée de l'étude on compte le nombre de mesures effectuées ce jour

days<-c()
trips<-c()

for(i in 1:Nbre_de_journees){
  today<-Journees[i]
  days<-c(days,as.integer(today))
  trips<-c(trips,sum(data$jour==today))
}

#On met sous forme de dataframe pour tracer avec ggplot2

mydata<-as.data.frame(cbind(days,trips))

#On trace dans un fichier.png

png("graphs/repartition_des_sorties_par_jour.png")

ggplot(data=mydata,aes(days,trips,fill=trips))+
  geom_bar(stat="identity")+
  scale_fill_gradient(low="green",high="red")

dev.off()

#Pour avoir des résultats significatifs, on recoupe par jour (lundi,mardi,..) grâce à des congruences modulo 7
# Le premier jour de l'étude, le 22/01/2018 est un lundi, pour que tous les jours soient également représentés 
#on prend les données jusqu'au 28eme jour
semaine<-c(1,2,3,4,5,6,7)
#On initialise un vecteur de taille 7 :
Nbre<-c()
for (i in 1:7) {
  Nbre<-c(Nbre,0)
}

#Puis on remplit Nbre à l'aide de days et trips

for(i in 1:28){
  Nbre[1+(i-1)%%7]<-Nbre[1+(i-1)%%7]+trips[i]
}

#Il n'y a plus qu'à plot

newdata<-as.data.frame(cbind(semaine,Nbre))

#Un fichier png

png("graphs/repartitionSemaine.png")

ggplot(data=newdata,aes(semaine,Nbre,fill=Nbre))+
  geom_bar(stat="identity")+
  scale_fill_gradient(low="purple",high="orange")

dev.off()