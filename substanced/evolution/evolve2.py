from substanced.util import postorder
from substanced.principal import PrincipalToACLBearing
from substanced.objectmap import find_objectmap
import logging

_marker = object()

logger = logging.getLogger('evolution')

def _referenceable_principals(acl):
    result = set()
    for ace in (acl or ()):
        principal_id = ace[1]
        if isinstance(principal_id, (int, long, tuple)):
            result.add(principal_id)
    return result

def evolve(root):
    logger.info(
        'Running substanced evolve step 2: add PrincipalToACLBearing '
        'relationships'
        )
    objectmap = find_objectmap(root)
    if objectmap is None:
        return
    for obj in postorder(root):
        logger.info(
            'Substanced evolve step 2: trying %s' % (obj,)
            )
        acl = getattr(obj, '__acl__', _marker)
        if acl is _marker:
            continue
        for princid in _referenceable_principals(acl):
            objectmap.connect(
                princid, obj, PrincipalToACLBearing
                )