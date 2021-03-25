import queue
import threading
import requests
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MultiWebbing():
    """call this class first to initiate MultiWebbing and the individual threads"""
    def __init__(self, num_threads, web_module="requests", webdriver=webdriver.Chrome):
        #TODO add harry's bots as web_module option
        """Creates a job queue, lock object, session and creates the number of requested threads"""
        sys.path
        self.job_queue = queue.Queue()
        self.results_queue = queue.Queue()
        self.lock = threading.Lock() #session and lock can be overwritten on a per job basis
        self.threads = []
        # self.result_thread = self.ResultThread(self)
        self.num_threads = num_threads
        self.web_module = web_module
        self.queue_added = 0#total number of items added to the queue

        if self.web_module == "requests":
            self.session = requests.session()
        if self.web_module == "selenium":
            self.web_module = web_module
            self.driver = webdriver

        for i in range(self.num_threads):
            self.threads.append(self.Thread(i, self))

    def start(self):
        """Call after initiating a Threading object to start the threads."""
        for thread in self.threads:
            thread.start()

    def finish(self):
        """When you are ready to finish your threads (e.g. when your work queue is empty and you have visited all pages, call this method to stop and join the threads."""
        for thread in self.threads:
            thread.join()

    def queue_job(self, job_function, url, job_data):
        """wrapper for mw.job_queue.put()"""
        self.job_queue.put(Job(job_function, url, job_data))
        self.queue_added += 1

    # class ResultThread(threading.Thread):

    #     def __init__(self, multiwebbing):
            

    #     def run(self):
    #         #execute on thread.start()
    #         #job_function should have a Job object as its sole argument. Can update job argument with additional attributes if needed for the function
    #         print(f" ** Starting thread - {self.number}")

    class Thread(threading.Thread):
        #define how the threads function
        #TODO add verbosity for more detailed output options
        def __init__(self, number, multiwebbing):
            threading.Thread.__init__(self)
            self.web_module = multiwebbing.web_module
            self.number = number
            self._stop_event = threading.Event()
            self.job_queue = multiwebbing.job_queue
            self.results_queue = multiwebbing.results_queue
            self.lock = multiwebbing.lock
            self.result = None
            if self.web_module == "requests":
                self.session = multiwebbing.session
            self.options = None
            if self.web_module == "selenium":
                self.options = Options() 
                self.options.add_argument("--headless")
                self.driver = multiwebbing.driver(options=self.options)

        def run(self):
            #execute on thread.start()
            #job_function should have a Job object as its sole argument. Can update job argument with additional attributes if needed for the function
            print(f" ** Starting thread - {self.number}")

            while not self._stop_event.isSet():
                #thread will continuously check the queue for work until the master process joins the threads, and the stop_event signal is sent
                try:
                    #get a job
                    job = self.job_queue.get(block=False) 
                    job.set_thread(self) #give job access to thread attributes

                except queue.Empty:
                    pass

                else:
                    #print("Thread " + self.name + ": Getting profile: " + profile.url)
                    #execute main thread function
                    job.get_url()
                    job.result = job.function(job)
                    #put job in result queue
                    self.results_queue.put(job)
                    
            print(f" ** Completed thread - {self.number}")

        def join(self, timeout=None):
            #send stop event to terminate the work loop before calling join
            self._stop_event.set()
            super().join(timeout)
            print(f" ** Joined thread - {self.number}")

class Job:
    #holds all the information needed for the worker threads to make a request and execute the job_function
    def __init__(self, function, url, custom_data, session = None, lock = None):
        self.url = url
        self.custom_data = custom_data #your data structure, accessible inside your job function (list, dictionary, list of list, list of dictionaries...)
        self.request = None
        self.status_code = None
        self.function = function
        self.session = None #can set session and lock per job, or can leave unset and attributes will be taken from thread set during init
        self.lock = None
        self.result = None

    def set_thread(self, thread):
        """allows access to thread attributes(e.g. session, lock) that may be needed for the job function"""
        self.thread = thread
        # if not set in init, use thread session and lock 
        if self.thread.web_module == "requests":
            if self.session == None:    
                self.session = self.thread.session
        elif self.thread.web_module == "selenium":
            self.driver = thread.driver
        if self.lock == None:
            self.lock = self.thread.lock

    def get_url_requests(self):
        """Make a get request to Job.url. Sets Job.request to the result, returns 1 upon an error"""
        try:
            self.request = self.session.get(self.url)               
        except requests.exceptions.ConnectionError:
            self.request = None
            return False

        return True

    def get_url_selenium(self):
        """Make a get request to Job.url. Sets Job.request to the result, returns 1 upon an error"""
        try:
            self.thread.driver.get(self.url)            
        except: #TODO: find the specific connection error/timeout exception name in selenium
            return False

        return True

    def get_url(self):
        if self.thread.web_module == "requests":
            self.get_url_requests()
        elif self.thread.web_module == "selenium":
            self.get_url_selenium()

