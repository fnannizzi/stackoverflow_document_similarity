import stackexchange, sys, time, argparse

def download():

    # Record a start time, so we can time the whole operation. I don't think we care 
    # that much, I just normally add some timing code.
    time_start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("out", help="the name of the output file")
    parser.add_argument("num_iter", help="total number of requests to make", type=int)
    parser.add_argument("--descriptions", help="get questions, tags, and descriptions")

    args = parser.parse_args()
    if args.descriptions:
        print "Fetching questions, tags, and descriptions."
        descriptions_on = True
    else:
        print "Fetching questions and tags."
        descriptions_on = False

    output_filename = args.out
    num_iter = args.num_iter

    # Set up a link to StackOverflow (as opposed to one of the many StackExchange 
    # sites) using our API key. 
    stackOverflow = stackexchange.Site(stackexchange.StackOverflow, '8D*yq20*d3XiEdEn46BmMQ((')
    
    # If we want to fetch the body of the posts as well, we need to specify the request to 
    # include all data
    if descriptions_on:
        stackOverflow.be_inclusive()

    # Set the throttling property to avoid being banned. With this enabled, the 
    # Py-StackExchange wrapper will make sure we don't send requests at a rate that 
    # would get us banned. However, the program just gets shut down if we send 
    # requests too quickly, so we still have to add timing code later.
    stackOverflow.impose_throttling = True
    stackOverflow.throttle_stop = False

    num_fetched = 0
    with open(output_filename, 'w') as outfile:
        for num in range(0,num_iter):
            # add some timing code to make sure the script actually 
            # finishes without being throttled
            # 100 is the max number of questions we can request at once
            questions = stackOverflow.questions(pagesize=100)
            num_fetched += 100
            for question in questions:
                outfile.write("title:{0} tags:".format(question.title.encode('utf-8')))
                outfile.write(','.join(question.tags).encode('utf-8'))
                if descriptions_on:
                    outfile.write("description:{0}".format(question.body.encode('utf-8')))
                outfile.write("\n")
            time.sleep(3) # sleep for 3 seconds to ensure we don't get cut off

    time_done = time.time()
    print "Fetched {0} questions of {1} requested in {2} seconds.".format(num_fetched, (num_iter*100), ((time_done - time_start)/60))
    

download()
