from elasticsearch import Elasticsearch

#Defining the necessary parameters
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
index_name = "flickrphotos"
mapping = { "mappings": {
"properties": {
"id": {"type": "text"},
"userid": {"type": "text"},
"title": {"type": "text"},
"tags": {"type": "text"},
"latitude": {"type": "double"},
"longitude": {"type": "double"},
"views": {"type": "integer"},
"date_taken": {"type": "date","format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
"date_uploaded": {"type": "date","format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
"accuracy": {"type": "short"},
"flickr_secret": {"type": "keyword"},
"flickr_server": {"type": "keyword"},
"flickr_farm": {"type": "keyword"},
"x": {"type": "double"},
"y": {"type": "double"},
"z": {"type": "double"},
"location" : {"type" : "geo_point"}
}
}
}

#Creating ELK index
es.indices.create(index=index_name, body=mapping)