"""
Name:       Beer Me
Purpose:    Snag data data from CraftBeer.com and save as a feature class.
DOB:        09Oct2015
Author:     Joel McCune (https://github.com/knu2xs)
"""

# import modules
import xml.etree.ElementTree as ElementTree
import os.path as path
from urllib import request
from time import strftime
import arcpy

# list of attributes in the xml file to be converted into fields in the output feature class
field_list = [
    'id',
    'company',
    'address',
    'city',
    'state',
    'zip',
    'country',
    'phone',
    'member_type',
    'type',
    'url'
]

# url to craft beer xml file
craft_beer_xml = 'http://www.craftbeer.com/wp-content/uploads/ba-us.xml'


def create_feature_class(feature_class):
    """
    Add the craft beer fields to the output feature class.
    :param feature_class: The polygon feature class where attributes will be added to.
    :return: Path to feature class.
    """
    # create the feature class if it does not already exist
    if not arcpy.Exists(feature_class):

        # create the feature class
        fc = arcpy.CreateFeatureclass_management(
            out_path=path.dirname(feature_class),
            out_name=path.basename(feature_class),
            geometry_type='POINT',
            spatial_reference=arcpy.SpatialReference(4326)  # WGS84
        )[0]

        # since all the fields are text, we are just going to iterate and add them all
        for field in field_list:

            # account for the url field needing to be longer
            if field == 'url':
                length = 500
            else:
                length = 100

            # add the field
            arcpy.AddField_management(
                in_table=fc,
                field_name=field,
                field_type='TEXT',
                field_length=length
            )

    # return path
    return feature_class


def craft_beer_xml_to_feature_class(xml_file, feature_class):
    """
    Convert the craft beer file to a feature class.
    :param xml_file: XML file of all breweries.
    :param feature_class: Output feature class of breweries.
    :return: String path to the breweries.
    """
    # load the xml file into an element tree object
    tree = ElementTree.parse(xml_file)

    # create the feature class
    create_feature_class(feature_class)

    # extend field list to include coordinates
    cursor_fields = field_list + ['SHAPE@XY']

    # create an insert cursor to add records to the feature class
    with arcpy.da.InsertCursor(feature_class, cursor_fields) as insert_cursor:

        # iterate the markers in the xml file
        for node in tree.findall('marker'):

            # sequentially extract the elements from the node into a list representing the new row attributes
            row = [str.encode(node.attrib.get(field), 'utf-8') for field in field_list]

            # now get the geometry and add this to the row
            row.append((
                float(node.attrib.get('lng')),
                float(node.attrib.get('lat'))
            ))

            # insert the new row into the output feature class
            insert_cursor.insertRow(row)

    # return the path to the output feature class
    return feature_class


def create_craft_beer_feature_class(feature_class):
    """
    Assuming the url does not change, grab the most recent version of the xml file and create a feature class from it.
    :param feature_class: Output brewery feature class.
    :return: Path to feature class.
    """
    # file location to temporarily save the xml
    xml_file = path.join(arcpy.env.scratchFolder, 'craft_beer.xml')

    # get the data as a response object from Al Gore's interwebs
    request.urlretrieve(craft_beer_xml, xml_file)

    # convert the xml file into a feature class
    craft_beer_xml_to_feature_class(xml_file, feature_class)

    # return the path
    return feature_class


# now, because I am lazy, I am going to just build it here and set it up to timestamp the output feature class
if __name__ == '__main__':

    # output to the ArcGIS default geodatabase for the current user
    output_fc = path.join(
            path.expanduser('~'),  # get user directory
            r'Documents\ArcGIS\Default.gdb',  # place in default user geodatabase
            'craft_beer_' + strftime('%Y%m%d')  # append YYYYMMDD onto the end of the filename for timestamp
    )

    # let the big dawg eat
    create_craft_beer_feature_class(output_fc)
