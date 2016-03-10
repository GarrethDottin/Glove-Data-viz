import sys
import BaseHTTPServer
import SimpleHTTPServer
import urlparse
import json
import argparse
import glove


def getQuery(queryParsed):
    try:
        return queryParsed['q'][0].decode("utf-8")
    except:
        return None

def matches(command, pathList):
    return any( command==path or command.startswith(path+"/") for path in pathList )

def getFlag(queryParsed, arg):
    return arg in queryParsed and queryParsed[arg][0]=='1'

#Content serialized
def sendContent(self, content, format="json", status=200):
    self.send_response(status)
    self.send_header('Content-Type', 'text/' + format + '; charset=utf-8')
    self.end_headers()

    self.wfile.write(content)
    self.wfile.close()

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):


    def do_GET(self):
        try:
            #separate into function
            parsedParams = urlparse.urlparse(self.path)
            queryParsed = getQuery(parsedParams.query)
            query = getQuery(queryParsed)
            status = 200

            command = parsedParams.path.strip("/")
            if command == "glove":
                assert g_glove is not None, "glove dataset not loaded, please use the --glove argument"
                limit = int(queryParsed.get('limit', [100])[0])

                # By default, we use global projection if and only if this was asked for at startup time.
                useGlobalProjection = g_glove.projection is not None
                if 'globalProjection' in queryParsed:
                    askedForGlobalProjection = queryParsed['globalProjection'][0] == '1'
                    assert not (
                    askedForGlobalProjection and not useGlobalProjection), "Global projection has not been set up."
                    useGlobalProjection = askedForGlobalProjection

                keywords = query.split(" ")

                if len(keywords) > 1:
                    wordOrWords = keywords
                else:
                    wordOrWords = keywords[0]

                jsonResult = g_glove.queryJson(wordOrWords,
                                               limit=limit, useGlobalProjection=useGlobalProjection)

            elif matches(command, ("vis",)):
                return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

            else:
                self.sendContent("unknown service: " + command, status=400)
                return

            self.sendContent(jsonResult, status=status)
        except:
            sys.stderr.write(
                "Exception catched and re-raised for request " + str(parsedParams) + " aka " + str(self.path) + "\n")
            raise

g_glove = None
