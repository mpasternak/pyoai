
#
class BadArgumentError(Exception):
    pass

def validate(argspec, dict):
    exclusive = None
    for arg_name, arg_type in list(argspec.items()):
        if arg_type == 'exclusive':
            exclusive = arg_name
    # check if we have unknown arguments
    for key, value in list(dict.items()):
        if key not in argspec:
            msg = "Unknown argument: %s" % key
            raise BadArgumentError(msg)
    # first investigate if we have exclusive argument
    if exclusive in dict:
        if len(dict) > 1:
            msg = ("Exclusive argument %s is used but other "
                   "arguments found." % exclusive)
            raise BadArgumentError(msg)
        return
    # if not exclusive, check for required
    for arg_name, arg_type in list(argspec.items()): 
        if arg_type == 'required':
            msg = "Argument required but not found: %s" % arg_name
            if arg_name not in dict:
                raise BadArgumentError(msg)
    return
        
class ValidationSpec(object):
    GetRecord = {
        'identifier':'required',
        'metadataPrefix':'required'
        }
    GetMetadata = {
        'identifier':'required',
        'metadataPrefix':'required'
        }
    
    Identify = {
        }

    ListIdentifiers = {
        'from_':'optional',
        'until':'optional',
        'metadataPrefix':'required',
        'set':'optional',
        }

    ListMetadataFormats = {
        'identifier':'optional'
        }

    ListRecords = {
        'from_':'optional',
        'until':'optional',
        'set':'optional',
        'metadataPrefix':'required',
        }

    ListSets = {
        }

class ResumptionValidationSpec(ValidationSpec):

    ListIdentifiers = {
        'from_':'optional',
        'until':'optional',
        'metadataPrefix':'required',
        'set':'optional',
        'resumptionToken':'exclusive',
        }
    
    ListRecords = {
        'from_':'optional',
        'until':'optional',
        'set':'optional',
        'metadataPrefix':'required',
        'resumptionToken':'exclusive',
        }

    ListSets = {
        'resumptionToken':'exclusive',
        }

def validateArguments(verb, kw):
    validate(getattr(ValidationSpec, verb), kw)

def validateResumptionArguments(verb, kw):
    validate(getattr(ResumptionValidationSpec, verb), kw)
    
