# Create data source table by joining inventory to source table and truncating file paths.
library (tidyverse)
read.csv("./data/Y_inventory_working.csv") %>% select(code, Path, Type) ->inv
read.csv("./data/ALL_BrokenSrc20200803_1950_working.csv") -> brk

# JOIN ---- 
brk %>% drop_na (code) %>% left_join (inv) %>%
  transmute ( UniqID,dataType,newType = replace_na(Type, "_review"),brokenPath,newPath = Path) -> joined

# Truncate ---- 
# remove ephemeral clutter at beginning of broken paths in temp. 
# Arc creates these temp dummy sdes if the version of the database is deleted after the mxd was saved. 
joined %>%
  mutate (brokenPath = gsub('^C:\\\\Users\\\\jdmumm\\\\AppData\\\\Local\\\\Temp\\\\16\\\\arc6107\\\\.{37}', '', joined$brokenPath)) %>% 
  distinct (brokenPath, .keep_all = TRUE) %>% # remove duplicate generalized records
  arrange (brokenPath) -> out

# write ----
out %>% write.csv('./out/rosetta_201119.csv', row.names = FALSE)
