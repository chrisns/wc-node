###*
# 400 (Bad Request) Handler
#
# Usage:
# return res.badRequest();
# return res.badRequest(data);
# return res.badRequest(data, 'some/specific/badRequest/view');
#
# e.g.:
# ```
# return res.badRequest(
#   'Please choose a valid `password` (6-12 characters)',
#   'trial/signup'
# );
# ```
###

module.exports = (data, options) ->
# Get access to `req`, `res`, & `sails`
  req = @req
  res = @res
  sails = req._sails
  # Set status code
  res.status 400
  # Log error to console
  if data != undefined
    sails.log.verbose 'Sending 400 ("Bad Request") response: \n', data
  else
    sails.log.verbose 'Sending 400 ("Bad Request") response'
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
    res.guessView {data: data}, ->
      res.jsonx data
