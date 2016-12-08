# Release 0.4.0 - Friday 9 December  07:17:38 AEDT 2016

- Added test to ensure the session can be manipulated in get_request_kwargs
- Added test to ensure the method can be manipulated in get_request_kwargs
- Cleanup repetition of content-type headers in test_http
- Allow the URL used to make the API request to be manipulated in get_request_kwargs (#5)

# Release 0.3.2 - Friday 9 December  06:15:46 AEDT 2016

- Fixed issue where request_model was incorrectly included in signature to request method. (#4)
- Cleanup internals of the request method - method and session can now be supplied as kwargs to __call__ or returned by get_request_kwargs.

# Release 0.3.1 - Wednesday 7 December  22:50:11 AEDT 2016

- Fixed issue with request data not being sent correctly. (#3)

# Release 0.3.0 - Wednesday 7 December  08:49:59 AEDT 2016

- Breaking API change: __init__ takes arguments for call to create request_cls instance rather than __call__.
- Increase coverage of HTTPEater (#2)

# Release 0.2.0 - Thursday 24 November  11:04:08 AEDT 2016

- Lots of documentation updates.
- HTTPEater.request_cls now defaults to None
- Added dynamic URL formatting.
- Use conda to build Python 3.5 in readthedocs

# Release 0.1.0 - Wednesday 23 November  00:37:41 AEDT 2016

- Initial release


