# Now

# Next

- Allow per-request injectables, to let parent components decorate for 
  their children, like context stuff in React

- Sometimes __call__ would be nice to pass in arguments to an adapter, for 
  example ``parent: Parents = injected(Parents, resourceid='some/other)``

- One registration for multiple targets, either:

    - resources=[Section, Sectionroot]
    
    - Stacked decorators

# Soon

- Bring in jinja2_component

- Fix the Optional[Request] = None problem, where returning None from 
  get_adapter_value or get_injected_value causes the target(**args) to 
  not construct

# Later

- Jinja2 renderer2

- Publish

- Is-a predicate matching based on isinstance with priority given to 
  most-specific class

- Put in a guard that doesn't allow non-dataclasses to be registered 
  as adapters, views (or perhaps, as anything)
  
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

- Let each service configure the injectables via Service.post_initialize 
  phase done after all the services are "registered"

- Two phases of dataclass fields, where the second phase can use information 
  from the first phase