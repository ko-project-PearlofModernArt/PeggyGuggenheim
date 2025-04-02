import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS,RDFS
import pandas as pd

# Namespaces
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
FABIO = Namespace("https://sparontologies.github.io/fabio/current/fabio.html")
PROV = Namespace("http://www.w3.org/ns/prov#")
CDWA = Namespace("https://www.getty.edu/research/publications/electronic_publications/cdwa/")


# Creating an RDF graph
g = rdflib.Graph()

# Base URI
pt = URIRef("https://w3id.org/pearlofmodernart.org/") 

# Creating URIs
item = URIRef(pt + "item/")
person = URIRef(pt + "person/")
organization = URIRef(pt + "organization/")
place = URIRef(pt + "place/")
museum = URIRef(pt + "museum/")
art_gallery = URIRef(pt + "art_gallery/")
archival_document_set = URIRef(pt + "archival_document_set/")
archival_document = URIRef(pt + "archival_document/")
group = URIRef(pt + "group/")
catalog = URIRef(pt + "catalog/")
physical_medium = URIRef(pt + "physical_medium/")
repository = URIRef(pt + "repository/")
document = URIRef(pt + "document/")

# Bind namespaces to graph
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("crm", CRM)
g.bind("prov", PROV)
g.bind("fabio", FABIO)


# List of CSV files
files_csv = [
   "csvfile_aLetter.csv",
   "csvfile_book.csv",
   "csvfile_catalogue.csv",
   "csvfile_archivaldocument.csv",
   "csvfile,vedio.csv",
   "csvfile_Potrait.csv",
   "csvfile_photo_of_gallery.csv",
   "csvfile_peggy&artist.csv",
   "csvfile_Guggenheim_fundation.csv",
   "csvfile_guggenheim_collection.csv"
    
]
for file in files_csv: 

  df = pd.read_csv(file)
  

# Create a dictionary to store URIs for subjects
  uris_dict =  dict()
  
  items_list = ["PeggyGuggenheimCollection", "Book", "catalog","Archival document", "Solomon R. Guggenheim Foundation", "letter", "PhotoOfPeggyAndArtist", "photo of Art of This Century Gallery", "Potrait of Peggy Guggenheim","VedioClip"]
 
 
    # Process each row in the dataframe
  for _, row in df.iterrows():
        
        subject = row["subject"]
        predicate = row["predicate"]
        object = row["object"]

        
        

        # Check if subject is already in uris_dict
        if subject not in uris_dict:
            subject_uri = URIRef(item + subject.replace(" ", "_"))
            uris_dict[subject] = subject_uri 

        else:
            subject_uri = uris_dict[subject]
       
        
        if predicate == "dcterms:creator":
            predicate_uri = DCTERMS.creator

        elif predicate == "dcterms:isPartOf":
            predicate_uri = DCTERMS.isPartOf

        elif predicate == "foaf:member":
            predicate_uri = FOAF.member

        elif predicate == "crm:P129_is_about":
            predicate_uri = CRM.P129_is_about

        elif predicate == "crm:P2_has_type":
            predicate_uri = CRM.P2_has_type

        elif predicate == "crm:P53_has_former_or_current_location":
            predicate_uri = CRM.P53_has_former_or_current_location

        elif predicate == "prov:wasDerivedFrom":
            predicate_uri = PROV.wasDerivedFrom
        
        elif predicate == "crm:P102_has_title":
            predicate_uri = CRM.P102_has_title

        elif predicate == "crm:P52_is_current_owner_of":
            predicate_uri = CRM.P52_is_current_owner_of

        elif predicate == "crm:P52_has_current_owner":
            predicate_uri = CRM.P52_has_current_owner
        
        elif predicate == "fabio:hasPublisher":
            predicate_uri = FABIO.hasPublisher
        
        elif predicate == "crm:P4_has_time_span":
            predicate_uri = CRM.P4_has_time_span

        elif predicate == "crm:P94_has_created":
            predicate_uri = CRM.P94_has_created

        elif predicate == "crm:P74_has_current_or_former_residence":
            predicate_uri = CRM.P74_has_current_or_former_residence

        elif predicate == "dcterms:issued":
            predicate_uri = DCTERMS.issued

        elif predicate == "dcterms:Medium":
            predicate_uri = DCTERMS.medium
        

        elif predicate == "fabio:has_access_date":
            predicate_uri = FABIO.has_access_date

        elif predicate == "crm:P82a_begin_of_the_begin":
            predicate_uri = CRM.P82a_begin_of_the_begin

        elif predicate == "rdfs:label":
            predicate_uri = RDFS.label
        
        elif predicate == "owl:sameAs":
            predicate_uri = OWL.sameAs
        
        elif predicate == "schema:relatedTo":  
            predicate_uri = SCHEMA.relatedTo
        
        elif predicate == "schema:director":
            predicate_uri = SCHEMA.director
        
        elif predicate == "schema:inLanguage":
            predicate_uri = SCHEMA.inLanguage
        
        elif predicate == "schema:mentions":
            predicate_uri = SCHEMA.mentions
        
        elif predicate == "schema:genre":
            predicate_uri = SCHEMA.genre
        
        elif predicate == "cdwa:DimensionDescription":
            predicate_uri= CDWA.DimensionDescription
        
        elif predicate == "dcterms:rights":
           predicate_uri = DCTERMS.rights

        elif predicate == "foaf:depicts":
            predicate_uri = FOAF.depicts

        elif predicate == "rdf:type":
            predicate_uri = RDF.type
        
        else:
            print(f"⚠️ : {predicate}")
            continue  
       
    
        if predicate_uri == RDF.type:

            if object == "crm:E21_Person":
                obj = CRM.E21_Person

            elif object == "schema:NonprofitType":
                obj = SCHEMA.NonprofitType          
            elif object == "crm:E53_Place":
                obj = CRM.E53_Place
            elif object == "schema:ArtGallery":
                obj = SCHEMA.ArtGallery
            elif object == "schema:Museum":
                obj = SCHEMA.museum
            elif object == "fabio:repository":
                obj = FABIO.repository
            elif object == "dc:PhysicalMedium":
                obj = DCTERMS.PhysicalMedium
            elif object == "foaf:Organization":
                obj = FOAF.Organization
            elif object == "fabio:catalog":
               obj = FABIO.catalog
            elif object == "fabio:archival_document_set":
               obj = FABIO.archival_document_set
            elif object == "fabio:archival_document":
                obj = FABIO.archival_document
            elif object == "crm:E31_Document":
                obj = CRM.E31_Document
            elif object == "schema:Organization":
               obj = SCHEMA.Organization
            
            elif object == "dcterms:SizeOrDuration":
               obj = DCTERMS.SizeOrDuration
            
            else:
              obj = URIRef(object)
            
        
            
    
        elif predicate_uri in [DCTERMS.creator, FOAF.depicts, CRM.P129_is_about, SCHEMA.director, SCHEMA.relatedTo,]:
            if object not in uris_dict:
                 obj = URIRef(person + object.replace(" ", "_"))
                 uris_dict[object] = obj
            else:
                obj = uris_dict[object]
          

        
        elif predicate_uri in [CRM.P94_has_created,CRM.P52_is_current_owner_of]:
            if object not in uris_dict:
                 obj = URIRef(museum + object.replace(" ", "_"))
                 uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        elif predicate_uri in [SCHEMA.mentions]:
            if object not in uris_dict:
                 obj = URIRef(art_gallery + object.replace(" ", "_"))
                 uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        
        elif predicate_uri in [FABIO.hasPublisher,CRM.P52_has_current_owner]:
            if object not in uris_dict:
                 obj = URIRef(organization + object.replace(" ", "_"))
                 uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        elif predicate_uri == FOAF.member:
            if object not in uris_dict:
                obj = URIRef(group + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                 obj = uris_dict[object]

        elif predicate_uri == PROV.wasDerivedFrom:
            if object not in uris_dict:
                obj = URIRef(repository + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                 obj = uris_dict[object]
        
        elif predicate_uri in [CRM.P53_has_former_or_current_location, CRM.P74_has_current_or_former_residence]:
            if object not in uris_dict:
                obj = URIRef(place + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                 obj = uris_dict[object]
        
        elif predicate_uri in [DCTERMS.isPartOf]:
             if object not in uris_dict:
                obj = URIRef(document + object.replace(" ", "_"))
                uris_dict[object] = obj
             else:
                 obj = uris_dict[object]
        

        elif predicate_uri in [DCTERMS.issued, CRM.P82a_begin_of_the_begin, FABIO.has_access_date]:
            if object not in uris_dict:
                try:
                    obj = Literal(object, datatype=XSD.date)
                except ValueError:
                    obj = Literal(object, datatype=XSD.gYear)
            else:
                obj = uris_dict[object]
        
        
        elif predicate_uri == SCHEMA.inLanguage:
            obj = Literal(object, datatype=XSD.string)  
      
        else:
             obj = Literal(object, datatype=XSD.string)    
        
        if obj is None:
           
            continue  
        
        g.add((subject_uri, predicate_uri, obj))

print(f"✅ : {file}")
    
# Serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=pt, encoding="utf-8")

# Write the Turtle string to a file
with open("csv_convert_output.ttl", "wb") as f:
    f.write(turtle_str)


