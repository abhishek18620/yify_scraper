"""
-*- coding: utf-8 -*-
========================
Python YouTube API
========================

Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com

========================
"""

import json
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen
import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0" 

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                 message=MISSING_CLIENT_SECRETS_MESSAGE)



class YouTubeApi():

    def get_video_comment(self):

        def load_comments(self):
            for item in mat["items"]:
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                print("Comment by {}: {}".format(author, text))
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        rauthor = reply['snippet']['authorDisplayName']
                        rtext = reply["snippet"]["textDisplay"]

                    print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")

        parser = argparse.ArgumentParser()
        mxRes = 20
        vid = str()
        parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return")
        parser.add_argument("--videourl", help="Required URL for which comments to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.videourl:
            exit("Please specify video URL using the --videourl=parameter.")

        if not args.key:
            exit("Please specify API key using the --key=parameter.")

        try:
            video_id = urlparse(str(args.videourl))
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet,replies',
                    'maxResults': args.max,
                    'videoId': vid,
                    'textFormat': 'plainText',
                    'key': args.key
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")
            load_comments(self)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                print("\nPage : ", i)
                print("------------------------------------------------------------------")

                load_comments(self)

                i += 1
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def search_keyword(self):

        def load_search_res(self):
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                  videos.append("{} ({})".format(search_result["snippet"]["title"],
                                             search_result["id"]["videoId"]))
                elif search_result["id"]["kind"] == "youtube#channel":
                  channels.append("{} ({})".format(search_result["snippet"]["title"],
                                               search_result["id"]["channelId"]))
                elif search_result["id"]["kind"] == "youtube#playlist":
                  playlists.append("{} ({})".format(search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

            print("Videos:\n", "\n".join(videos), "\n")
            print("Channels:\n", "\n".join(channels), "\n")
            print("Playlists:\n", "\n".join(playlists), "\n")

        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
        parser.add_argument("--search", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                    'q': args.search,
                    'part': 'id,snippet',
                    'maxResults': args.max,
                    'regionCode': args.r,
                    'key': args.key
                }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)
            i = 2

            nextPageToken = search_response.get("nextPageToken")

            videos = []
            channels = []
            playlists = []
            print("\nPage : 1 --- Region : {}".format(args.r))
            print("------------------------------------------------------------------")
            load_search_res(self)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                search_response = json.loads(matches)
                nextPageToken = search_response.get("nextPageToken")
                print("Page : {} --- Region : {}".format(i, args.r))
                print("------------------------------------------------------------------")

                load_search_res(self)

                i += 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def channel_videos(self):

        def load_channel_vid(self):

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    videos.append("{} ({})".format(search_result["snippet"]["title"],
                                             search_result["id"]["videoId"]))

            print("###Videos:###\n", "\n".join(videos), "\n")

        parser = argparse.ArgumentParser()
        mxRes = 20
        parser.add_argument("--sc", help="calls the search by channel by keyword function", action='store_true')
        parser.add_argument("--channelid", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.channelid:
            exit("Please specify channelid using the --channelid= parameter.")

        if not args.key:
            exit("Please specify API key using the --key= parameter.")

        parms = {
                   'part': 'id,snippet',
                   'channelId': args.channelid,
                   'maxResults': args.max,
                   'key': args.key
               }

        try:
            matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

            search_response = json.loads(matches)

            videos = []
            i = 2

            nextPageToken = search_response.get("nextPageToken")
            print("\nPage : 1")
            print("------------------------------------------------------------------")

            load_channel_vid(self)

            while nextPageToken:
                    parms.update({'pageToken': nextPageToken})
                    matches = self.openURL(YOUTUBE_SEARCH_URL, parms)

                    search_response = json.loads(matches)
                    nextPageToken = search_response.get("nextPageToken")
                    print("Page : ", i)
                    print("------------------------------------------------------------------")

                    load_channel_vid(self)

                    i += 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches


def main():
    y = YouTubeApi()

    if str(sys.argv[1]) == "--s":
        y.search_keyword()
    elif str(sys.argv[1]) == "--c":
        y.get_video_comment()
    elif str(sys.argv[1]) == "--sc":
        y.channel_videos()
    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --c to list comments after the filename\nAdd --sc to list vidoes based on channel id")



youtube=get_authenticated_service()
def videos_get_rating(service, **kwargs):
    #kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
    results = service.getRating(
      **kwargs
    ).execute()

    print_results(results)

videos_get_rating(youtube,
                  id='Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI')

#if __name__ == '__main__':
    #videos_get_rating(service)

#    --c --max=20 --videourl=https://www.youtube.com/watch?v=z6S4bszpfpA --key=AIzaSyC_gT7V6gcMJkkyuDv-WkZ-mwkNeqOY23o 
