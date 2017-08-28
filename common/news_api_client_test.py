import news_api_client as client

def test_basic():
    # test the function without using parameters
    news = client.getNewsFromSource()
    print news
    # if news is not none then pass
    assert len(news) > 0
    # test the function using parameters
    news = client.getNewsFromSource(sources=['cnn'], sortBy='top') # cnn doesn't support latest sorting
    assert len(news) > 0
    print 'test_basic passed'


if __name__ == "__main__":
    test_basic()