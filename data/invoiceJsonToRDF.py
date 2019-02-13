#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import requests
import json
import time
from random import randint

skeleton = '''
    <!-- http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID** -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**">
        <rdf:type rdf:resource="http://www.semanticweb.org/MUIA/pproci#invoice"/>
        <electronic_invoice rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">**ELECTRONIC_INVOICE**</electronic_invoice>
        <invoice_status rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**INVOICE_STATUS**</invoice_status>
        <invoice_title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**INVOICE_TITLE**</invoice_title>
        <invoice_uri rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://www.zaragoza.es/sede/servicio/factura/**INVOICE_ID**.json</invoice_uri>
    </owl:NamedIndividual>
    


    <!-- http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/CA -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/CA">
        <rdf:type rdf:resource="http://www.w3.org/ns/org#Organization"/>
        <public-contracts:contractingAuthority rdf:resource="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**"/>
        <organization_id rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**ORGANIZATION_ID**</organization_id>
        <organization_title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**ORGANIZATION_TITLE**</organization_title>
        <organization_uri rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">**ORGANIZATION_URI**</organization_uri>
    </owl:NamedIndividual>
    


    <!-- http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/CO -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/CO">
        <rdf:type rdf:resource="http://www.w3.org/ns/org#Organization"/>
        <contracted_organization rdf:resource="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**"/>
        <cif rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**CIF**</cif>
        <organization_id rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**TERCERO_ID**</organization_id>
        <organization_title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">**TERCERO_TITLE**</organization_title>
    </owl:NamedIndividual>
    


    <!-- http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/IEC -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/IEC">
        <rdf:type rdf:resource="http://www.semanticweb.org/MUIA/pproci#invoice_economic_conditions"/>
        <invoice_economic_conditions rdf:resource="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**"/>
        <currency rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Euros</currency>
        <currency_value rdf:datatype="http://www.w3.org/2001/XMLSchema#float">**CURRENCY_VALUE**</currency_value>
    </owl:NamedIndividual>
    


    <!-- http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/ITC -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**/ITC">
        <rdf:type rdf:resource="http://www.semanticweb.org/MUIA/pproci#invoice_temporal_conditions"/>
        <invoice_temporal_conditions rdf:resource="http://www.semanticweb.org/MUIA/pproci#**INVOICE_ID**"/>
        <billing_period rdf:datatype="http://www.w3.org/2001/XMLSchema#date">**BILLING_PERIOD**</billing_period>
        <date_of_issue rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTimeStamp">**DATE_ISSUE**</date_of_issue>
        <date_of_payment rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTimeStamp">**DATE_PAY**</date_of_payment>
    </owl:NamedIndividual>\n\n\n'''

out = open("parsedJson.xml","w+")
outputData = ''

with open('invoices.json') as f:
    data = json.load(f)

for invoice in data['result']:
    tmp = skeleton
    tmp = tmp.replace('**INVOICE_ID**' ,str(invoice['id']))
    tmp = tmp.replace('**INVOICE_TITLE**' ,invoice['title'])
    tmp = tmp.replace('**ORGANIZATION_ID**' ,str(invoice['entidad']['id']))
    tmp = tmp.replace('**ORGANIZATION_TITLE**' ,invoice['entidad']['title'])
    tmp = tmp.replace('**ORGANIZATION_URI**' ,invoice['entidad']['uri'])
    tmp = tmp.replace('**TERCERO_ID**' ,str(invoice['tercero']['id']))
    tmp = tmp.replace('**TERCERO_TITLE**' ,invoice['tercero']['title'])
    if len(invoice['tercero']) > 2: 
        tmp = tmp.replace('**CIF**' ,invoice['tercero']['cif']) 
    else: 
        tmp = tmp.replace('**CIF**' ,'')
    if invoice['facturaElectronica'] == 'N':
        tmp = tmp.replace('**ELECTRONIC_INVOICE**' ,'0')
    else:
        tmp = tmp.replace('**ELECTRONIC_INVOICE**' ,'1')
    tmp = tmp.replace('**CURRENCY_VALUE**' ,str(invoice['amount']))
    tmp = tmp.replace('**BILLING_PERIOD**' ,str(invoice['ejercicio']))
    tmp = tmp.replace('**DATE_ISSUE**' ,invoice['issued'])
    tmp = tmp.replace('**DATE_PAY**' ,invoice['payment'])
    if invoice['status'] == 'Pagada':
        tmp = tmp.replace('**INVOICE_STATUS**' ,'Paid')
    else:
        tmp = tmp.replace('**INVOICE_STATUS**' ,'Not Paid')
    outputData += tmp

out.write(outputData)
