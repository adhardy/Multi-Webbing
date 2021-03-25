import os
from time import sleep
from selenium import webdriver
from multi_webbing import multi_webbing as mw
import queue

def job_function_selenium(job):

    return job.request.url

def job_function_requests(job):

    return job.request.url

os.environ["DISPLAY"] = ":0"

test = {}

print("Testing selenium:")
try:
    num_threads = 2
    my_threads = mw.MultiWebbing(num_threads, web_module="selenium")
    my_threads.start()


    for i in range(4):
        my_threads.queue_job(mw.queue_job(job_function_selenium, f"https://www.google.com/search?q={i}", "string", ))


    while my_threads.job_queue.qsize() > 0:
        sleep(5)

    my_threads.finish()

except:
    test["selenium"] = False

else:
    test["selenium"] = True

print("Selenium test complete, testing requests:")

try:
    num_threads = 2
    my_threads = mw.MultiWebbing(num_threads)
    my_threads.start()


    for i in range(4):
        my_threads.queue_job(job_function_requests, f"https://www.google.com/search?q={i}", "string", )

    results = []

#wait for the job queue to be empty
    while my_threads.job_queue.qsize() > 0:
        pass

#end the threads, ensure last results have been processed
    my_threads.finish()

    qsize = my_threads.results_queue.qsize()
    while qsize > 0:
        try:
            results.append(my_threads.results_queue.get(block=False))
        except queue.Empty: 
            pass
        qsize = my_threads.results_queue.qsize()
        qtest = qsize > 0
        sizetest = my_threads.queue_added < 4
        tnot = not(sizetest and qtest)
        tand = sizetest and qtest 
        
    for job in results:
        print(job.result)

    while my_threads.job_queue.qsize() > 0:
        sleep(5)

except:
    test["requests"] = False

else:
    test["requests"] = True

print("Tests Complete")

for key,val in test.items():
    if val:
        print (f"{key} test successful.")
    else:
        print (f"{key} test failed.")

