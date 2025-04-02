library(linkET)
library(ggplot2)
library(ggtext)
library(dplyr)
library(RColorBrewer)
library(cols4all)
library(tidyverse)
speciese <- read.csv("inter-config.csv", header = TRUE)
env <- read.csv("all.csv", header = TRUE)
cor2 <- correlate(speciese)  
corr2 <- cor2 %>% as_md_tbl()
write.csv(corr2, file = "pearson_correlate(env&env).csv", row.names = TRUE)
#Mantel test
mantel <- mantel_test(env, speciese,  
                      mantel_fun = 'mantel', 
                      spec_select = list(spec01 = 1:1,
                                         spec02 = 2:2,
                                         spec03 = 3:3))
mantel2 <- mantel %>%
  mutate(r = cut(r, breaks = c(-Inf, 0, 0.25, 0.5, 0.75, Inf),
                 labels = c("<0", "0-0.25", "0.25-0.5", "0.5-0.75", ">0.75")),
         p = cut(p, breaks = c(-Inf, 0.001, 0.01, 0.05, Inf),
                 labels = c("<0.001", "0.001-0.01", "0.01-0.05", ">=0.05")))

p4 <- qcorrplot(cor2,
                grid_col = "#A9A9A9",
                grid_size = 0.2,
                type = "upper",
                diag = FALSE) +
  geom_square() +
  scale_fill_gradientn(
    colours = c("#0933CA", "#FFFFFF", "#C12702"), 
    limits = c(0.5, 1) 
  )


p6 <- p4 +
  geom_couple(data = mantel2,
              aes(colour = r, size = p), 
              curvature = nice_curvature(),
              alpha = 0.7)  

p7 <- p6 +
  scale_colour_manual(
    values = c("<0" = "#6E6E6E",   
               "0-0.25" = "#3182BD",   
               "0.25-0.5" = "#9ECAE1",
               "0.5-0.75" = "#FC9272",
               ">0.75" = "#DE2D26")   
  ) +
  scale_size_manual(
    values = c("<0.001" = 2, 
               "0.001-0.01" = 1.5,
               "0.01-0.05" = 1,
               ">=0.05" = 0.6)
  )


p7 <- p7 +
  guides(
    size = guide_legend(title = "Mantel's p",
                        override.aes = list(colour = "grey35"),
                        nrow = 1),  
    colour = guide_legend(title = "Mantel's r",
                          override.aes = list(size = 4),
                          nrow = 1),
    fill = guide_colorbar(title = "Pearson's r")
  ) +
  theme(
    text = element_text(size = 12, family = "serif"),
    plot.title = element_text(size = 14, hjust = 0.5),
    legend.position = "right", 
    axis.text.y = element_text(size = 10, angle = 0, hjust = 1),
    axis.text.x = element_text(size = 10, angle = 45, hjust = 1)
  ) +

  labs(x = "Completed genome distance", 
       y = "Relative fitness", 
       title = "HGT-genome distance")


print(p7)
