dis_df<-read.table('Dissem_values.tsv',T)
tmp<-dis_df[which(dis_df$word=='alskj'|dis_df$word=='alskjing'|dis_df$word=='alskjer'|dis_df$word=='alskjed'),]
main_uses_df<-tmp[which(tmp$N_w>5),]
main_uses_df$norm_log_freq <- log((main_uses_df$N_w*(10^6))/main_uses_df$N_a)
main_uses_df$norm_freq <- (main_uses_df$N_w*(10^6))/main_uses_df$N_a


pdf('Dissemination&frequency_plots.pdf')

myplotter <- function(point_type,y){
  plot(NULL,xlim=c(0,11),ylim=c(min(main_uses_df[,y]),max(main_uses_df[,y])),xlab = 'Time',ylab = y)
  x=1
  
  mycolors=c('green','blue','red','pink')
  
  legend_text <- c()
  
  for (i in unique(factor(main_uses_df$word)))
  {
    points(main_uses_df[main_uses_df$word==i,]$time,main_uses_df[main_uses_df$word==i,y],col=mycolors[x],pch=point_type)
    lines(main_uses_df[main_uses_df$word==i,]$time,main_uses_df[main_uses_df$word==i,y],col=mycolors[x],pch=point_type)
    
    print(paste(i,mycolors[x]))
    x<- x+1
    
    legend_text <- c(legend_text, i)
    
  }
  title(main=paste(y,"by time"))
  legend('topleft',legend= legend_text, fill= mycolors)
  
}

for (x in c(colnames(main_uses_df)[2:3],colnames(main_uses_df)[7:8])){
  myplotter(18,x)}
dev.off()