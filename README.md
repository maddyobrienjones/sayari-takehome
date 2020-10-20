# Sayari Takehome Project

**scraper.py** - Web crawler utilizing the requests library to scrape the North Dakota Secretary of State Business Search web app

**request_data.csv** - The data collected by above web crawler - contains business data about registered agents and owners, among other extraneous information

**graph.py** - Code used to create a NetworkX graph of the business, agent and owner data, and to plot that data

**business_owneragent_plot.png** - Graph plot (also below)

As shown in the graph below, it seems that many of the businesses are small and independent. However, there are a few registered agents who are connected to many businesses.

![Business/Agent/Owner Relationship Plot](https://github.com/maddyobrienjones/sayari-takehome/blob/main/business_owneragent_plot.png)
