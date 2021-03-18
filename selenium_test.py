from selenium import webdriver
import os
import multi_webbing as mw

os.environ["DISPLAY"] = ":0"

num_threads = 4
my_threads = mw.MultiWebbing(num_threads)
my_threads.start()
my_threads.finish()

