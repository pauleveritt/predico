# Now

- Example app

- Docs

# Next

- Formalize the System/Request concepts

    - System represents Sphinx, is instantiated once during the lifetime 
      of the process, an adapter provides SphinxSystem to 
      implement/extend the contract
      
    - Request is created/destroyed on every request, SphinxRequest adapter to 
      implement/extend etc.  

- Renderer

# Soon

- Publish

- Bring in jinja2_component

# Later

- Is-a predicate matching based on isinstance with priority given to 
  most-specific class

- Have the base class just be like a marker interface (e.g. Request) 
  and have a default=True registration that can be overridden by a 
  customization
  
- Schema service

- Look for TODO and fix

- Mimic Pyramid request methods by allowing adapters to say if they want 
  to hang off the request at some well-known-name. Then add a 
  Request.__getattr__ which looked for the well-known things (view, resource, 
  etc.) then if no match, try to make an adapter

- Configurable development-only pydantic validation

    - Look for the knob
    
    - Take the class wrapped by the dataclass decorator
    
    - Do pydantic.etc.dataclass(TargetClass) without the decorator 
      to validate, then discard

- Allow per-request injectables, to let parent components decorate for 
  their children, like context stuff in React
  