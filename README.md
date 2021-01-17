# infotext
Connecting to the internet through text messaging.
In a time where information is equal to power the usage of text messaging through a Twillio back end can be used for a wide spread distrabution of information through text messaging.

## How to set infoText up
To use infoText you must have a Twillio account that has a phone number with Text message support. Open up ngrok and setup a secure public url for port *x* web server using the command "ngrok http x" in the command line then copy the web interface URL and paste into the text URL connection tab under the Twillio phone number that's being used. Then simply run the infoText.py file and text a command to the set up phone number.
#### Required Python Libraries for full functionality
Flask, nltk, wikipedia, CurrencyRates, beautifulsoup4, urllib2, heapq
## Functions
#### Wikipedia:
Send a text message in the "wikipedia (topic)" format for a condenced, sumarized version of the wikipedia page for your topic.
#### News:
Send a text message in the "news" format for a condeced, sumarized version of the top BBC articles for the day.
#### Currency Exchange:
Send a text message in the "exchange (currencyA)(currencyB)" to get the exchange rate of currencyA to currencyB.
