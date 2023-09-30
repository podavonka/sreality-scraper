# sRelity Scraper

This project implements the solution to the task:

*Use scrapy framework to scrape the first 500 items (title, image url) from sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker-compose command so that I can just run "docker-compose up" in the Github repository and see the scraped ads on 127.0.0.1:8080 page.*

### User manual

Clone the project into the folder of the system on which Docker is installed:

```
git clone https://github.com/podavonka/sreality-scraper.git
```

Start Docker and run the program from your local git repository using the command:

```
docker-compose up
```

Wait about 30 seconds while selenium processes the necessary pages of the site and see the result at the address *127.0.0.1:8080*.

### Time spent on project implementation

![luxonis_time](https://github.com/podavonka/sreality-scraper/assets/145363658/fd62d4ce-f6e4-43bc-be6b-1f59c0c9e6ad)
