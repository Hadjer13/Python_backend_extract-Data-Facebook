import facebook
import datetime
import json

def scrapRS(d):
    serializer = CollecteRSSerializer(data=d)
    if serializer.is_valid():
        app_id = serializer.data['appID']
        app_secret = serializer.data['appSecret']
        print app_secret
        print app_id

    serializer2 = SourceRSSerializer(data=d2)
    if serializer2.is_valid():

      #  app_id = "175905439591084"
        #app_secret = "551dc63b4566af6aa7b5109b41d9971a"  # DO NOT SHARE WITH ANYONE!


        access_token = app_id + "|" + app_secret

        # requete HTTP
        def request_until_succeed(url):
            req = urllib2.Request(url)
            success = False
            while success is False:
                try:
                    response = urllib2.urlopen(req)
                    if response.getcode() == 200:
                        success = True
                except Exception, e:
                    print e
                    time.sleep(5)

                    print "Error for URL %s: %s" % (url, datetime.datetime.now())
                    print "Retrying."

            return response.read()

        # Needed to write tricky unicode correctly to csv
        def unicode_normalize(text):
            return text.translate({0x2018: 0x27, 0x2019: 0x27, 0x201C: 0x22, 0x201D: 0x22,
                                   0xa0: 0x20}).encode('utf-8')

        def getFacebookPageFeedData(page_id, access_token, num_statuses):

            # Construct the URL string
            # Reactions parameters
            base = "https://graph.facebook.com/v2.6"
            node = "/%s/posts" % page_id
            fields = "/?fields=message,link,created_time,type,name,id," + \
                     "comments.limit(0).summary(true),shares,reactions" + \
                     ".limit(0).summary(true)"
            parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
            url = base + node + fields + parameters

            # retrieve data
            data = json.loads(request_until_succeed(url))

            return data

        def getReactionsForStatus(status_id, access_token):

            # Reactions are only accessable at a single-post endpoint

            base = "https://graph.facebook.com/v2.6"
            node = "/%s" % status_id
            reactions = "/?fields=" \
                        "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
                        ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
                        ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
                        ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
                        ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
                        ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
            parameters = "&access_token=%s" % access_token
            url = base + node + reactions + parameters

            # retrieve data
            data = json.loads(request_until_succeed(url))

            return data

        def processFacebookPageFeedStatus(status, access_token):

            # The status is now a Python dictionary, so for top-level items,
            # we can simply call the key.

            # Additionally, some items may not always exist,
            # so must check for existence first

            status_id = status['id']
            status_message = '' if 'message' not in status.keys() else \
                unicode_normalize(status['message'])
            link_name = '' if 'name' not in status.keys() else \
                unicode_normalize(status['name'])
            status_type = status['type']
            status_link = '' if 'link' not in status.keys() else \
                unicode_normalize(status['link'])

            # Time needs special care since a) it's in UTC and
            # b) it's not easy to use in statistical programs.

            status_published = datetime.datetime.strptime(
                status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
            status_published = status_published + \
                               datetime.timedelta(hours=-5)  # EST
            status_published = status_published.strftime(
                '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

            # Nested items require chaining dictionary keys.

            num_reactions = 0 if 'reactions' not in status else \
                status['reactions']['summary']['total_count']
            num_comments = 0 if 'comments' not in status else \
                status['comments']['summary']['total_count']
            num_shares = 0 if 'shares' not in status else status['shares']['count']

            # Counts of each reaction separately; good for sentiment
            # Only check for reactions if past date of implementation:
            # http://newsroom.fb.com/news/2016/02/reactions-now-available-globally/

            reactions = getReactionsForStatus(status_id, access_token) if \
                status_published > '2016-02-24 00:00:00' else {}

            num_likes = 0 if 'like' not in reactions else \
                reactions['like']['summary']['total_count']

            # Special case: Set number of Likes to Number of reactions for pre-reaction
            # statuses

            num_likes = num_reactions if status_published < '2016-02-24 00:00:00' \
                else num_likes

            def get_num_total_reactions(reaction_type, reactions):
                if reaction_type not in reactions:
                    return 0
                else:
                    return reactions[reaction_type]['summary']['total_count']

            num_loves = get_num_total_reactions('love', reactions)
            num_wows = get_num_total_reactions('wow', reactions)
            num_hahas = get_num_total_reactions('haha', reactions)
            num_sads = get_num_total_reactions('sad', reactions)
            num_angrys = get_num_total_reactions('angry', reactions)

            # Return a tuple of all processed data

            return (status_id, status_message, link_name, status_type, status_link,
                    status_published, num_reactions, num_comments, num_shares,
                    num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys)

        def scrapeFacebookPageFeedStatus(page_id, access_token):
            with open(page_id + '_facebook_statuses.csv', 'w') as file:
                file.write(codecs.BOM_UTF8)
                w = csv.writer(file)
                w.writerow(["status_id", "status_message", "link_name", "status_type",
                            "status_link", "status_published", "num_reactions",
                            "num_comments", "num_shares", "num_likes", "num_loves",
                            "num_wows", "num_hahas", "num_sads", "num_angrys"])

                has_next_page = True
                num_processed = 0  # keep a count on how many we've processed
                scrape_starttime = datetime.datetime.now()

                print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)

                statuses = getFacebookPageFeedData(page_id, access_token, 100)

                while has_next_page:
                    for status in statuses['data']:

                        # Ensure it is a status with the expected metadata
                        if 'reactions' in status:
                            tuple = processFacebookPageFeedStatus(status,
                                                                  access_token)

                            status_id = tuple.__getitem__(0).encode('utf-8')
                            status_message = tuple.__getitem__(1)
                            link_name = tuple.__getitem__(2)
                            status_type = tuple.__getitem__(3).encode('utf-8')
                            status_link = tuple.__getitem__(4)
                            status_published = tuple.__getitem__(5).encode('utf-8')
                            num_reactions = tuple.__getitem__(6)
                            num_comments = tuple.__getitem__(7)
                            num_shares = tuple.__getitem__(8)
                            num_likes = tuple.__getitem__(9)
                            num_loves = tuple.__getitem__(10)
                            num_wows = tuple.__getitem__(11)
                            num_hahas = tuple.__getitem__(12)
                            num_sads = tuple.__getitem__(13)
                            num_angrys = tuple.__getitem__(14)
                            key_insert = {"status_id": status_id,
                                          "status_message": status_message,
                                          "link_name": link_name,
                                          "status_type": status_type,
                                          "status_link": status_link,
                                          "status_published": status_published,
                                          "num_reactions": num_reactions,
                                          "num_comments": num_comments,
                                          "num_shares": num_shares,
                                          "num_likes": num_likes,
                                          "num_loves": num_loves,
                                          "num_wows": num_wows,
                                          "num_hahas": num_hahas,
                                          "num_sads": num_sads,
                                          "num_angrys": num_angrys
                                          }
                           #ici insert save

                        # output progress occasionally to make sure code is not
                        # stalling
                        num_processed += 1
                        if num_processed % 100 == 0:
                            print "%s Statuses Processed: %s" % \
                                  (num_processed, datetime.datetime.now())

                    # if there is no next page, we're done.
                    if 'paging' in statuses.keys():
                        statuses = json.loads(request_until_succeed(
                            statuses['paging']['next']))
                    else:
                        has_next_page = False

                print "\nDone!\n%s Statuses Processed in %s" % \
                      (num_processed, datetime.datetime.now() - scrape_starttime)

        def getPage(access,url):
            graph = facebook.GraphAPI(access_token=access, version='2.7')

            page1 = graph.request('?id=' + url)

            id1 = page1['id']

            nbfans1 = graph.request(id1 + '?fields=fan_count')

            page = Page(idPage=data['id'],name=data['name'],link=url,nbAbonnee=data['fan_count'])
            page.save()
            return id1


        if __name__ == '__main__':
            id = getPage(access_token, 'http://facebook.com/djezzy')

            scrapeFacebookPageFeedStatus(id, access_token)

