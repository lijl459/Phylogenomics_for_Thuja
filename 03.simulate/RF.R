library("ggplot2")


setwd("E:\\?????????\\project\\Thuja\\ILS\\RF")
a = read.table("observed.RF.txt", header = TRUE)
b = read.table("simulated.txt", header=TRUE)
head(a)

ggplot(b, aes(x = as.factor(RF), y = Frequency)) + 
  geom_violin(fill = "#BBD6E8") +
  theme_bw(base_size = 19) + 
  theme(panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), 
        axis.line = element_line(colour = "black"))+
  labs(y = "Frequency", x = "RF") +
  geom_point(data=a, aes(x = as.factor(RF), y = Frequency), color = "#EA7255", size = 2.8)



