# Multi-Webbing
A multi-threaded libary for web scraping in python, built upon the python threading modules. Supports using requests and selenium for making web requests.

## Set Up

1. Install the module from pip

        pip install multi_webbing

2. Import the Module into your python file

        from multi_webbing import multi_webbing as mw

3. Set the Number of threads and create a multi-webbing object. By default this will use the requests module, but this can be changed to selenium by passing the web_module="selenium" option to MultWebbing.

        num_threads = 4
        my_threads = mw.MultiWebbing(num_threads) #intialize threading
        
4. Start the threads. The threads will now continuously check the work queue for work.

        my_threads.start

5. To put a job in the queue, call the job_queue.put() method of the multi-webbing object.

        my_threads.job_queue.put(mw.Job(job_id, job_function, url, [job_data, job_type]))

6. When you are ready, stop the threads

        my_threads.finish()

You might find it useful to check the size of the queue in a loop before calling finish:
       
        while my_threads.queue.qsize() > 0:
                pass
        my_threads.finish()

## Job Function

When creating a job, you need to pass a job function that the thread will call to do some work.

The job function has 3 required arguments and 2 optional ones:

### Required Arguments

1. url

The URL of the webpage to be worked on.

2. job_function

The function the thread should call when it picks the job out of the queue. See [Job Function](#Job-Function).

3. custom_data

An argument that can be used for anything to be accessed inside the job function.

### Optional Arguments

4. session

A requests.session object. If this is not set, the job will use the session set when the MultiWebbing object was instanced.

5. lock

A threading.lock object. If this is not set, the job will use the lock set when the MultiWebbing object was instanced.
                
## Returning Data From Threads

It is not possible to directly return data from a thread to the main process using the "return" statement.

Instead you should create a list or dictioary in the main process, then put this in the custom_data argument of the job. You can then use       
        
        dictionary.update() 
        
or 

        list.append()
        
in the job function. The main process will be able to access the updated/appended data. A note: while the update and append functions are thread safe, some other functions are not (e.g. JSON.dumps()) and you may need to wrap them in a lock to prevent a race condition.

Multiple variables and data structures can be accessed in the job by placing them in a list.


## Job Function

The job function will be called from a thread when it gets a job from the queue.

An example using using the requests module:

    def job_function(job):

        job_data = job.custom_data[0] #in this example, a dictionary which contains the data processed from scraping
        job_type = job.custom_data[1] #in this example, a string
        
        get_url_success = job.get_url() #get the URL
        if get_url_success: #check the request connected
            if job.request.status_code == 200: #check that the URL was recieved OK
                job.lock.acquire() #update/append are thread safe but other operations elsewhere (e.g. JSON.dumps) might not be
                if job.type == "jobtype1": #do something
                    job.custom_data.update({"key1":"val3", "key2":"val4"})
                if job.type == "jobtype2": #do something different
                    job.custom_data.update({"key1":"val3", "key2":"val4"})
                job.lock.release()

Using requests, you can access the request object by calling job.request. For example, to obtain the text attribute from the visited page:

        text = job.request.text 

Using selenium you can access the webdriver by calling job.driver, for example:

        element = driver.find_element_by_xpath('xpath_string')
