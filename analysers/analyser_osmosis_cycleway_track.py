#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    cycle_track.id,
    cycleway.id,
    ST_AsText(way_locate(cycle_track.linestring))
FROM
    (
        SELECT
            id,
            linestring
        FROM
            ways
        WHERE
            tags?'highway' AND
            tags->'highway' != 'cycleway' AND
            tags?'cycleway' AND
            tags->'cycleway' IN ('track', 'opposite_track')
    ) AS cycle_track
    JOIN (
        SELECT
            id,
            linestring
        FROM
            ways
        WHERE
            tags?'highway' AND
            tags->'highway' = 'cycleway'
    ) AS cycleway ON
        cycle_track.linestring && cycleway.linestring AND
        ST_Length(ST_Intersection(ST_Buffer(cycle_track.linestring, 1e-5), cycleway.linestring)) > 5e-5
;
"""

class Analyser_Osmosis_Cycleway_track(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1180", "level": 2, "tag": ["geom", "highway", "cycleway", "fix:chair"], "desc": T_(u"Duplicated cycle tracks, highway=*+cycleway=track and highway=cycleway") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format(""), self.callback10)
