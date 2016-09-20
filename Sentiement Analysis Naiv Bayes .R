Data <- read.csv("File",header = TRUE)
names(Data)
library('caret')
library('e1071')

bound <- floor((nrow(Data)/4)*3) 
df <- Data[sample(nrow(Data)), ]
df.train <- Data[1:bound, ]
df.test <- Data[(bound+1):nrow(Data),]

#data Split
dt = sort(sample(nrow(Data), nrow(Data)*.8))
train<-Data[dt,]
test<-Data[-dt,]


names(train)
Training <- train[,c(2,6,7:19)]
names(Training)

names(test)
Testing <- test[,c(6:19)]
names(Testing)


MOdel <- naiveBayes(Target~.,data = Training)
Prediction <- predict(MOdel,Testing)
table(Prediction,test$Target)
confusionMatrix(Prediction,test$Target)
Prediction



write.csv(Prediction,"pred.csv")
write.csv("test.csv")
confusionMatrix(Prediction,df.test$Traget)





