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
        self.lock = threading.Lock() #session and lock can be overwritten on a per job basis
        self.threads = []
        self.web_module = web_module
        self.driver = webdriver
        self.num_threads = num_threads
        if web_module = "requests":
            self.session = requests.session 
        else:
            self.session = None

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

    class Thread(threading.Thread):
        #define how the threads function
        #TODO add verbosity for more detailed output options
        def __init__(self, number, multiWebbing):
            threading.Thread.__init__(self)
            self.web_module = multiWebbing.web_module
            self.number = number
            self._stop_event = threading.Event()
            self.job_queue = multiWebbing.job_queue
            self.lock = multiWebbing.lock
            self.session = multiWebbing.session
            self.options = None
            if self.web_module = "selenium"
                self.options = Options() 
                self.options.add_argument("--headless")
                self.driver = multiWebbing.driver(self.options=options)

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
                    job.function(job)
                    #update the data structure with the returned data

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

    def set_thread(self, thread):
        """allows access to thread attributes(e.g. session, lock) that may be needed for the job function"""
        self.thread = thread
        # if not set in init, use thread session and lock 
        if self.session == None:    
            self.session = self.thread.session
        if self.lock == None:
            self.lock = self.thread.lock

    def get_url(self)
        if self.web_module="requests":
            get_url_requests(self)
        elif: self.web_module="selenium":
            get_url_selenium(self)

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