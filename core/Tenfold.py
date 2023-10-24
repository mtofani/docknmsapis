import zeep

class Tenfold(object):

    def __init__(self):
        pass
    
    def getSubsNumber(self, idSubs):
        try:
            wsdl = 'https://iibaph01.iplan.com.ar/IdANumeroSuscripcionService/IdANumeroSuscripcionPort?wsdl'
            client = zeep.Client(wsdl=wsdl)
            
            request_data = {
                "id": str(idSubs)
            }
            
            response = client.service.IdANumeroSuscripcionOperation(**request_data)
            
            return response
        except Exception as e:
            print(e)