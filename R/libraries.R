##############################################################################
# CLASSIFIER CHAINS - MULTI-LABEL CLASSIFICATION                             #
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
# 1 - Prof PhD Elaine Cecilia Gatto                                          #
# 2 - Prof PhD Ricardo Cerri                                                 #
# 3 - Prof PhD Mauri Ferrandin                                               #
# 4 - Prof PhD Celine Vens                                                   #
# 5 - PhD Felipe Nakano Kenji                                                #
# 6 - Prof PhD Jesse Read                                                    #
#                                                                            #
# 1 = Federal University of São Carlos - UFSCar - https://www2.ufscar.br     #
# Campus São Carlos | Computer Department - DC - https://site.dc.ufscar.br | #
# Post Graduate Program in Computer Science - PPGCC                          # 
# http://ppgcc.dc.ufscar.br | Bioinformatics and Machine Learning Group      #
# BIOMAL - http://www.biomal.ufscar.br                                       # 
#                                                                            # 
# 1 = Federal University of Lavras - UFLA                                    #
#                                                                            # 
# 2 = State University of São Paulo - USP                                    #
#                                                                            # 
# 3 - Federal University of Santa Catarina Campus Blumenau - UFSC            #
# https://ufsc.br/                                                           #
#                                                                            #
# 4 and 5 - Katholieke Universiteit Leuven Campus Kulak Kortrijk Belgium     #
# Medicine Department - https://kulak.kuleuven.be/                           #
# https://kulak.kuleuven.be/nl/over_kulak/faculteiten/geneeskunde            #
#                                                                            #
# 6 - Ecole Polytechnique | Institut Polytechnique de Paris | 1 rue Honoré   #
# d’Estienne d’Orves - 91120 - Palaiseau - FRANCE                            #
#                                                                            #
##############################################################################



###############################################################################
# SET WORKSAPCE                                                               #
###############################################################################
library(here)
library(stringr)
FolderRoot <- here::here()
FolderScripts <- here::here("R")



##############################################################################
# AUTO-INSTALL AND LOAD REQUIRED PACKAGES FOR MULTI-LABEL SCRIPT (v2025)
##############################################################################

# Load 'here' package and define project root folders
if (!require("here", quietly = TRUE)) install.packages("here", dependencies = TRUE)
library(here)
FolderRoot <- here::here()
FolderScripts <- here::here("R")

# List of required CRAN packages
cran_packages <- c(
  "foreign", "stringr", "tidyverse", "parallel", "rJava",
  "RWeka", "mldr", "utiml", "foreach", "doParallel", "caTools"
)

# Function to install and load packages
install_and_load <- function(pkg) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    message(paste("Installing package:", pkg))
    tryCatch({
      install.packages(pkg, dependencies = TRUE)
      library(pkg, character.only = TRUE, quietly = TRUE)
      message(paste("✅ Package", pkg, "successfully installed and loaded."))
    }, error = function(e) {
      message(paste("❌ Error installing package", pkg, ":", e$message))
    })
  } else {
    message(paste("✅ Package", pkg, "is already installed and loaded."))
  }
}

# Install and load all CRAN packages
invisible(lapply(cran_packages, install_and_load))

message("🎉 All packages have been successfully verified and loaded!")

##############################################################################
# Please, any errors, contact us: elainececiliagatto@gmail.com
# Thank you very much!
##############################################################################
