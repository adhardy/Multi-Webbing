from selenium import webdriver
import os
import multi_webbing as mw
from time import sleep

def job_function(job):
    job.get_url()

    print(job.driver.current_url)

os.environ["DISPLAY"] = ":0"

num_threads = 2
my_threads = mw.MultiWebbing(num_threads)
my_threads.start()


for i in range(4):
    my_threads.job_queue.put(mw.Job(job_function, f"https://www.google.com/search?q={i}", "string", ))


while my_threads.job_queue.qsize() > 0:
    sleep(5)

my_threads.finish()