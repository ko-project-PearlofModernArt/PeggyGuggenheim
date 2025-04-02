mport xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, DC, DCTERMS, OWL, XSD


TEI = Namespace("http://www.tei-c.org/ns/1.0")
SCHEMA = Namespace("https://schema.org/")
WIKIDATA = Namespace("https://www.wikidata.org/wiki/")
FABIO = Namespace("https://sparontologies.github.io/fabio/current/fabio.html")
CRM = Namespace("https://www.cidoc-crm.org/")

def main():
   
    tree = ET.parse('/Users/pro/Desktop/xml/peggy-letter.xml')
    root = tree.getroot()
    
  
    g = rdflib.Graph()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    base_uri = "https://w3id.org/pearlofmodernart.org/"
    

    g.bind("tei", TEI)
    g.bind("schema", SCHEMA)
    g.bind("wikidata", WIKIDATA)
    g.bind("crm", CRM)
    g.bind("fabio", FABIO)
    
    
    letter_uri = URIRef(base_uri + "letter")
    g.add((letter_uri, RDF.type, FABIO.Letter))
    

    def safe_text(elem, path):
        target = elem.find(path, ns)
        return target.text if target is not None else None
    

    title = safe_text(root, ".//tei:titleStmt/tei:title")
    if title:
        g.add((letter_uri, DC.title, Literal(title)))
    
 
    author = safe_text(root, ".//tei:author")
    if author:
        author_uri = URIRef(base_uri + "person/" + author.replace(" ", "_"))
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author)))
        g.add((letter_uri, DC.creator, author_uri))
    
    
    date = root.find(".//tei:date[@when]", ns)
    if date is not None:
        g.add((letter_uri, DCTERMS.created, Literal(date.get("when"), datatype=XSD.date)))
    

    for person in root.findall(".//tei:person", ns):
        person_id = person.get("{http://www.w3.org/XML/1998/namespace}id")
        if person_id:
            person_uri = URIRef(base_uri + "person/" + person_id)
            g.add((person_uri, RDF.type, FOAF.Person))
            
  
            name = safe_text(person, "./tei:persName")
            if name:
                g.add((person_uri, FOAF.name, Literal(name)))
            

            occupation = safe_text(person, "./tei:occupation")
            if occupation:
                g.add((person_uri, SCHEMA.hasOccupation, Literal(occupation)))
            
          
            same_as = person.get("sameAs")
            if same_as and same_as.startswith("https://www.wikidata.org"):
                g.add((person_uri, OWL.sameAs, URIRef(same_as)))
    
        
   
        body_div = root.find(".//tei:div[@type='body']", ns)
        if body_div is not None:

              body_uri = URIRef(base_uri + "text/body")
              g.add((body_uri, RDF.type, SCHEMA.Text))
    
   
              full_text = ' '.join(body_div.itertext()).replace('\n', ' ').replace('  ', ' ').strip()
              g.add((body_uri, RDF.value, Literal(full_text)))
    

    pollock_ref = body_div.find(".//tei:persName[@ref='#Pollock']", ns)
    if pollock_ref is not None:
        g.add((body_uri, SCHEMA.mentions, URIRef(base_uri + "person/Pollock")))
    g.add((letter_uri, SCHEMA.hasPart,body_uri ))

    for action in root.findall(".//tei:correspAction", ns):
        action_type = action.get("type")
        person = action.find("tei:persName", ns)
        place = action.find("tei:placeName", ns)
        date_elem = action.find("tei:date", ns)
        
        if person is not None:
            event_uri = URIRef(base_uri + f"event/{action_type}-1947-05-05")
            g.add((event_uri, RDF.type, CRM.E7_Activity))
            g.add((letter_uri, CRM.P129_is_about, event_uri))
            
    
            person_ref = person.get("ref", "").strip("#")
            if person_ref:
                g.add((event_uri, CRM.P14_carried_out_by, URIRef(base_uri + f"person/{person_ref}")))
            
    
            if place is not None and place.text:
                place_uri = URIRef(base_uri + "place/" + place.text.replace(" ", "_"))
                g.add((place_uri, RDF.type, SCHEMA.Place))
                g.add((place_uri, SCHEMA.name, Literal(place.text.strip())))
                g.add((event_uri, CRM.P7_took_place_at, place_uri))
            
  
            if date_elem is not None and date_elem.get("when"):
                g.add((event_uri, CRM.P4_has_time_span, Literal(date_elem.get("when"), datatype=XSD.date)))
    

        opener = root.find(".//tei:opener", ns)
        if opener is not None:
                opener_salute = opener.find("./tei:salute", ns)
                if opener_salute is not None:
                  opener_salute_uri = URIRef(base_uri + "text/opener_salute")
                  g.add((opener_salute_uri, RDF.type, SCHEMA.Text))
                  opener_salute_text = ' '.join(opener_salute.itertext()).strip()
                  g.add((opener_salute_uri, RDF.value, Literal(opener_salute_text)))
                  g.add((URIRef(base_uri + "text/opener"), SCHEMA.hasPart, opener_salute_uri))
        g.add((letter_uri, SCHEMA.hasPart,opener_salute_uri ))

        closer = root.find(".//tei:closer", ns)
        if closer is not None:
           closer_salute = closer.find("./tei:salute", ns)
           if closer_salute is not None:
             closer_salute_uri = URIRef(base_uri + "text/closer_salute")
             g.add((closer_salute_uri, RDF.type, SCHEMA.Text))
             closer_salute_text = ' '.join(closer_salute.itertext()).strip()
             g.add((closer_salute_uri, RDF.value, Literal(closer_salute_text)))
             g.add((URIRef(base_uri + "text/closer"), SCHEMA.hasPart, closer_salute_uri))
        g.add((letter_uri, SCHEMA.hasPart,closer_salute_uri ))
  
        postscript = root.find(".//tei:postscript", ns)
        if postscript is not None:

          postscript_uri = URIRef(base_uri + "text/postscript")
          g.add((postscript_uri, RDF.type, SCHEMA.Text))
    
 
          pers_name = postscript.find(".//tei:persName", ns)
          if pers_name is not None :
     
           signature_uri = URIRef(base_uri + "text/postscript_signature")
           g.add((signature_uri, RDF.type, SCHEMA.Text))
           g.add((signature_uri, RDF.value, Literal(pers_name.text.strip())))
           g.add((signature_uri, SCHEMA.author, URIRef(base_uri + "person/Guggenheim")))
           
    

          postscript_text = " ".join([
             t.strip() for t in postscript.itertext() 
             if t.strip() and (pers_name is None or t.strip() != pers_name.text.strip())
             ]).replace("  ", " ")
        g.add((postscript_uri, RDF.value, Literal(postscript_text)))
             

        g.add((letter_uri, SCHEMA.hasPart, postscript_uri))

    output_file = "peggy-letter.ttl"
    g.serialize(destination=output_file, format="turtle", encoding="utf-8")
   
