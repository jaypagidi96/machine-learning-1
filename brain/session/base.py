#!/usr/bin/python

'''

This file serves as the superclass for 'data_xx.py', and 'model_xx.py' files.

Note: the term 'dataset' used throughout various comments in this file,
      synonymously implies the user supplied 'file upload(s)', and XML url
      references.

'''

from flask import current_app
from brain.validator.settings import Validator


class Base(object):
    '''

    This class provides a general base class, used for the following sessions,
    and within their corresponding classes:

        - data_new
        - data_append
        - model_generate
        - model_predict

    Note: this class is invoked within 'data_xx.py', 'model_xx.py'

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self, premodel_data):
        '''

        This constructor is responsible for defining class variables.

        '''

        self.premodel_data = premodel_data
        self.list_model_type = current_app.config.get('MODEL_TYPE')
        self.session_type = self.premodel_data['properties']['session_type']
        self.list_error = []

    def validate_arg_none(self):
        '''

        This method checks if the class variable 'premodel_data' is defined.

        '''

        if self.premodel_data is None:
            return True
        else:
            return False

    def validate_premodel_settings(self):
        '''

        This method validates the provided settings (not the dataset), that
        describe the session.

        '''

        error = Validator().validate_settings(
            self.premodel_data['properties'],
            self.session_type
        )

        session_type = self.premodel_data['properties'].get('session_type', None)
        if session_type in ['data_add', 'data_append']:
            location = self.premodel_data['properties']['session_name']
        else:
            location = session_type

        if error:
            self.list_error.append({
                'location': location,
                'message': str(error)
            })

    def get_errors(self):
        '''

        This method returns all current errors associated with this class.

        '''

        return self.list_error
