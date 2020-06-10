library(xml2)
library(rvest)

URL <- "http://awoiaf.westeros.org/index.php/List_of_characters"
session <- read_html(URL)

urls <- session %>%
    html_nodes("li") %>%
    html_nodes("a") %>%
    html_attr("href") %>%
    xml2::url_absolute(url)

chars <- session %>%
    html_nodes("li") %>%
    html_nodes("a") %>%
    html_attr("title")
