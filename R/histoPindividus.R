library(ggplot2)
library(readr)
#Grâce à ce code on va tracer l'histogramme pour 5 individus.

p<-10

#Importation des données

data <- read_csv("~/Desktop/Ponts/Projets/PIR_Mobilite_Urbaine/DonnéesBrutes/Geo4Cast_100_idf_3_Waël.csv")
#write.csv (df, nomfichier)
#On récupère les individus

Individus<-unique(data$device)

for (i in 1:p) {
  #On recupere l'individu i
  Individu<-subset(data,data$device==Individus[i])
  #On récupère la liste des lieux qu'il a visité
  lieux<-unique(Individu$ID_sejour_1km)
  N<-length(lieux)
  #Puis on calcule la fréquentation de chaque lieu
  freq<-c()
  x<-c()
  j<-1
  for(lieu in lieux){
    freq<-c(freq,sum(Individu$ID_sejour_1km==lieu))
    x<-c(x,j)
    j<-j+1
  }
  #Ensuite on met freq sous la forme d'un dataframe
  places=as.factor(x)
  placesfreq=cbind(places,freq)
  LieuxFreq<-as.data.frame(placesfreq)
  #On va enregistrer l'histogramme dans un fichier.png
  png(paste0("graphs/hist", i, ".png"))
  
  g<-ggplot(data=LieuxFreq,aes(places,freq,fill=freq))+
    geom_bar(stat = "identity")+
    scale_fill_gradient(low="green",high="red")
  print (g)
  dev.off()
}