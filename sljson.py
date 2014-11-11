import tornado.ioloop
import tornado.web
import tornado.httpclient
import json

class MainHandler(tornado.web.RequestHandler):

  @tornado.web.asynchronous
  def get(self):
    hclient = tornado.httpclient.AsyncHTTPClient()
    hclient.fetch("http://api.sl.se/api2/TravelplannerV2/trip.json?"+self.request.uri.split("?")[1], self.searchdone)

  def searchdone(self, response):
     data = json.loads(response.body)
     try:
       if type(data["TripList"]["Trip"]) == list:
         utdata = {"TripList":data["TripList"]["Trip"],"Error":{}}
       else:
         utdata = {"TripList":[data["TripList"]["Trip"]],"Error":{}}
     except:
       try:
         utdata = {"TripList":[],"Error":data["TripList"]}
       except:
         utdata = {"TripList":[],"Error":data}
       self.write(utdata)
       self.finish()
       return

     for trip in range(len(utdata["TripList"])):
       messages = []
       try:
         if type(utdata["TripList"][trip]["PriceInfo"]["TariffMessages"]["TariffMessage"]) == list:
           for row in utdata["TripList"][trip]["PriceInfo"]["TariffMessages"]["TariffMessage"]:
             messages.append(row["$"])
         else:
           messages = [utdata["TripList"][trip]["PriceInfo"]["TariffMessages"]["TariffMessage"]["$"]] 
       except:
         nodata = 1
       utdata["TripList"][trip]["PriceInfo"]["TariffMessages"] = messages

       try:
         utdata["TripList"][trip]["PriceInfo"]["TariffZones"] = utdata["TripList"][trip]["PriceInfo"]["TariffZones"]["$"]
       except:
         utdata["TripList"][trip]["PriceInfo"]["TariffZones"] = "" 

       try:
         utdata["TripList"][trip]["PriceInfo"]["TariffRemark"] = utdata["TripList"][trip]["PriceInfo"]["TariffRemark"]["$"]
       except:
         utdata["TripList"][trip]["PriceInfo"]["TariffRemark"] = ""

       if type(utdata["TripList"][trip]["LegList"]["Leg"]) == list:
         utdata["TripList"][trip]["LegList"] = utdata["TripList"][trip]["LegList"]["Leg"]
       else:
         utdata["TripList"][trip]["LegList"] = [utdata["TripList"][trip]["LegList"]["Leg"]]
     self.write(utdata)
     self.finish()

    
application = tornado.web.Application([
    (r"/trip.json", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

#https://api.sl.se/api2/TravelplannerV2/trip.json
#?key=ed99953977a54a9b8ee0ea7451e9db53&Date=2014-11-21&Time=11:00&originId=5009&destId=9001&numTrips=1

