require(data.table)
require(ggplot2)
require(dplyr)
require(jsonlite)

unzip('data/train.json.zip')

data <- jsonlite::fromJSON('train.json', simplifyDataFrame = T)


sapply(data, function(c) length(c))


cols <- names(data)

data$description

cols
sapply(cols, function(c) data[c] %>% unlist %>% table)

df <- data.frame(price = data['price'] %>% unlist(use.names = F) %>% as.numeric,
                 interest_level = data['interest_level'] %>% unlist(use.names = F),
                 longitude = data['longitude'] %>% unlist(use.names = F),
                 latitude = data['latitude'] %>% unlist(use.names = F),
                 bedrooms = data['bedrooms'] %>% unlist(use.names = F) %>% as.numeric,
                 num_photos = data['photos'] %>% unlist(recursive = F, use.names = F) %>% lapply(length) %>% unlist) %>% data.table


df[, price_norm:= (price - mean(price))/sd(price)]
df[, price_outlier:= ifelse(abs(price_norm) > 5, T,F)]

data$features

cols
data$manager_id %>% unlist %>% table %>% length

ggplot(df[price_outlier == F], aes(x = log(price))) + geom_histogram(bins = 200)

ggplot(df, aes(x = num_photos, y = log(price))) + geom_jitter(aes(color = interest_level), alpha = 0.5)

df$num_photos %>% hist

ggplot(df[price_outlier == F], aes(x = interest_level, y = log(price))) + geom_boxplot()

data$bathrooms

names(data)

data$interest_level
tibble(unlist(data$interest_level))
tibble(unlist(data$bathrooms))

data$features

df <- lapply(data, function(l)as.vector(unlist(l)))

df_features <- lapply(data$features, function(l) unlist(l))

df_features$`2463`
sapply(df, print(NROW))

df$features
df$bathrooms

df$bathrooms

View(df)

data <- data.frame(tibble(iunlist(data$interest_level)))
data

# it may be that the slope between price and interest level varies based on features..use facets on features
ggplot(df, aes(x = num_photos, y = log(price))) + geom_jitter(aes(color = interest_level), alpha = 0.5) + facet_wrap(~ bedrooms)

data$longitude %>% unlist %>% dist


df[, ln_price:= log(price)]

m1 <- glm(interest_level ~ ln_price, data = df,family = binomial(link = 'mlogit'))

summary(m1)
coef(m1)



require(MASS)


redf$interest_level

m2 <- polr(interest_level ~ ln_price + num_photos, data = df)
fitted <- predict(m2,type = 'probs') 
fitted2 <- data.table(fitted/colMeans(fitted))
fitted2$class <- apply(fitted2, MARGIN = 1, FUN = which.max)
fitted2[, class:= names(fitted2)[class]]
fitted2$actual <- df$interest_level
fitted2[,mean(class == actual)]


## should probably try uSING ROC or One Vs All classification