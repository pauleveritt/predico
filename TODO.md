# Now

# Next

- Renderer

# Soon

- Docs

- Example app

- Publish

- Bring in jinja2_component

# Later

- Is-a predicate matching based on isinstance with priority given to 
  most-specific class

- Allow `for_` to default to some stated default (`IndexView`)

- Have the base class just be like a marker interface (e.g. Request) 
  and have a default=True registration that can be overridden by a 
  customization
  
- Schema service

- Look for TODO and fix

- Configurable development-only pydantic validation

    - Look for the knob
    
    - Take the class wrapped by the dataclass decorator
    
    - Do pydantic.etc.dataclass(TargetClass) without the decorator 
      to validate, then discard

- Allow per-request injectables, to let parent components decorate for 
  their children, like context stuff in React
  