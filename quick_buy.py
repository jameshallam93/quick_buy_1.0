import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_soup(response):
    """
    gets the 'soupified' version of the pages html, ready to start parsing
    """
    return BeautifulSoup(response.content, "html.parser")


def get_button_widget(soup):
    """
    finds the 'add to basket' button
    """
    return soup.find("button", {"data-id": "addToCart"})


def check_if_button_disabled(button):
    """
    checks to see if the button has the 'disabled' property
    """
    return button.get("disabled") != None


def product_is_out_of_stock(response):
    """
    gets the add to cart button from the soup and checks to see if it is disabled
    """
    soup = get_soup(response)
    button = get_button_widget(soup)
    return check_if_button_disabled(button)


def add_to_basket(url):
    """
    creates a webdriver and navigates to the url
    clicks the add to basket button
    navigates to the basket webpage
    sleeps for 10 minutes, then closes the browser
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    # assert "MISSION TO MARS" in driver.title

    driver.find_element(by=By.CLASS_NAME, value="b-modal-button").click()
    sleep(5)
    driver.find_element(by=By.CLASS_NAME, value="b-pdp-button_add").click()
    sleep(3)
    driver.get("https://www.swatch.com/en-gb/cart")
    sleep(600)


def alert_product_in_stock(url, alarm_url):
    """
    opens the two urls, one to the shop page and one to the alarm page
    prints when the product came back in stock
    """
    webbrowser.open(url)
    webbrowser.open(alarm_url)
    print(f"Product in stock at time: {datetime.now()}")


def main(url, alarm_url):
    """
    main function, checks to see if the product is in stock
    if it is, it adds it to the basket and opens the two urls
    provided in the command line arguments.
    if not, keeps refreshing the page and rechecking every 5 seconds
    """
    response = requests.get(url)
    while product_is_out_of_stock(response):
        print(f"Product out of stock at time: {datetime.now()}")
        sleep(5)
        response = requests.get(url)

    alert_product_in_stock(url, alarm_url)
    add_to_basket(url)
    sleep(600)


if __name__ == "__main__":
    """
    accepts two optional parameters, url and alarm_url, which point to the
    shop and alarm pages respectively.
    if no parameters are provided, the default values are used
    """
    url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "https://www.swatch.com/en-gb/mission-to-mars-so33r100/SO33R100.html"
    )
    alarm_url = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "https://www.youtube.com/watch?v=umj0gu5nEGs"
    )
    main(url, alarm_url)
