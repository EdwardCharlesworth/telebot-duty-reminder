default_dump_path = 'dutybot_database.json'

# communicater
maximum_input_trys = 50
yes = 'Yes'
no = 'No'
yes_no_options = [yes, no]
def string_to_bool(input):
    if input == yes:
        return True
    return False
add_abort_message = "\nstart input with '/' - abort with /exit "
