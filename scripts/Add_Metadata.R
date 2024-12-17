

All_Demos_means <- read.csv("~/BSR_Simulations/data/clean_data/All_Combos_Mean_Summary_Stats.csv")
All_Demos_vars <- read.csv("~/BSR_Simulations/data/clean_data/All_Combos_Variance_Summary_Stats.csv")


## Create metadata columns for each aspect of the runcode
All_Demos_means$Demo <- NA
All_Demos_means$Alpha <- NA
All_Demos_means$Rec_rate <- NA
All_Demos_means$Mut_rate <- NA
for (i in 1:nrow(All_Demos_means)) {
  All_Demos_means$Demo[i] <- strsplit(All_Demos_means$Run_Code[i], split = "_")[[1]][1]
  All_Demos_means$Alpha[i] <- strsplit(All_Demos_means$Run_Code[i], split = "_")[[1]][2]
  All_Demos_means$Rec_rate[i] <- strsplit(All_Demos_means$Run_Code[i], split = "_")[[1]][3]
  All_Demos_means$Mut_rate[i] <- strsplit(All_Demos_means$Run_Code[i], split = "_")[[1]][4]
}



## Create metadata columns for each aspect of the runcode
All_Demos_vars$Demo <- NA
All_Demos_vars$Alpha <- NA
All_Demos_vars$Rec_rate <- NA
All_Demos_vars$Mut_rate <- NA
for (i in 1:nrow(All_Demos_vars)) {
  All_Demos_vars$Demo[i] <- strsplit(All_Demos_vars$Run_Code[i], split = "_")[[1]][1]
  All_Demos_vars$Alpha[i] <- strsplit(All_Demos_vars$Run_Code[i], split = "_")[[1]][2]
  All_Demos_vars$Rec_rate[i] <- strsplit(All_Demos_vars$Run_Code[i], split = "_")[[1]][3]
  All_Demos_vars$Mut_rate[i] <- strsplit(All_Demos_vars$Run_Code[i], split = "_")[[1]][4]
}


## write the files again 
write.csv(All_Demos_means, '~/BSR_Simulations/data/clean_data/All_Combos_Mean_Summary_Stats.csv')
write.csv(All_Demos_vars, '~/BSR_Simulations/data/clean_data/All_Combos_Variance_Summary_Stats.csv')

