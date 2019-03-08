import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

############################################
# get_ctastations.py
# Script for collecting CTA Stations data
############################################

class get_ctastations(dml.Algorithm):
    contributor = 'smithnj'
    reads = []
    writes = ['smithnj.ctastations']

    @staticmethod
    def execute(trial=False):

        startTime = datetime.datetime.now()

        # ---[ Connect to Database ]---------------------------------
        client = dml.pymongo.MongoClient()
        repo = client.cs506
        repo.authenticate('smithnj', 'bOstonuniv!!')
        repo_name = ctastations.writes[0]

        # ---[ Grab Data ]-------------------------------------------
        url = 'https://data.cityofchicago.org/api/views/4qtv-9w43/files/8762c89e-813a-4c5a-9f09-fb0eb740dde0?filename=CTA_RailStations.kml'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        jsondata = json.loads(data)
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)

        # ---[ MongoDB Insertion ]-------------------------------------------
        repo.dropCollection('ctastations')
        repo.createCollection('ctastations')
        repo[repo_name].insert_many(r)
        repo[repo_name].metadata({'complete': True})

        # ---[ Finishing Up ]-------------------------------------------
        print(repo[repo_name].metadata())
        repo.logout()
        endTime = datetime.datetime.now()
        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
#-----------------------__!!!!!!!!!!!!!!!!!!!!!NOT COMPLETE!!!!!!!!!!!!!!!!!!!!__---------------------------------------------------
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
        '''
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f')
        doc.add_namespace('dmc', 'http://datamechanics.io/data/smithnj')
        this_script = doc.agent('alg:smithnj#get_ctastations', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('dmc:5neh-572f.json', {'prov:label':'CTA - Ridership - L Station Entries - Daily Totals', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_ctastations = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(get_ctastations, this_script)
        doc.usage(get_ctastations, resource, startTime, None, {prov.model.PROV_TYPE.'ont:Retrieval'})
        ctastations = doc.entity('dat:smithnj#ctastations', {prov.model.PROV_LABEL:''})

        return doc
