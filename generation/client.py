
import rest_client

def generate_url_filter(model_attributes,filterForm):
    url = '?'
    for attribute in filterForm:
        assert attribute in model_attributes, "Error: " + attribute + " is not an Result attribute."
        for drffilter in filterForm[attribute]:
            assert drffilter in model_attributes[attribute]["filters"], "Error: " + drffilter + " is not a valid filter for Result attribute " + attribute + "."
            if filterForm[attribute][drffilter] != None:
                if type(filterForm[attribute][drffilter]) == int or type(filterForm[attribute][drffilter]) == float:
                    url += attribute + "__" + drffilter + "=" + str(filterForm[attribute][drffilter]) + "&"
                elif type(filterForm[attribute][drffilter]) == str:
                    url += attribute + "__" + drffilter + "=" + filterForm[attribute][drffilter] + "&"
                elif type(filterForm[attribute][drffilter]) == tuple or type(filterForm[attribute][drffilter]) == list:
                    url += attribute + "__" + drffilter + "="
                    start = True
                    for value in filterForm[attribute][drffilter]:
                        if start:
                            url += str(value)
                            start = False
                        else:
                            url += "%2C" + str(value)
                    url += '&'
    return url

def getSourceFilterForm():
    return_value = {
        'id' : {
            'exact' : None,
            'in' : None,
            },
        'patientid' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'offset' : {
            'isnull' : None,
            'exact' : None,
            'gte' : None,
            'lte' : None,
            },
        'sex' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'age' : {
            'isnull' : None,
            'exact' : None,
            'gte' : None,
            'lte' : None,
            },
        'finding' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'RT_PCR_positive' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'survival' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'intubated' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'intubation_present' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'went_icu' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'in_icu' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'needed_supplemental_O2' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'extubated' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'temperature' : {
            'isnull' : None,
            'gte' : None,
            'lte' : None,
            },
        'pO2_saturation' : {
            'isnull' : None,
            'gte' : None,
            'lte' : None,
            },
        'leukocyte_count' : {
            'isnull' : None,
            'gte' : None,
            'lte' : None,
            },
        'neutrophil_count' : {
            'isnull' : None,
            'gte' : None,
            'lte' : None,
            },
        'lymphocyte_count' : {
            'isnull' : None,
            'gte' : None,
            'lte' : None,
            },
        'view' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'modality' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'date' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'location' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'folder' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'filename' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'doi' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'url' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'license' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'clinical_notes' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'other_notes' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'creator' : {
            },
        }
    return return_value

def retrieveSource(filterForm):
    model_attributes =creator
    return "Source/" + generate_url_filter(model_attributes,filterForm)

def getResultFilterForm():
    return_value = {
        'directory' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'filename' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'method' : {
            'iexact' : None,
            'in' : None,
            'istartswith' : None,
            'icontains' : None,
            'iendswith' : None,
            'iregex' : None,
            'search' : None,
            },
        'source' : {
            },
        'creator' : {
            },
        }
    return return_value

def retrieveResult(filterForm):
    model_attributes =creator
    return "Result/" + generate_url_filter(model_attributes,filterForm)


