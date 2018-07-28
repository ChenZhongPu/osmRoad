# --------------------------------------------------------------------
# The osmRoad is
#
# Copyright (c) 2018 by Zhongpu Chen (chenloveit@gmail.com)
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

import xml.etree.cElementTree as et


def load_osm(filename):
    root = et.parse(filename).getroot()
    return root


def load_parse_osm(filename):
    root = load_osm(filename)
    return {'bound': parse_bound(root), 'nodes': parse_node(root), 'ways': parse_way(root)}


def load_parse_osmxy(filename):
    root = load_osm(filename)
    return {'bound': parse_bound(root), 'nodes': parse_nodexy(root), 'ways': parse_way(root)}


def parse_bound(root):
    bound = root.findall('bounds')[0]
    xmin = float(bound.attrib['minlon'])
    xmax = float(bound.attrib['maxlon'])
    ymin = float(bound.attrib['minlat'])
    ymax = float(bound.attrib['maxlat'])
    return {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}


def parse_nodexy(root):
    nodes = {}
    for node in root.findall('node'):
        nodes[int(node.attrib['id'])] = (float(node.attrib['lon']), float(node.attrib['lat']))
    return nodes


def parse_node(root):
    nodes = {}
    idx = 0
    for node in root.findall('node'):
        nodes[int(node.attrib['id'])] = idx
        idx += 1
    return nodes


def parse_way(root):
    # refer to https://wiki.openstreetmap.org/wiki/Key:highway
    road_vals = ['montorway', 'motorway_link', 'trunk', 'trunk_link',
                 'primary', 'primary_link', 'secondary', 'secondary_link',
                 'tertiary', 'road', 'residential', 'living_street',
                 'service', 'services', 'motorway_junction']
    ways = []
    for way in root.findall('way'):
        nodes = []
        for node in way.findall('nd'):
            nodes.append(int(node.attrib['ref']))
        tags = {}
        for tag in way.findall('tag'):
            tags[tag.attrib['k']] = tag.attrib['v']
        # only highway is kept
        if 'highway' not in tags:
            continue
        if tags['highway'] not in road_vals:
            continue
        ways.append((nodes, tags))
    return ways

