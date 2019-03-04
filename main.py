
# import time
# from selenium import webdriver
#
# driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
# driver.get('http://www.google.com/xhtml');
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()

import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://smithstix.com/music")

time.sleep(2)

concerts = driver.find_elements_by_class_name("event-row")

# concerts[0]

for concert in concerts:
    print(concert.find_element_by_class_name("date-outer").text)
    # print(concert)

print(len(concerts))


time.sleep(2)
driver.quit()