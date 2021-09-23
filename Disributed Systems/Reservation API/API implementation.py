""" Reservation API wrapper

This class implements a simple wrapper around the reservation API. It
provides automatic retries for server-side errors, delays to prevent
server overloading, and produces sensible exceptions for the different
types of client-side error that can be encountered.
"""

import sys
import requests
import json as simplejson
import warnings
import time
from requests.api import request

from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError, ReservationLimitError)

class ReservationApi:
    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        """ Create a new ReservationApi to communicate with a reservation
        server.

        Args:
            base_url: The URL of the reservation API to communicate with.
            token: The user's API token obtained from the control panel.
            retries: The maximum number of attempts to make for each request.
            delay: A delay to apply to each request to prevent server overload.
        """
        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay

    def _reason(self, req: requests.Response) -> str:
        """Obtain the reason associated with a response"""
        reason = ''

        # Try to get the JSON content, if possible, as that may contain a
        # more useful message than the status line reason
        try:
            json = req.json()
            reason = json['message']

        # A problem occurred while parsing the body - possibly no message
        # in the body (which can happen if the API really does 500,
        # rather than generating a "fake" 500), so fall back on the HTTP
        # status line reason
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason

        return reason


    def _headers(self) -> dict:
        """Create the authorization token header needed for API requests"""
        # Your code goes here
        return {"Authorization" : "Bearer " + self.token}


    def _send_request(self, method: str, endpoint: str) -> dict:
        """Send a request to the reservation API and convert errors to
           appropriate exceptions"""

        # Your code goes here
        authorization = self._headers()

        # Allow for multiple retries if needed
        counter = 0
        while (counter < self.retries):
            # Perform the request.
            # Delay before processing the response to avoid swamping server.
            if (method == "0"): # get available slots
                url = self.base_url + endpoint
                message = requests.get(url, headers = authorization)
                time.sleep(self.delay) # delay
            elif (method == "1"): # get client reserved slots
                message = requests.get(self.base_url + endpoint, headers = authorization)
                time.sleep(self.delay) # delay
            elif (method == "2"): # free a reserved slot if owned by client
                message = requests.delete(self.base_url + endpoint, headers = authorization)
                time.sleep(self.delay) # delay
            elif (method == "3"): # reserve a slot if free
                message = requests.post(self.base_url + endpoint, headers = authorization)
                time.sleep(self.delay) # delay

            counter += 1
            # 200 response indicates all is well - send back the json data.
            if (message.status_code == 200):
                if (method == "0" or method == "1"):
                    return simplejson.loads(message.text)
                else:
                    return True

            # 5xx responses indicate a server-side error, show a warning
            # (including the try number).
            if (message.status_code == 500 or message.status_code == 503):
                print("WARNING - SERVER ERROR ON TRY #", counter)
                continue
            # 400 errors are client problems that are meaningful, so convert
            # them to separate exceptions that can be caught and handled by
            # the caller.
            elif (message.status_code == 400):
                return BadRequestError
            elif (message.status_code == 401):
                return InvalidTokenError
            elif (message.status_code == 403):
                return BadSlotError
            elif (message.status_code == 404):
                return NotProcessedError
            elif (message.status_code == 409):
                return SlotUnavailableError
            elif (message.status_code == 451):
                return ReservationLimitError
            # Anything else is unexpected and may need to kill the client.
            else:
                sys.exit()
        # Get here and retries have been exhausted, throw an appropriate
        # exception.
        return HTTPError


    def get_slots_available(self):
        """Obtain the list of slots currently available in the system"""
        # Your code goes here
        answer = self._send_request("0", "/reservation/available")

        if (type(answer) == list):
            print("Some available slots found")
            return answer
        elif (answer == BadRequestError):
            print("\nBad request error - request malformed\n")
        elif (answer == InvalidTokenError):
            print("\nInvalid token error\n")
        elif (answer == NotProcessedError):
            print("\nNot processed error - request malformed\n")
        else:
            print("Unforseen error - trying again")
            return []

    def get_slots_held(self):
        """Obtain the list of slots currently held by the client"""
        # Your code goes here
        answer = self._send_request("1", "/reservation")

        if (type(answer) == list):
            if (len(answer) == 0):
                print("You have no slots reserved\n")
                return []
            else:
                print("\nYou have the following slots reserved: ")
                i = 0
                while (i < len(answer)):
                    print(answer[i]["id"])
                    i += 1
                return answer
        elif (answer == BadRequestError):
            print("\nBad request error - request malformed\n")
        elif (answer == InvalidTokenError):
            print("\nInvalid token error\n")
        elif (answer == NotProcessedError):
            print("\nNot processed error - request malformed\n")
        else:
            print("Unforseen error - trying again")
            return []

    def release_slot(self, slot_id):
        """Release a slot currently held by the client"""
        # Your code goes here
        url = "/reservation/{slotid}"
        url = url.format(slotid = slot_id)
        answer = self._send_request("2", url)

        if (answer == True):
            print("\nSlot: ", slot_id, " released")
            return True
        elif (answer == BadRequestError):
            print("\nBad request error - request malformed\n")
            return False
        elif (answer == InvalidTokenError):
            print("\nInvalid token error\n")
            return False
        elif (answer == BadSlotError):
            print("\nBad slot error - slot does not exist\n")
            return False
        elif (answer == NotProcessedError):
            print("\nNot processed error - request malformed\n")
            return False
        elif (answer == SlotUnavailableError):
            print("\nSlot unavailable error - you do not own this slot\n")
            return False
        else:
            print("Unforseen error - trying again")
            return False

    def reserve_slot(self, slot_id):
        """Attempt to reserve a slot for the client"""

        # Your code goes here
        url = "/reservation/{slotid}"
        url = url.format(slotid = slot_id)
        answer = self._send_request("3", url)

        if (answer == True):
            print("\nSlot: ", slot_id, " reserved")
            return True
        elif (answer == BadRequestError):
            print("\nBad request error - request malformed\n")
            return False
        elif (answer == InvalidTokenError):
            print("\nInvalid token error\n")
            return False
        elif (answer == BadSlotError):
            print("\nBad slot error - slot does not exist\n")
            return False
        elif (answer == NotProcessedError):
            print("\nNot processed error - request malformed\n")
            return False
        elif (answer == SlotUnavailableError):
            print("\nSlot unavailable error - slot already reserved\n")
            return False
        elif (answer == ReservationLimitError):
            print("Reservation limit error - reservation total reached")
        else:
            print("Unforseen error - trying again")
            return False
