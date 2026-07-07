"""
Built-in analysis modules.

Every module here defines one or more :class:`~mdforge.core.base.BaseAnalysis`
subclasses, which auto-register on import.  The registry imports all modules in
this package (except ``plugins``, handled separately) at selection time.
"""
