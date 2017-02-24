install.packages("dplyr")
install.packages("stringr")
library(dplyr)
library(stringr)

csv1 <- read.csv("log20070201.csv")

#creating additional columns
#flags for extension
csv1<-mutate(csv1, isHtml = ifelse((grepl(".htm$", extention)), "1", "0"))
csv1<-mutate(csv1, isTxt = ifelse((grepl(".txt$", extention)), "1", "0"))
csv1<-mutate(csv1, isPdf = ifelse((grepl(".pdf$", extention)), "1", "0"))


#dat columns