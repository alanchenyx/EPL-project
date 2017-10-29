"""

main prediction file

read input from collections of matches in mongoDB
produce out as excel file and also save result to result database

"""

import csv
import datetime
import nltk
import numpy
from pymongo import MongoClient
import config

# loop throught match db and produce 2 txt for each match, relatively for each team

client = MongoClient(config.connection)
matchdbs = client.match.collection_names()
resultdb = client.result

half_time = 45
break_time = 15
stoppage_time = 2
game_length = half_time*2 + break_time + stoppage_time*2
peak_distance = 5

def main():
    for db in matchdbs:
        print(db)
        print('---------------------------------------------------------------')
        dbName = client.get_database(db)
        teamA = dbName.name.split('_')[0].lower()
        teamB = dbName.name.split('_')[1].lower()

        coll = client.match.get_collection(db)
        predict(teamA, coll, db)
        predict(teamB, coll, db)


def predict(team, collection, outputName):
    teamName = team
    coll = collection
    team_keywords = [teamName]
    team_players = []
    timeCounter = 0

    #time interval in seconds
    timInterval = 60
    team_tweets = []
    team_pos_sentiment = []
    team_neg_sentiment = []
    result = {}

    with open('.\\doc\\' + teamName + '.csv', 'r') as f:

        reader = csv.reader(f)
        mylist = list(reader)
        players = []
        for row in mylist:
            if row[1] != '' and row[1] != 'Player':
                players.append(row[1].split(',')[0].lower())
                # print(players)

    team_players = players
    team_keywords = team_keywords + team_players
    # print('team players: ' + str(team_players))
    # print('team keywords: ' + str(team_keywords))

    for doc in coll.find():
        startTime = doc['created_at']
        break

    while timeCounter < game_length:
        # print(timeCounter)
        dt = datetime.datetime.strptime(startTime, '%a %b %d %H:%M:%S +0000 %Y')
        dfshift = dt + datetime.timedelta(0, timInterval)
        endTime = dfshift.strftime('%a %b %d %H:%M:%S +0000 %Y')

        interval_tweets = list(coll.find({'created_at': {'$gte': startTime, '$lt': endTime}}))

        team_tweets_interval = []
        posCount = 0
        negCount = 0
        for tweet in interval_tweets:
            for keyword in team_keywords:
                if keyword in tweet['text']:
                    team_tweets_interval.append(tweet['text'])
                    if tweet['vader_tag'] == 'pos':
                        posCount += 1
                    if tweet['vader_tag'] == 'neg':
                        negCount += 1

        try:
            pos_sentiment = float(posCount) / len(team_tweets_interval)
        except ZeroDivisionError:
            pos_sentiment = 0.0
        try:
            neg_sentiment = float(negCount) / len(team_tweets_interval)
        except ZeroDivisionError:
            neg_sentiment = 0.0

        # print('appending tweets: '+str(len(team_tweets_interval)))
        team_tweets.append(team_tweets_interval)
        # print('length of teamtweets: '+str(len(team_tweets)))
        # print('appending sentiment: '+str(sentiment))
        team_pos_sentiment.append(pos_sentiment)
        team_neg_sentiment.append(neg_sentiment)
        # print('length of senti: '+str(len(team_sentiment)))
        timeCounter += 1
        startTime = endTime

    i = 0
    timeline = []
    volume = []
    result = open(str(outputName) + '_' + teamName + 'stats' + '.csv', 'w')
    # while i < 120:
    #     # minute tweet_number %pos %neg
    #     result.write(str(i) + ',' + str(len(team_tweets[i])) + ',' + (str(team_pos_sentiment[i])) + ',' + str(
    #         team_neg_sentiment[i]) + ',' + '\n')
    #     timeline.append(i)
    #     volume.append(len(team_tweets[i]))
    #     i += 1

    # print(timeline)
    # print(volume)
    # print(team_pos_sentiment)
    # print('---------------------------------------------------------------')

    peak_time_goal = []
    peak_time_foul = []
    pos_q3 = numpy.percentile(team_pos_sentiment, 75)
    volume_q3 = numpy.percentile(volume, 75)
    neg_q3 = numpy.percentile(team_neg_sentiment, 75)
    for i in range(len(team_pos_sentiment)):
        if team_pos_sentiment[i] > pos_q3 and team_pos_sentiment[i] > team_pos_sentiment[i - 1] and volume[
            i] > volume_q3 and ((i >= peak_distance and i <= half_time) or (i > (half_time + break_time) and i < game_length)):
            try:
                if (i - peak_time_goal[-1]) >= peak_distance:
                    peak_time_goal.append(i)
            except IndexError:
                peak_time_goal.append(i)

        if team_neg_sentiment[i] > neg_q3 and team_neg_sentiment[i] > team_neg_sentiment[i - 1] and volume[
            i] > volume_q3 and ((i >= peak_distance and i <= half_time) or (i > (half_time + break_time) and i < game_length)):
            try:
                if (i - peak_time_foul[-1]) >= peak_distance:
                    peak_time_foul.append(i)
            except IndexError:
                peak_time_foul.append(i)

    if len(peak_time_goal) > 0:
        for goal in peak_time_goal:
            # look for the player mentioned most frequently for each goal
            goal_tweets = team_tweets[goal]
            player_count = []
            for tweet in goal_tweets:
                for player in team_players:
                    if player in tweet:
                        player_count.append(player)

            fdist = nltk.FreqDist(player_count)

            if goal > (half_time + break_time):
                # if happens at second-half , minus break time
                goal = goal - break_time
            try:
                predict_player = fdist.max()
                prediction = str(outputName) + '_' + teamName + ' ,' + predict_player + ' at ' + str(goal)
                result['goal'] = prediction
                print(str(outputName) + '_' + teamName + ' ,' + predict_player + ' goal at ' + str(goal) + '\'')
                print()
            except ValueError:
                # print(str(outputName)+'_'+teamName + ' ,no goals!')
                pass

    #print('-------------------------------------------------------')

    if len(peak_time_foul) > 0:
        for foul in peak_time_foul:
            # look for the player mentioned most frequently for each goal
            foul_tweets = team_tweets[foul]
            player_count = []
            for tweet in foul_tweets:
                for player in team_players:
                    if player in tweet:
                        player_count.append(player)

            fdist = nltk.FreqDist(player_count)

            if foul > (half_time + break_time):
                # if happens at second-half , minus break time
                foul = foul - break_time
            try:
                predict_player = fdist.max()
                prediction = str(outputName) + '_' + teamName + ' ,' + predict_player + ' at ' + str(foul)
                result['foul'] = prediction
                print(str(outputName) + '_' + teamName + ' ,' + predict_player + ' foul at ' + str(foul) + '\'')
                print()
            except ValueError:
                # print(str(outputName)+'_'+teamName + ' ,no goals!')
                pass

    #save to mongoDB
    resultdb.save(result)


    #print('---------------------------------------------------------------')


# tweets = list(sourcedb.find({'created_at': {'$gte':startTime, '$lt':endTime}}))
# for tweet in tweets:
#     # if 'chelsea' in tweet['processed_text']:
#     targetdb.save(tweet)
#
#
# team_tweets = []
#
#


# give prediction for each of the collections of matches
# for db in matchdbs:
#     coll = client.get_database(db)
#


if __name__ == '__main__':
    main()
