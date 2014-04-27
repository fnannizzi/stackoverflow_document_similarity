import stackexchange, sys, time, argparse


def download():

    # Record a start time, so we can time the whole operation. I don't think we care 
    # that much, I just normally add some timing code.
    time_start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("out", help="the name of the output file")
    parser.add_argument("--descriptions", help="get questions, tags, and descriptions")

    args = parser.parse_args()
    if args.descriptions:
        print "Fetching questions, tags, and descriptions."
        descriptions_on = True
    else:
        print "Fetching questions and tags."
        descriptions_on = False

    output_filename = args.out

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

    duplicate_sets = initialize_list()
    with open(output_filename, 'w') as outfile:
        for dup_set in duplicate_sets:
            outfile.write("<begin_duplicate_set>\n")
            for dup in dup_set:
                question = stackOverflow.question(dup)
                outfile.write("<begin_title>\n{0}\n<end_title>\n <begin_tags>\n".format(question.title.encode('utf-8')))
                outfile.write(','.join(question.tags).encode('utf-8'))
                outfile.write("\n<end_tags>\n")
                if descriptions_on:
                    outfile.write("<begin_body>\n{0}\n<end_body>\n".format(question.body.encode('utf-8')))
                outfile.write("\n")
                #time.sleep(4) # sleep for 4 seconds to ensure we don't get cut off
            outfile.write("<end_duplicate_set>\n")

    time_done = time.time()
    print "Fetched {0} duplicate sets in {1} seconds.".format(len(duplicate_sets), (time_done - time_start))


def initialize_list():
    duplicate_sets = []

    # java iterate map duplicates
    dup = [1066589, 46898]
    duplicate_sets.append(dup)

    return duplicate_sets

download()
