# Now

- Get rid of all import tests

- Move more stuff out of classes, into fixutres

- Convert class-based tests to function-based

- Remove "injected" field, the caller implicitly looks up things it is not 
  provided
  
  - Move the "attr" field type

# Next

- Have an "environment" that gets passed down

- request which encases the possible values

- Renderer

- Is-a predicate matching based on isinstance with priority given to 
  most-specific class

# Soon

- Schema

- Adapter

- View

- App

# Later

- Look for TODO and fix

- Make a Sphinx install and start writing some docs

- Proxies on request which implement the "traversal"

- Allow `for_` to default to some stated default (`IndexView`)