from producer.checkers.websitechecker import WebsiteChecker
import schedule
import time

if __name__ == "__main__":
    # get website checker

    checker = WebsiteChecker("https://www.verkkokauppa.com/fi/myymalat/jatkasaari")
    def job():
        status = checker.check_get()
        if status is not None:
            print(status)

    schedule.every(10).seconds.do(job_func=job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # create a publishers producer