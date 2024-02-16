""" This is a throttling class that we can use to limit/ specified
 the number of requests that a user can make to our API. """

from rest_framework.throttling import UserRateThrottle


class TenCallsPerMinuteThrottle(UserRateThrottle):
    scope = 'ten'


# class AnonThrottle(UserRateThrottle):
#     scope = 'twenty'