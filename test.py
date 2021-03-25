import os
from time import sleep
from selenium import webdriver
from multi_webbing import multi_webbing as mw

def job_function_selenium(job):
    job.get_url()

    print(job.driver.current_url)

def job_function_requests(job):
    job.get_url()

    print(job.request.url)

os.environ["DISPLAY"] = ":0"

test = {}

print("Testing selenium:")
try:
    num_threads = 2
    my_threads = mw.MultiWebbing(num_threads, web_module="selenium")
    my_threads.start()


    for i in range(4):
        my_threads.job_queue.put(mw.queue_job(job_function_selenium, f"https://www.google.com/search?q={i}", "string", ))


    while my_threads.job_queue.qsize() > 0:
        sleep(5)

    my_threads.finish()

except:
    test["selenium"] = False

else:
    test["selenium"] = True

print("Selenium test complete, testing requests:")

# try:
num_threads = 2
my_threads = mw.MultiWebbing(num_threads)
my_threads.start()


for i in range(4):
    my_threads.queue_job(job_function_requests, f"https://www.google.com/search?q={i}", "string", )


while my_threads.job_queue.qsize() > 0:
    sleep(5)

my_threads.finish()

# except:
#     test["requests"] = False

# else:
#     test["requests"] = True

print("Tests Complete")

for key,val in test.items():
    if val:
        print (f"{key} test successful.")
    else:
        print (f"{key} test failed.")

