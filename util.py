from private_constants import DEV_MODE

def dev_print(message):
    '''
    Prints only if DEV_MODE is enabled
    @arg: message to be printed
    @argtype: str
    '''
    
    if DEV_MODE:
        print(message)
