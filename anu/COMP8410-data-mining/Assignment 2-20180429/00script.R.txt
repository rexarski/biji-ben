set.seed(8410)
dat <- read.csv('dat/ALL.csv')
# "Date" to date
dat$Date <- as.Date(as.character(dat$Date), format="%Y%m%d")

# divide data by industry
write.csv(dat[dat$Sector=="Technology",], file="dat/tech.csv")
write.csv(dat[dat$Sector=="Financial_Services",], file="dat/finn.csv")
write.csv(dat[dat$Sector=="Agriculture",], file="dat/agri.csv")
write.csv(dat[dat$Sector=="Basic_Materials/Resources",], file="dat/rsrc.csv")
write.csv(dat[dat$Sector=="Retail/Wholesale",], file="dat/sale.csv")
write.csv(dat[dat$Code=="WOW",], file="dat/WOW.csv")

write.csv(dat, file="dat/ALL-lite.csv")

# remove DayofMonth, Month, Year, WeekofYear, DayofYear
drops <- c("DayofMonth","Month","Year","WeekofYear","DayofYear",
           "SubSector","Weekday","Close.Open","Change","High.Low",
           "HMLOL")
dat <- dat[,!names(dat) %in% drops]




# # EXPLORATARY ANALYSIS
# library(plotly)
# plot_ly(dat, x = ~dat$Open, y = ~dat$Close,  type="scatter", mode = "markers" , color = ~dat$Sector , 
#         marker=list( size=20 , opacity=0.5)  )

# SINGLE STOCK ANALYSIS (TS)

WOW <- read.csv("dat/WOW.csv")

library(latticeExtra)
obj1 <- xyplot(WOW$Close ~ WOW$Date, type="l", lwd=2)
obj2 <- xyplot(WOW$Volume ~ WOW$Date, type="l", lwd=2)

doubleYScale(obj1, obj2, text=c("close price", "volume"), add.ylab2 = TRUE) # need to change label name, change tick space etc.


for (i in 1:nrow(dat)){
    
}
