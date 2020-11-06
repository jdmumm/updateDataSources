library (tidyverse)

read.csv("./data/Y_inventory_working.csv") %>% select(code, Path, Type) ->inv
read.csv("./data/ALL_BrokenSrc20200803_1950_working.csv") -> brk

brk %>% drop_na (code) %>% left_join (inv) %>%
  transmute ( UniqID,dataType,newType = replace_na(Type, "_review"),brokenPath,newPath = Path) -> out

out %>% write.csv('./out/rosetta_201106.csv', row.names = FALSE)  

