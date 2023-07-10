import sys
import argparse
import quickfix as fix
import quickfix44 as fix44



ECHO_DEBUG= True
sessionID = 0


class Application(fix.Application):
        orderID = 0
        execID = 0
        global sessionID

        def gen_ord_id(self):
            global orderID
            orderID+=1
            return orderID


        def onCreate(self, sessionID):
            print("created!!!!")
            return

        def onLogon(self, sessionIDIn):

            # print("la prueba de fuego : ", str(sessionIDIn))


            session = fix.Session.lookupSession(sessionIDIn)

            if session and session.isLoggedOn():
                print("Estás logueado en la aplicación FIX")
            else:
                print("No estás logueado en la aplicación FIX")

            # print(" FromApp: %s " + str(message))

            mktcodes = ["GBPUSD", "EURUSD", "CCCCCC"]
   
            reqID = 1
            for mkt in mktcodes:

                message = fix.Message()
                header = message.getHeader();
                header.setField(fix.MsgType("R")) #35
                message.setField(644, "99999999")  # ReqId
                message.setField(146, "1")  # ReqId # 644
                message.setField(55, mkt)  # 55=SMBL
                message.setField(263, "1")  # SubscriptionRequestType
                message.setField(262, "12356") #Request Type
                message.setField(264, "1")  # Market Depth

                fix.Session.sendToTarget(message, self.sessionID)
            
                symbol = message.getField(fix.Symbol().getField())
                print(symbol)

            return

        def onLogout(self, sessionID):
            return

        def toAdmin(self, message, sessionID):
            self.sessionID = sessionID
            print(" toAdmin " + str(message))
            # print( " session Id " + str(sessionID))
            # print(" login Message " + str(message.getHeader().getField(fix.MsgType().getField())))
            if(message.getHeader().getField(fix.MsgType().getField()) == "A"):
                # print(" login Message already inside " + str(sessionID))
                message.setField(fix.Username("test80129"))
                message.setField(fix.Password("fd55ds64"))
            return

        def toApp(self, sessionID, message):
            print("ToApp: %s" % message.toString())
            return

        def fromAdmin(self, sessionID, message):
            print("fromAdmin: %s" % message.toString())

            return
        
        def fromApp(self, sessionID, message ):
            print(" FromApp: %s " + str(message))
            symbol = message.getField(fix.Symbol().getField())
            print(symbol)
            
            return
        

        def genOrderID(self):
            self.orderID = self.orderID+1
            return self.orderID


        def genExecID(self):
            self.execID = self.execID+1
            return self.execID

        def requestQuote(self):
            print("Creating the following order: ")
            message = fix.Message()
            header = message.getHeader();
            header.setField(fix.MsgType("R"))
            message.setField(55, 'CCCCCC')  # 55=SMBL ?

            print(message.toString())

            fix.Session.sendToTarget(message, self.sessionID)


def main(config_file):
    try:
            # print("esto es lo que trae el config file : " + config_file)

            settings = fix.SessionSettings( config_file )

            print(settings)

            application = Application()
            storeFactory = fix.FileStoreFactory( settings )
            logFactory = fix.FileLogFactory( settings )
            initiator = fix.SocketInitiator( application, storeFactory, settings, logFactory )

            initiator.start()

            while 1:
                #  if session.isLoggedOn():
                #     print("Conexión activa a la API FIX")
                # else:
                # print("ccocococococ")
                # import time
                # time.sleep(1)
                input1 = input(" Input \n")

                # print("el input : " + str(input1))

                print(input1)

                if input1 == 'q':
                    print("Request Quote")
                    application.requestQuote()
                if input1 == '2':
                    sys.exit(0)
                if input1 == 'd':
                    import pdb
                    pdb.set_trace()
                else:
                    print("Valid input is 1 for order, 2 for exit")
                    continue

    except fix.ConfigError as e:
            print(e)

            # --configfile archivo.cfg

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('-c', '--configfile', default="/clientLocal.cfg",help='file to read the config from')
    args = parser.parse_args()
    main(args.configfile)
    # config_file = 'C:\Users\Romario Diaz\Desktop\quickfix\prueba2\config_file.conf'
                            