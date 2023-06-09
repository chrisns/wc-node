###*
# 403 (Forbidden) Handler
#
# Usage:
# return res.forbidden();
# return res.forbidden(err);
# return res.forbidden(err, 'some/specific/forbidden/view');
#
# e.g.:
# ```
# return res.forbidden('Access denied.');
# ```
###

module.exports = (data, options) ->
# Get access to `req`, `res`, & `sails`
  req = @req
  res = @res
  sails = req._sails
  # Set status code
  res.status 403
  # Log error to console
  if data != undefined
    sails.log.verbose 'Sending 403 ("Forbidden") response: \n', data
  else
    sails.log.verbose 'Sending 403 ("Forbidden") response'
  # Only include errors in response if application environment
  # is not set to 'production'.  In production, we shouldn't
  # send back any identifying information about errors.
  if sails.config.environment == 'production'
    data = undefined
  # If the user-agent wants JSON, always respond with JSON
  if req.wantsJSON
    return res.jsonx(data)
  # If second argument is a string, we take that to mean it refers to a view.
  # If it was omitted, use an empty object (`{}`)
  options = if typeof options == 'string' then view: options else options or {}
  # If a view was provided in options, serve it.
  # Otherwise try to guess an appropriate view, or if that doesn't
  # work, just send JSON.
  if options.view
    res.view options.view, data: data
  else
    res.view '403', {data: data}, (err, html) ->
# If a view error occured, fall back to JSON(P).
      if err
#
# Additionally:
# • If the view was missing, ignore the error but provide a verbose log.
        if err.code == 'E_VIEW_FAILED'
          sails.log.verbose 'res.forbidden() :: Could not locate view for error page (sending JSON instead).  Details: ', err
        else
          sails.log.warn 'res.forbidden() :: When attempting to render error page view, an error occured (sending JSON instead).  Details: ', err
        return res.jsonx(data)
      res.send html
