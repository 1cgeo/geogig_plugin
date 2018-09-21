# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geogig_pg
                                 A QGIS plugin
 Plugin para gerenciar prod
                             -------------------
        begin                : 2018-02-18
        copyright            : (C) 2018 by Cesar
        email                : cesar.soares@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    from main import Main
    return Main(iface)
