from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

Bars = [0,1,2,3,4,5,6,7,8]

def play():
  result = weigh(Bars[0:3], Bars[3:6])

  if result == '=':
    fake_bar = final_weighing(Bars[6:9])
  elif result == '>':
    fake_bar = final_weighing(Bars[3:6])
  elif result == '<':
    fake_bar = final_weighing(Bars[0:3])
  return fake_bar

def final_weighing(bars):
  result = weigh([bars[0]], [bars[1]])
  if result == '=':
    return bars[2]
  elif result == '>':
    return bars[1]
  elif result == '<':
    return bars[0]
  else:
    return -1

def init():
  global ResetButton, WeighButton, LeftBowl, RightBowl

  driver = webdriver.Chrome(ChromeDriverManager().install(), )
  driver.get("http://ec2-54-208-152-154.compute-1.amazonaws.com/")

  LeftBowl = [
    driver.find_element_by_id("left_0"),
    driver.find_element_by_id("left_1"),
    driver.find_element_by_id("left_2")
  ]

  RightBowl = [
    driver.find_element_by_id("right_0"),
    driver.find_element_by_id("right_1"),
    driver.find_element_by_id("right_2")
  ]

  WeighButton = driver.find_element_by_id("weigh")
  ResetButton = driver.find_element_by_xpath("//button[text()='Reset']")

  return driver

# loads the scales and clicks Weigh button
def weigh(left, right):
  global ResetButton, LeftBowl, RightBowl, WeighButton

  ResetButton.click()

  for i in range(len(left)):
    LeftBowl[i].send_keys(str(left[i]))

  for i in range(len(right)):
    RightBowl[i].send_keys(str(right[i]))

  WeighButton.click()
  time.sleep(3)
  return wait()

# waits for results of the weighing
def wait():
  global Driver, weighings

  weighing = WebDriverWait(Driver, 10).until(EC.visibility_of_element_located((By.XPATH, build_path(weighings))))
  weighings.append(weighing.text)
  return weighing_result(Driver)

# determines the results of the weighing
def weighing_result(driver):
  return driver.find_element_by_xpath("//div[@class='result']/button").text

# builds xpath of the expected weighing display
def build_path(weighings):
  index = "[" + str(len(weighings) + 1) + "]"
  return "//div[@class='game-info']/ol/li" + index

# checks the fake bar
def game_over(fake):
  global Driver

  bar = Driver.find_element_by_id("coin_" + str(fake))
  time.sleep(2)
  bar.click()

  result = None
  alert = None

  WebDriverWait(Driver, 10).until(EC.alert_is_present())
  alert = Driver.switch_to.alert

  if alert.text == "Yay! You find it!":
    result = True
  else:
    result = False

  time.sleep(4)
  alert.dismiss()
  return result

def main():
  global Driver, weighings
  Driver = init()
  weighings = []

  # start the game
  fake_bar = play()

  if game_over(fake_bar):
    print (f'WIN !!! Fake bar is {fake_bar}')

    for j in range(len(weighings)):
      print(f'weighing [{j+1}] : {weighings[j]}')

  Driver.close()

if __name__ == "__main__":
  main()
