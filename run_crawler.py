from spider.tasks import crawl_task

if __name__ == "__main__":
    result = crawl_task.delay("https://google.com")
    print(f"Started crawling. Task ID: {result.id}")
