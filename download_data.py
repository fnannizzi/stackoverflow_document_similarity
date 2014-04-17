import stackexchange
import sys

def download():
    stackOverflow = stackexchange.Site(stackexchange.StackOverflow, '8D*yq20*d3XiEdEn46BmMQ((')

    # set the throttling property to avoid being banned
    stackOverflow.impose_throttling = True
    stackOverflow.throttle_stop = False

    with open("outfile.txt", 'w') as outfile:
        for num in range(0,10):
            # add some timing code to make sure the script actually 
            # finishes without being throttled
            # 100 is the max number of questions we can request at once
            questions = stackOverflow.questions(pagesize=100)
            for question in questions:
                outfile.write("title:{0} tags:".format(question.title.encode('utf-8')))
                outfile.write(','.join(question.tags).encode('utf-8'))
                outfile.write("\n")
    

download()
