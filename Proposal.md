# Section 1: Motivation and Purpose

Our role: Data scientist consultancy firm

Target audience: Internal management

Better customer understanding and good customer services can improve internal efficiencies resulting in higher revenues. To address this challenge, we propose building a data visualization app that allows the top administration to visually explore the dataset for identifying key characteristics of our customers, missed opportunities (in terms of cancelled reservations) and services ordered by our customers for understanding their needs. Our app will illustrate the key metrics and trends and further allow users to explore different aspects of this data by filtering and re-ordering of different variables in order to understand customer's needs in a better way. 

# Section 2: Description of the data

The data set we used in building the dashboard comes from the Hotel Booking demand datasets from Antonio, Almeida and Nunes at Instituto Universitário de Lisboa (ISCTE-IUL), Lisbon, Portugal (Antonio, Almeida, and Nunes 2019). The data can be found from the GitHub Repository [here](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11). There are two sets of real world hotel reservation data contained in this data set, one resort hotel and one city hotel. Each row in this dataset is an individual hotel reservoir information due to arrive between July 1st, 2015 and August 31st, 2017. There are a total of 119,390 booking details with 31 features. 40,060 observations from the resort hotel and 79,330 observations from the city hotel are included in this data set.
In the preliminary investigation of the data set, we find out there are a total 119,300 booking details with 34% on resort hotels and 66% on city hotels. Each observation has numerical features such as number of adults, number of previous bookings not cancelled etc., and categorical features such as code of room type reserved, type of meal booked etc. In the future work, we would like to select the best features to be displayed in our app in order to deliver an informative dashboard.


# Section 3: Research questions and usage scenarios

Mary is an Executive Director with the ABC Hotel, Portuguese. and she wants to see the overall trend in the market and what relationships exist among the variables available in the collected data to make better marketing and internal policies. When Mary logs on to the "XXX app", she will see the summary of all the key metrics such as reservations made by year/months to see the seasonality effect on the business. She can also manage better internal resources as per seasonal fluctuation. Also, This will help her in making strategies to attract customers in the off-season. She can also filter trends by locations, type of customers etc. so that she can focus on one segment and can design marketing promotions to allure them. She can see the main factors that are contributing the most in the success story such as the top 5 types of meal ordered. She can also see the effect of one variable on another variable, for example the impact of having kids on demanding extra services.