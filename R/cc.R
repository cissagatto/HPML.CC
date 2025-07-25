cat("\n###########################################################")
cat("\n# HPML.CC: START                                          #")
cat("\n###########################################################\n\n")


# clean
rm(list=ls())


##############################################################################
# CLASSIFIER CHAINS                                                          #
# Copyright (C) 2025                                                         #
#                                                                            #
# This code is free software: you can redistribute it and/or modify it under #
# the terms of the GNU General Public License as published by the Free       #
# Software Foundation, either version 3 of the License, or (at your option)  #
# any later version. This code is distributed in the hope that it will be    #
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of     #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General   #
# Public License for more details.                                           #
#                                                                            #
# Prof. Elaine Cecilia Gatto - UFLA - Lavras, Minas Gerais, Brazil           #
# Prof. Ricardo Cerri - USP - São Carlos, São Paulo, Brazil                  #
# Prof. Mauri Ferrandin - UFSC - Blumenau, Santa Catarina, Brazil            #
# Prof. Celine Vens - Ku Leuven - Kortrijik, West Flanders, Belgium          #
# PhD Felipe Nakano Kenji - Ku Leuven - Kortrijik, West Flanders, Belgium    #
#                                                                            #
# BIOMAL - http://www.biomal.ufscar.br                                       #
#                                                                            #
##############################################################################



###############################################################################
# SET WORKSAPCE                                                               #
###############################################################################
library(here)
library(stringr)
FolderRoot <- here::here()
FolderScripts <- here::here("R")


cat("\n############################################")
cat("\n# HPML.CC: R Options Configuration         #")
cat("\n############################################\n\n")
options(java.parameters = "-Xmx64g")  # JAVA
options(show.error.messages = TRUE)   # ERROR MESSAGES
options(scipen=20)                    # number of places after the comma


########################################
parameters = list()
########################################


cat("\n##################################################")
cat("\n# HPML.CC: Reading Datasets-Original.csv         #")
cat("\n##################################################\n\n")
setwd(FolderRoot)
datasets <- data.frame(read.csv("datasets-original.csv"))
parameters$Datasets.List = datasets


cat("\n#################################################")
cat("\n# HPML.CC: GET ARGUMENTS FROM COMMAND LINE      #")
cat("\n#################################################\n\n")
args <- commandArgs(TRUE)


# config_file = "~/HPML.CC/config-files/cc-corel5k-1.csv"

config_file <- args[1]


if(file.exists(config_file)==FALSE){
  cat("\n################################################################")
  cat("#\n HPML.CC: Missing Config File! Verify the following path:     #")
  cat("#\n ", config_file, "                                            #")
  cat("##################################################################\n\n")
  break
} else {
  cat("\n###################################################")
  cat("\n# HPML.CC: Properly loaded configuration file!    #")
  cat("\n###################################################\n\n")
}


cat("\n##################################################")
cat("\n# HPML.CC: Config File                           #")
cat("\n##################################################\n\n")
config = data.frame(read.csv(config_file))
print(config)



cat("\n#################################################")
cat("\n# HPML.CC: Getting Parameters                   #")
cat("\n#################################################")
FolderScripts = toString(config$Value[1])
FolderScripts = str_remove(FolderScripts, pattern = " ")
parameters$Config.File$FolderScripts = FolderScripts

dataset_path = toString(config$Value[2])
dataset_path = str_remove(dataset_path, pattern = " ")
parameters$Config.File$Dataset.Path = dataset_path

folderResults = toString(config$Value[3]) 
folderResults = str_remove(folderResults, pattern = " ")
parameters$Config.File$Folder.Results = folderResults

implementation = toString(config$Value[4])
implementation = str_remove(implementation, pattern = " ")
parameters$Config.File$Implementation = implementation

dataset_name = toString(config$Value[5])
dataset_name = str_remove(dataset_name, pattern = " ")
parameters$Config.File$Dataset.Name = dataset_name

number_dataset = as.numeric(config$Value[6])
parameters$Config.File$Number.Dataset = number_dataset

number_folds = as.numeric(config$Value[7])
parameters$Config.File$Number.Folds = number_folds

number_cores = as.numeric(config$Value[8])
parameters$Config.File$Number.Cores = number_cores

ds = datasets[number_dataset,]
parameters$Dataset.Info = ds


cat("\n################################################################\n")
print(ds)
cat("\n################################################################\n\n")


cat("\n#####################################################")
cat("\n# HPML.CC: Creating temporary processing folder     #")
cat("\n#####################################################\n\n")
if (dir.exists(folderResults) == FALSE) {dir.create(folderResults)}



cat("\n##################################################")
cat("\n# HPML.CC: Loading R Sources                     #")
cat("\n##################################################\n\n")
source(file.path(FolderScripts, "libraries.R"))
source(file.path(FolderScripts, "utils.R"))



cat("\n#########################################")
cat("\n# HPML.CC: Get directories              #")
cat("\n#########################################\n\n")
diretorios <- directories(parameters)
parameters$Directories = diretorios



cat("\n####################################################################")
cat("\n# Checking the dataset tar.gz file                                 #")
cat("\n####################################################################\n\n")
str00 = paste(dataset_path, "/", ds$Name,".tar.gz", sep = "")
str00 = str_remove(str00, pattern = " ")

if(file.exists(str00)==FALSE){
  
  cat("\n######################################################################")
  cat("\n# The tar.gz file for the dataset to be processed does not exist!    #")
  cat("\n# Please pass the path of the tar.gz file in the configuration file! #")
  cat("\n# The path entered was: ", str00, "                                  #")
  cat("\n######################################################################\n\n")
  break
  
} else {
  
  cat("\n####################################################################")
  cat("\n# tar.gz file of the DATASET loaded correctly!                     #")
  cat("\n####################################################################\n\n")
  
  # COPIANDO
  str01 = paste("cp ", str00, " ", diretorios$folderDataset, sep = "")
  res = system(str01)
  if (res != 0) {
    cat("\nError: ", str01)
    break
  }
  
  # DESCOMPACTANDO
  str02 = paste("tar xzf ", diretorios$folderDataset, "/", ds$Name,
                ".tar.gz -C ", diretorios$folderDataset, sep = "")
  res = system(str02)
  if (res != 0) {
    cat("\nError: ", str02)
    break
  }
  
  #APAGANDO
  str03 = paste("rm ", diretorios$folderDataset, "/", ds$Name,
                ".tar.gz", sep = "")
  res = system(str03)
  if (res != 0) {
    cat("\nError: ", str03)
    break
  }
  
}




##############################################################################

if(implementation=="utiml"){
  # 
  # setwd(FolderScripts)
  # source("run-utiml.R")
  # 
  # cat("\n\n############################################################")
  #   cat("\n# RSCRIPT ECC START                                     #")
  #   cat("\n############################################################\n\n")
  # timeFinal <- system.time(results <- run.ecc.utiml(ds, 
  #                                                   dataset_name,
  #                                                   number_dataset, 
  #                                                   number_cores, 
  #                                                   number_folds, 
  #                                                   folderResults))  
  # 
  # cat("\n\n#####################################################")
  #   cat("\n# RSCRIPT SAVE RUNTIME                              #")
  #   cat("\n#####################################################\n\n")
  # result_set <- t(data.matrix(timeFinal))
  # setwd(diretorios$folderCC)
  # write.csv(result_set, "Runtime-Final.csv")
  # x.minutos =(1 * as.numeric(result_set[3]))/60
  # setwd(diretorios$folderCC)
  # write(x.minutos, "minutos.txt")
  # 
  # 
  # cat("\n\n#####################################################")
  #   cat("\n# RSCRIPT DELETE                                   #")
  #   cat("\n####################################################\n\n")
  # str5 = paste("rm -r ", diretorios$folderDataset, sep="")
  # print(system(str5))
  # 
  # 
  # 
  # cat("\n\n######################################################")
  #   cat("\n# RSCRIPT COPY TO GOOGLE DRIVE                       #")
  #   cat("\n######################################################\n\n")
  # origem = diretorios$folderCC
  # destino = paste("nuvem:ECC/Utiml/", dataset_name, sep="")
  # comando = paste("rclone -P copy ", origem, " ", destino, sep="")
  # cat("\n", comando, "\n") 
  # a = print(system(comando))
  # a = as.numeric(a)
  # if(a != 0) {
  #   stop("Erro RCLONE")
  #   quit("yes")
  # }
  # 
  
} else if(implementation=="rf"){
  
  source(file.path(FolderScripts, "run-python.R"))
  
  cat("\n#########################################################")
  cat("\n# HPML.CC: START                                        #")
  cat("\n#########################################################\n\n")
  timeFinal <- system.time(results <- run.cc.python(parameters))  
  
  
  cat("\n#####################################################")
  cat("\n# HPML.CC: SAVE RUNTIME                             #")
  cat("\n#####################################################\n\n")
  result_set <- t(data.matrix(timeFinal))
  setwd(diretorios$folderCC)
  write.csv(result_set, "Runtime-Final.csv")
  
  
  cat("\n###################################################")
  cat("\n# HPML.CC: DELETE ALL TEMPORARY FILES             #")
  cat("\n###################################################\n\n")
  str5 = paste("rm -r ", diretorios$folderDataset, sep="")
  print(system(str5))
  
  
  cat("\n##############################################################")
  cat("\n# HPML.CC: COMPRESS RESULTS                                  #")
  cat("\n##############################################################\n\n")
  str3 <- paste0(
    "tar -zcvf ", parameters$Directories$folderResults, "/",
    parameters$Dataset.Info$Name, "-results-cc.tar.gz ",
    "-C ", parameters$Directories$folderResults, " ."
  )
  print(system(str3))
  
  
  cat("\n######################################################")
  cat("\n# COPY TO HOME                                       #")
  cat("\n#####################################################\n\n")
  
  str0 = paste0(FolderRoot, "/Reports")
  if(dir.exists(str0)==FALSE){dir.create(str0)}
  
  str3 = paste(parameters$Directories$folderResults , "/",
               parameters$Dataset.Info$Name, 
               "-results-cc.tar.gz", sep="")
  
  str4 = paste("cp ", str3, " ", str0, sep="")
  print(system(str4))
  
  
} else {
  
  # 
  # setwd(FolderScripts)
  # source("run-mulan.R")
  # 
  # 
  # cat("\n\n############################################################")
  # cat("\n# RSCRIPT ECC START                                     #")
  # cat("\n############################################################\n\n")
  # timeFinal <- system.time(results <- run.ecc.mulan(ds, 
  #                                                   dataset_name,
  #                                                   number_dataset, 
  #                                                   number_cores, 
  #                                                   number_folds, 
  #                                                   folderResults))  
  # 
  # 
  # 
  # cat("\n\n#####################################################")
  # cat("\n# RSCRIPT SAVE RUNTIME                              #")
  # cat("\n#####################################################\n\n")
  # result_set <- t(data.matrix(timeFinal))
  # setwd(diretorios$folderCC)
  # write.csv(result_set, "Runtime-Final.csv")
  # x.minutos = (1 * as.numeric(result_set[3]))/60
  # setwd(diretorios$folderCC)
  # write(x.minutos, "minutos.txt")
  # 
  # 
  # cat("\n\n#################################################")
  # cat("\n# RSCRIPT DELETE                                  #")
  # cat("\n###################################################\n\n")
  # str5 = paste("rm -r ", diretorios$folderDataset, sep="")
  # print(system(str5))
  # 
  # 
  # cat("\n\n######################################################")
  #   cat("\n# RSCRIPT COPY TO GOOGLE DRIVE                       #")
  #   cat("\n######################################################\n\n")
  # origem = diretorios$folderCC
  # destino = paste("nuvem:ECC/Mulan/", dataset_name, sep="")
  # comando = paste("rclone -P copy ", origem, " ", destino, sep="")
  # cat("\n", comando, "\n") 
  # a = print(system(comando))
  # a = as.numeric(a)
  # if(a != 0) {
  #   stop("Erro RCLONE")
  #   quit("yes")
  # }
  # 
  
  
} 


# cat("\n\n###################################################################")
# cat("\n# ECC ECC: COMPRESS RESULTS                                      #")
# cat("\n#####################################################################\n\n")
# str3 = paste("tar -zcvf ", diretorios$folderResults, "/", 
#              dataset_name, "-results-ECC.tar.gz ", 
#              diretorios$folderResults, sep="")
# print(system(str3))


# cat("\n\n##############################################################")
# cat("\n# ECC ECC: COPY TO FOLDER REPORTS                           #")
# cat("\n###############################################################\n\n")
# str0 = "~/Ensemble-Classifier-Chains/Reports/"
# if(dir.exists(str0)==FALSE){dir.create(str0)}
# str1 = paste(diretorios$folderResults, "/", dataset_name,
#              "-results-ECC.tar.gz", sep="")
# str4 = paste("cp -r ", str1 , " ", str0, sep="")
# print(system(str4))



cat("\n#######################################################")
cat("\n# CLEAN                                               #")
cat("\n#######################################################\n\n")
cat("\nDelete folder \n")
str5 = paste("rm -r ", folderResults, sep="")
print(system(str5))


cat("\n################################################################")
cat("\n# RSCRIPT SUCCESSFULLY FINISHED                                #")
cat("\n################################################################\n\n")


rm(list = ls())
gc()

###############################################################################
# Please, any errors, contact us: elainececiliagatto@gmail.com                #
# Thank you very much!                                                        #                                #
###############################################################################
