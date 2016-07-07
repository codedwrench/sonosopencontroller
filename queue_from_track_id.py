# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from soco import SoCo
from soco.data_structures import DidlItem, DidlResource
from soco.music_services import MusicService
from soco.compat import quote_url


device = SoCo("192.168.1.80")  # <------- Your IP here
service = MusicService("Deezer")  # <------ Your Music Service here
track_id = service.get_metadata(item_id='radio-37635')['mediaMetadata']['id']


def add_from_service(item_id, service, device, is_track=True):


    # The DIDL item_id is made of the track_id (url escaped), but with an 8
    # (hex) digit prefix. It is not clear what this is for, but it doesn't
    # seem to matter (too much) what it is. We can use junk (thought the
    # first digit must be 0 or 1), and the player seems to do the right
    # thing. Real DIDL items sent to a player also have a title and a
    # parent_id (usually the id of the relevant album), but they are not
    # necessary. The flow charts at http://musicpartners.sonos.com/node/421
    # and http://musicpartners.sonos.com/node/422 suggest that it is the job
    # of the player, not the controller, to call get_metadata with a track
    # id, so this might explain why no metadata is needed at this stage.

    # NB: quote_url will break if given unicode on Py2.6, and early 2.7. So
    # we need to encode.


    item_id = quote_url(item_id.encode('utf-8'))
    didl_item_id = "0fffffff{0}".format(item_id)

    # For an album:
    if not is_track:
        uri = 'x-rincon-cpcontainer:' + didl_item_id

    else:
        # For a track:
        uri = service.sonos_uri_from_id(item_id)

    res = [DidlResource(uri=uri, protocol_info="DUMMY")]
    didl = DidlItem(title="DUMMY",
        # This is ignored. Sonos gets the title from the item_id
        parent_id="DUMMY",  # Ditto
        item_id=didl_item_id,
        desc=service.desc,
        resources=res)

    device.add_to_queue(didl)


add_from_service(track_id, service, device, True)

