from wiki_crawler import wiki_crawler

seedUrl = "https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones"
num_pages = 1000

def main():
  wiki_crawler(seedUrl, num_pages)

main()