# Multi-Webbing
A multi-threaded libary for web scraping in python.
## Set Up

        import multi_webbing as mw

        num_threads = 4
        my_threads = mw.MultiWebbing(num_threads) #intialize threading
        my_threads.start #start threads, they are now checking the queue, waiting for work

        my_threads.job_queue.put(mw.Job(job_id, job_function, url, [job_data, job_type])) #put a job in the queue

## Job Function

    def job_function(job): #example

        job_data = job.custom_data[0] #in this example, a dictionary which contains the data being scraped
        job_type = job.custom_data[1] #in this example, a string

        #TODO adjust for selenium
        get_url_success = job.get_url() #get the URL
        if get_url_success: #check the request connected
            if job.request.status_code == 200: #check that the URL was recieved OK
                job.lock.acquire() #update/append are thread safe but other operations elsewhere (e.g. JSON.dumps) might not be
                if job.type == "jobtype1": #do something
                    job.custom_data.update({"key1":"val3", "key2":"val4"})
                if job.type == "jobtype2": #do something different
                    job.custom_data.update({"key1":"val3", "key2":"val4"})
                job.lock.release()