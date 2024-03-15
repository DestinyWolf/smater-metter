from time import sleep
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import raw as db


app = Flask(__name__)
api  = Api(app)

class DataInsert(Resource):

    def get(self):
        args = request.args
        data = args.get('data', type=str)
        hora = args.get('hora', type=str)
        tempA = args.get('tempA', type=float)
        tempB = args.get('tempB', type=float)
        tensao = args.get('tensao', type=float)
        corrente = args.get('corrente', type=float)

        newData = {
            '_id' : "|".join([data,hora]),
            'data': data,
            'hora': hora,
            'tempA': tempA,
            'tempB': tempB,
            'tensao': tensao,
            'corrente': corrente
        }

        db.insertInDb(newData)

        return {"message":"dados inseridos com sucesso"}


class Data(Resource):

    def get(self):
        return(jsonify(db.getAllItens()))
        
    def post(self):
        dia = request.json['dia']
        hora = request.json['hora']
        tempB = float(request.json['tempB'])
        tempA = float(request.json['tempA'])
        tensao = float(request.json['tensao'])
        corrente = float(request.json['corrente'])

        newData = {
            "_id" : "|".join([dia,hora]),
            "dia": dia,
            "hora": hora,
            "tempA": tempA,
            "tempB": tempB,
            "tensao": tensao,
            "corrente":corrente
        }

        db.insertInDb(newData)
        return {"message":"Dado inserido"}
    
    def  put(self):
        id = request.json['id']
        data = request.json['data']
        hora = request.json['hora']
        tempB = float(request.json['tempB'])
        tempA = float(request.json['tempA'])
        tensao = float(request.json['tensao'])
        corrente = float(request.json['corrente'])

        newData = {
            "_id" : "|".join([data,hora]),
            "data": data,
            "hora": hora,
            "tempA": tempA,
            "tempB": tempB,
            "tensao": tensao,
            "corrente":corrente
        }

        if(db.getItensByFilter({"_id":id})): 
            newData.pop( '_id') #Remove o _id
            data = db.updateItenByFilter({"_id":id}, newData)
            
            return {"message":"dados atualizados"}
        else:
            db.insertInDb(newData)
            return {"message":"Dado inserido"}
        
    def delete(self):
        id = request.json['id']
        db.deleteItenByFilter({"_id": id})
        return {"message":"Registro deletado"}

        
api.add_resource(Data, '/data')
api.add_resource(DataInsert, '/insert')  

if __name__ ==  '__main__':
    app.run(debug=True)

